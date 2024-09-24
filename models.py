from sqlalchemy import Column, Integer, String, Date, Time, Float
from database import Base

class Plan(Base):
    __tablename__ = "plans"

    id = Column(Integer, primary_key=True, index=True)
    year = Column(Integer)
    month = Column(Integer)
    item_number = Column(Integer)
    item_name = Column(String(100))
    inventory = Column(Integer)
    model = Column(String(100))
    price = Column(Float)
    account_idx = Column(Integer)


class Production(Base):
    __tablename__ = "productions"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date)
    line = Column(String)
    operator = Column(String(100))
    item_number = Column(Integer)
    item_name = Column(String(100))
    model = Column(String(100))
    target_quantity = Column(Integer)
    produced_quantity = Column(Integer)
    production_efficiency = Column(Integer)
    equipment = Column(String(100))
    operating_time = Column(Time)
    non_operating_time = Column(Time)
    shift = Column(String(100))
    equipment_efficiency = Column(Integer)
    specification = Column(String(100))
    account_idx = Column(Integer)

class InventoryManagement(Base):
    __tablename__ = "inventory_managements"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date)
    item_number = Column(Integer)
    item_name = Column(String(100))
    price = Column(Float)
    basic_quantity = Column(Integer)
    basic_amount = Column(Float)
    in_quantity = Column(Integer)
    in_amount = Column(Float)
    defective_in_quantity = Column(Integer)
    defective_in_amount = Column(Float)
    out_quantity = Column(Integer)
    out_amount = Column(Float)
    adjustment_quantity = Column(Integer)
    current_quantity = Column(Integer)
    current_amount = Column(Float)
    lot_current_quantity = Column(Integer)
    difference_quantity = Column(Integer)
    account_idx = Column(Integer)

class Material(Base):
    __tablename__ = "materials"

    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Date)
    client = Column(String(100))
    item_number = Column(Integer)
    item_name = Column(String(100))
    item_category = Column(String(100))
    model = Column(String(100))
    process = Column(String(100))
    quantity = Column(Integer)
    account_idx = Column(Integer)