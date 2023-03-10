from pydantic import BaseModel


class SeedSchema(BaseModel):
    is_executed: bool = False
