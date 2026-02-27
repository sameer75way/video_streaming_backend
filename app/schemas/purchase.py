from pydantic import BaseModel


class PurchaseResponse(BaseModel):
    message: str