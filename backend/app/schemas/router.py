from pydantic import BaseModel


class RouterResponse(BaseModel):
    skill: str