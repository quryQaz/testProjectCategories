from pydantic import BaseModel, ConfigDict
from typing import Optional  

class CategorySchema(BaseModel):
    id: int
    name: str
    parent_id: Optional[int]

    model_config = ConfigDict(from_attributes=True)
