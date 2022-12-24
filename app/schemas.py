""" schema to enforce the data sent from frontend
in this case we use pydantic which also validates the data
example: title cannot be empty which will checked by pydantic
in this case published can be empty coz it has a default value """

from pydantic import BaseModel

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass