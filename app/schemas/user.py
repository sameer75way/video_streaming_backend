from pydantic import BaseModel


class UserResponse(BaseModel):
    id: int
    email: str
    role: str

class RoleUpdate(BaseModel):
    role_name: str