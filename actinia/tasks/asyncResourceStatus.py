from celery import shared_task
import actinia.utils as acp

# from actinia import *
import requests
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


@shared_task()
def asyncResourceStatus(user_id, resource_id):
    """
    Poll actinia api to check on status of process chain resource.

    Parameters
    ----------
    user_id : string
        The requesting user's id
    resource_id: string
        The id of the actinia resource.

    Returns:
        Any: _description_
    """

    # Make request to actinia to check resource status
    url = f"{acp.baseUrl()}/resources/{user_id}/{resource_id}"
    r = requests.get(url, auth=acp.auth())
    data = r.json()
    if r.status_code == 200:
        channel_layer = get_channel_layer()
        resource_name = resource_id.replace("-", "_")
        updated_status = data["status"]
        resources = data["urls"]["resources"]
        process_log = []
        if data.get("process_log") is not None:
            process_log = data["process_log"]

        resource_group = f"actinia_{resource_name}"

        # Response with message back to to consumer
        response_message = {
            "type": "resource_message",
            "message": updated_status,
            "resource_id": resource_id,
            "resources": resources,
            "process_log": process_log,
        }

        return async_to_sync(channel_layer.group_send)(resource_group, response_message)
