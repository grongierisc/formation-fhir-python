from jsonpath_ng import parse

def filter_resource_util(resource:dict, permissions:list) -> dict:
    for permission in permissions:
        # does the resource is the type of the permission
        if (hasattr(permission,"resource_type")
            and hasattr(permission,"json_path")
            and permission.json_path is not None
            and resource["resourceType"] == permission.resource_type):
            # remove the fields that are not in the permission
            resource = remove_fields(resource, permission.json_path)
    return resource

def remove_fields(resource:dict, json_path:str) -> dict:
    jsonpath_expr = parse(json_path)
    return jsonpath_expr.filter(lambda d: True,resource)