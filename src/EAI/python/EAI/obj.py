from dataclasses import dataclass

@dataclass
class PermissionObj:
    resource_type: str
    json_path: str = None
    query: str = None
    security: list = None