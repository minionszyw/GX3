from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class BillingRecordBase(BaseModel):
    change_amount: int
    description: str

class BillingRecordCreate(BillingRecordBase):
    user_id: int
    balance_after: int

class BillingRecordUpdate(BillingRecordBase):
    pass

class BillingRecordInDBBase(BillingRecordBase):
    id: int
    user_id: int
    balance_after: int
    created_at: datetime

    class Config:
        orm_mode = True

class BillingRecord(BillingRecordInDBBase):
    pass