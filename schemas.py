from pydantic import BaseModel
from typing import Optional
from datetime import date, time

class PlanBase(BaseModel):
    year: int
    month: int
    item_number: int
    item_name: str
    inventory: int
    model: str
    price: float
    account_idx: int = 1

class ProductionBase(BaseModel):
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

class PlanResponse(BaseModel):
    year: int
    month: int
    prod_plan: int
    business_plan: float
    prod_amount: int
    business_amount: float
    production_achievement_rate: float
    business_achievement_rate: float