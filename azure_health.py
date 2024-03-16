from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.compute import ComputeManagementClient
import json
# todo: import for each azure.mgmt. type

# 
def get_status(compute_client, resource_group, resoure_name, resource_type):
    # todo: get status of other resource types

    if resource_type == 'Microsoft.Compute/virtualMachines':
        # Getting the status of a virtual machine
        vm_instance_view = compute_client.virtual_machines.instance_view(resource_group, resoure_name)
        statuses = vm_instance_view.statuses
        for status in statuses:
            if status.code.startswith('PowerState/'):
                return status.code
        return 'Unknown'

def list_resources(subscription_id, resource_group_name):
    credential = DefaultAzureCredential()
    resource_client = ResourceManagementClient(credential, subscription_id)
    compute_client = ComputeManagementClient(credential, subscription_id)

    resource_list = []
    for resource in resource_client.resources.list_by_resource_group(resource_group_name):
        # todo: map resource types to friendly names
        resource_info = {
            'name': resource.name,
            'type': resource.type,
        }

        # Check if the resource is a VM to get its status
        if resource.type == 'Microsoft.Compute/virtualMachines':
            resource_info['status'] = get_status(compute_client, resource_group_name, resource.name, resource.type)
        # todo: add more resource types statuses
        else:
            resource_info['status'] = 'Status Not Available'

        resource_list.append(resource_info)

    return json.dumps(resource_list, indent=2)

subscription_id = "eeeee5b2-666a-4f32-bb9f-4d548cd027db"
resource_group_name = "azurestorage"

print(list_resources(subscription_id, resource_group_name))