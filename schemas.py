from pydantic import BaseModel
from typing import Optional
from datetime import date, time

class PlanCreate(BaseModel):
    year: int
    month: int
    item_number: int
    item_name: str
    inventory: int
    model: str
    price: float
    account_idx: int = 1

class PlanBase(BaseModel):
    id: int
    year: int
    month: int
    item_number: int
    item_name: str
    inventory: int
    model: str
    price: float
    account_idx: int = 1

class PlanUpdate(BaseModel):
    year: Optional[int] = None
    month: Optional[int] = None
    itme_number: Optional[int] = None
    item_name: Optional[str] = None
    inventory: Optional[int] = None
    model: Optional[str] = None
    price: Optional[float] = None
    
    class Config:
        orm_mode = True

class ProductionBase(BaseModel):
    id: int
    date: date
    line: Optional[str] = None
    operator: Optional[str] = None
    item_number: int
    item_name: str
    model: str
    target_quantity: int
    produced_quantity: int
    production_efficiency: int
    equipment: str
    operating_time: time
    non_operating_time: time
    shift: str
    equipment_efficiency: int
    specification: str
    account_idx: int = 1

class InventoryManagementBase(BaseModel):
    id: int
    date: date
    item_number: int
    item_name: str
    price: float
    basic_quantity: int
    basic_amount: float
    in_quantity: int
    in_amount: float
    defective_in_quantity: int
    defective_in_amount: float
    out_quantity: int
    out_amount: float
    adjustment_quantity: int
    current_quantity: int
    current_amount: float
    lot_current_quantity: int
    difference_quantity: int
    account_idx: int = 1

class MaterialBase(BaseModel):
    id: int
    date: date
    client: str
    item_number: int
    item_name: str
    item_category: str
    model: str
    process: str
    quantity: int
    account_idx: int = 1

class PlanResponse(BaseModel):
    year: int
    month: int
    prod_plan: float
    business_plan: float
    prod_amount: float
    business_amount: float
    production_achievement_rate: float
    business_achievement_rate: float

class MaterialResponse(BaseModel):
    year: int
    month: int
    client: str
    previous_amount: float
    current_amount: float
    growth_rate: Optional[float] = None

class MaterialUpdate(BaseModel):
    client: Optional[str] = None
    item_number: Optional[int] = None
    item_name: Optional[str] = None
    item_category: Optional[str] = None
    model: Optional[str] = None
    process: Optional[str] = None
    quantity: Optional[int] = None
    
    class Config:
        orm_mode = True

class MaterialInvenBase(BaseModel):
    date: date
    item_number: int
    item_name: str
    price: float
    item_category: str
    process: str
    client: str
    model: str
    overall_status_quantity: int
    overall_status_amount: float
    account_idx: int = 1