###############################################################################
# Filename: Permission.py                                                      #
# Project: OpenPlains Inc.                                                     #
# File Created: Tuesday September 3rd 2024                                     #
# Author: Corey White (smortopahri@gmail.com)                                  #
# Maintainer: Corey White                                                      #
# -----                                                                        #
# Last Modified: Tue Sep 03 2024                                               #
# Modified By: Corey White                                                     #
# -----                                                                        #
# License: GPLv3                                                               #
#                                                                              #
# Copyright (c) 2024 OpenPlains Inc.                                           #
#                                                                              #
# django-actinia is an open-source django app that allows for with             #
# the Actinia REST API for GRASS GIS for distributed computational tasks.      #
#                                                                              #
# This program is free software: you can redistribute it and/or modify         #
# it under the terms of the GNU General Public License as published by         #
# the Free Software Foundation, either version 3 of the License, or            #
# (at your option) any later version.                                          #
#                                                                              #
# This program is distributed in the hope that it will be useful,              #
# but WITHOUT ANY WARRANTY; without even the implied warranty of               #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the                #
# GNU General Public License for more details.                                 #
#                                                                              #
# You should have received a copy of the GNU General Public License            #
# along with this program.  If not, see <https://www.gnu.org/licenses/>.       #
#                                                                              #
###############################################################################

from django.db import models
from django.core.exceptions import ValidationError
from .ActiniaUser import ActiniaUser
from .abstracts.ObjectInfoAbstract import ObjectInfoAbstract
from .abstracts.ObjectAuditAbstract import ObjectAuditAbstract
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from datetime import time
import ast
import operator

import logging

logger = logging.getLogger(__name__)


class Permission(ObjectAuditAbstract):
    ACTIONS = [
        ("read", "Read"),
        ("write", "Write"),
        ("delete", "Delete"),
        ("execute", "Execute"),
    ]

    actinia_user = models.ForeignKey(ActiniaUser, on_delete=models.CASCADE)
    action = models.CharField(max_length=50, choices=ACTIONS)

    # Generic Foreign Key to link to any model
    content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, related_name="grass_permissions"
    )
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    # When clause fields
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    day_of_week = models.CharField(
        max_length=9, null=True, blank=True
    )  # e.g., "Monday"
    custom_condition = models.TextField(
        null=True, blank=True
    )  # Store a custom condition as a string

    class Meta:
        unique_together = ("actinia_user", "content_type", "object_id", "action")

    def __str__(self):
        return f"{self.actinia_user} - {self.action} on {self.content_object}"

    def is_within_time_range(self):
        if self.start_time and self.end_time:
            now = time.now()
            return self.start_time <= now <= self.end_time
        return True

    def is_day_of_week(self):
        if self.day_of_week:
            return self.day_of_week == time.now().strftime("%A")
        return True

    def evaluate_custom_condition(self, context):
        if self.custom_condition:
            # You can use `eval`, `exec`, or a safer custom parser here
            # Pass context variables to eval the condition
            # custom_condition = "context['user_role'] == 'admin' and context['request_method'] == 'POST'"
            # Pass context like

            # context = {
            #     'user_role': user.role,
            #     'request_method': request.method,
            # }

            # has_permission = mapset.has_permission(request.user.actiniauser, 'write', context=context)
            return self._evaluate_expression(self.custom_condition, {}, context)
        return True

    def is_valid(self, context=None):
        return (
            self.is_within_time_range()
            and self.is_day_of_week()
            and self.evaluate_custom_condition(context)
        )

        # Supported operators

    OPERATORS = {
        ast.Eq: operator.eq,
        ast.NotEq: operator.ne,
        ast.Lt: operator.lt,
        ast.LtE: operator.le,
        ast.Gt: operator.gt,
        ast.GtE: operator.ge,
        ast.And: operator.and_,
        ast.Or: operator.or_,
    }

    def _validate_context(self, context):
        allowed_keys = {"user_role", "request_method"}
        for key in context.keys():
            if key not in allowed_keys:
                raise ValueError(f"Invalid context key: {key}")

    def _safe_eval(self, node, context):
        if isinstance(node, ast.BinOp) and type(node.op) in self.OPERATORS:
            left = self._safe_eval(node.left, context)
            right = self._safe_eval(node.right, context)
            return self.OPERATORS[type(node.op)](left, right)
        elif isinstance(node, ast.Compare) and type(node.ops[0]) in self.OPERATORS:
            left = self._safe_eval(node.left, context)
            right = self._safe_eval(node.comparators[0], context)
            return self.OPERATORS[type(node.ops[0])](left, right)
        elif isinstance(node, ast.Name):
            return context[node.id]
        elif isinstance(node, ast.Constant):
            return node.value
        elif isinstance(node, ast.NameConstant):
            return node.value  # Support for boolean literals
        elif isinstance(node, ast.BoolOp) and type(node.op) in self.OPERATORS:
            values = [self._safe_eval(v, context) for v in node.values]
            return all(values) if isinstance(node.op, ast.And) else any(values)
        elif isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.Not):
            return not self._safe_eval(node.operand, context)  # Support for 'not'
        else:
            raise ValueError("Unsupported expression")

    def _evaluate_expression(self, expression, context):
        try:
            node = ast.parse(expression, mode="eval").body
            result = self._safe_eval(node, context)
            logger.debug(
                f"Evaluated expression: {expression} with context: {context} -> Result: {result}"
            )
            return result
        except Exception as e:
            logger.error(
                f"Failed to evaluate expression: {expression} with context: {context}. Error: {e}"
            )
            raise ValueError(f"Invalid expression: {e}")
