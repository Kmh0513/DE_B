from sqlalchemy.orm import Session
from models import Plan, Production, InventoryManagement
import schemas
from sqlalchemy import func, desc
from typing import List
from datetime import datetime, timedelta

# Plan CRUD
def create_plan(db: Session, plan: schemas.PlanBase):
    db_plan = Plan(
        year=plan.year,
        month=plan.month,
        item_name=plan.item_name,
        plan_quantity=plan.plan_quantity,
        account_idx = plan.account_idx
    )
    db.add(db_plan)
    db.commit()
    db.refresh(db_plan)
    return db_plan

def get_plans(db: Session):
    return db.query(Plan).all()
def get_date_range(year: int, month: int):
    start_date = datetime(year, month, 1)
    end_date = (start_date + timedelta(days=31)).replace(day=1) - timedelta(days=1)
    return start_date, end_date

def get_all_plans(db: Session, year: int, month: int) -> schemas.PlanResponse:
    start_date, end_date = get_date_range(year, month)
    total_plan_quantity = db.query(Plan).filter(Plan.year == year, Plan.month == month).with_entities(func.sum(Plan.plan_quantity)).scalar() or 0
    total_business_plan = db.query(func.sum(Plan.plan_quantity * Production.price)).join(Production, Plan.item_name == Production.item_name).filter(Plan.year == year, Plan.month == month).scalar() or 0

    total_production_quantity = db.query(func.sum(Production.production_quantity)).filter(Production.date.between(start_date.date(), end_date.date())).scalar() or 0
    total_business_actual = db.query(func.sum(Production.production_quantity * Production.price)).filter(Production.date.between(start_date.date(), end_date.date())).scalar() or 0

    production_achievement_rate = (total_production_quantity / total_plan_quantity) * 100 if total_plan_quantity > 0 else 0
    business_achievement_rate = (total_business_actual / total_business_plan) * 100 if total_business_plan > 0 else 0

    return schemas.PlanResponse(
        total_plan_quantity=total_plan_quantity,
        total_business_plan=total_business_plan,
        total_production_quantity=total_production_quantity,
        total_business_actual=total_business_actual,
        production_achievement_rate=production_achievement_rate,
        business_achievement_rate=business_achievement_rate,
        year=year,
        month=month
    )

# Production CRUD
def create_production(db: Session, production: schemas.ProductionBase):
    db_production = Production(
        date=production.date,
        item_id=production.item_id,
        item_name=production.item_name,
        category=production.category,
        price=production.price,
        standard=production.standard,
        module_name=production.module_name,
        line=production.line,
        worker_name=production.worker_name,
        module_time=production.module_time,
        working_time=production.working_time,
        production_quantity=production.production_quantity,
        bad_production=production.bad_production,
        bad_production_type=production.bad_production_type,
        punching_quantity=production.punching_quantity,
        not_module_time=production.not_module_time,
        account_idx=production.account_idx
    )
    db.add(db_production)
    db.commit()
    db.refresh(db_production)
    return db_production

def get_production(db: Session, production_id: int):
    return db.query(Production).filter(Production.id == production_id).first()

def get_all_productions(db: Session):
    return db.query(Production).all()

def get_latest_production(db: Session):
    return db.query(Production).order_by(desc(Production.date)).first()

# InventoryManagement CRUD
def create_inventory_management(db: Session, inventory: schemas.InventoryManagementBase):
    db_inventory = InventoryManagement(
        date=inventory.date,
        item_id=inventory.item_id,
        item_name=inventory.item_name,
        category=inventory.category,
        price=inventory.price,
        standard=inventory.standard,
        basic_quantity=inventory.basic_quantity,
        quantity_received=inventory.quantity_received,
        defective_quantity_received=inventory.defective_quantity_received,
        quantity_shipped=inventory.quantity_shipped,
        current_stock=inventory.current_stock,
        current_LOT_stock=inventory.current_LOT_stock,
        account_idx=inventory.account_idx
    )
    db.add(db_inventory)
    db.commit()
    db.refresh(db_inventory)
    return db_inventory

def get_inventory(db: Session, inventory_id: int):
    return db.query(InventoryManagement).filter(InventoryManagement.id == inventory_id).first()

def get_all_inventories(db: Session):
    return db.query(InventoryManagement).all()