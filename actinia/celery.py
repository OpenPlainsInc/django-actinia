# ###############################################################################
# # Filename: celery.py                                                          #
# # Project: TomorrowNow                                                         #
# # File Created: Monday March 28th 2022                                         #
# # Author: Corey White (smortopahri@gmail.com)                                  #
# # Maintainer: Corey White                                                      #
# # -----                                                                        #
# # Last Modified: Mon Mar 28 2022                                               #
# # Modified By: Corey White                                                     #
# # -----                                                                        #
# # License: GPLv3                                                               #
# #                                                                              #
# # Copyright (c) 2023 OpenPlains Inc.                                               #
# #                                                                              #
# # TomorrowNow is an open-source geospatial participartory modeling platform    #
# # to enable stakeholder engagment in socio-environmental decision-makeing.     #
# #                                                                              #
# # This program is free software: you can redistribute it and/or modify         #
# # it under the terms of the GNU General Public License as published by         #
# # the Free Software Foundation, either version 3 of the License, or            #
# # (at your option) any later version.                                          #
# #                                                                              #
# # This program is distributed in the hope that it will be useful,              #
# # but WITHOUT ANY WARRANTY; without even the implied warranty of               #
# # MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the                #
# # GNU General Public License for more details.                                 #
# #                                                                              #
# # You should have received a copy of the GNU General Public License            #
# # along with this program.  If not, see <https://www.gnu.org/licenses/>.       #
# #                                                                              #
# ###############################################################################

# # Used this blog post to get started
# # https://www.caktusgroup.com/blog/2021/08/11/using-celery-scheduling-tasks/
# import os
# from celery import Celery

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'test_settings')

# # Create default Celery app
# app = Celery('api')

# # namespace='CELERY' means all celery-related configuration keys
# # should be uppercased and have a `CELERY_` prefix in Django settings.
# # https://docs.celeryproject.org/en/stable/userguide/configuration.html
# app.config_from_object("django.conf:settings", namespace="CELERY")

# # When we use the following in Django, it loads all the <appname>.tasks
# # files and registers any tasks it finds in them. We can import the
# # tasks files some other way if we prefer.
# app.autodiscover_tasks()
