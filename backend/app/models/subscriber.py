from typing import List, Optional

from pydantic import BaseModel, Field, EmailStr
from bson import ObjectId

from models.dbmodel import DBModelMixin, PyObjectId
from models.rwmodel import RWModel


class SubscriberModel(RWModel):
    name: Optional[str]
    email: EmailStr
    state: Optional[str]
    district: Optional[str]
    district_id: Optional[int]
    zip_code: Optional[int]
    vaccine_doze: Optional[List[int]] = [1, 2]
    is_subscribed: bool = True


class SubscriberInDB(SubscriberModel, DBModelMixin):
    pass
    # id : PyObjectId = Field(default_factory=PyObjectId, alias="_id")
