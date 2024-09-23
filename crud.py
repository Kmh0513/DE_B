from sqlalchemy.orm import Session
from models import Plan, Production, InventoryManagement
import schemas
from sqlalchemy import func, desc
from typing import List
from datetime import datetime, timedelta
# 기간 계산 함수
def get_date_range(year: int, month: int):
    start_date = datetime(year, month, 1)
    end_date = (start_date + timedelta(days=31)).replace(day=1) - timedelta(days=1)
    return start_date, end_date
# Plan CRUD
def create_plan(db: Session, plan: schemas.PlanBase):
    db_plan = Plan(
        year=plan.year,
        month=plan.month,
        item_number=plan.item_number,
        item_name=plan.item_name,
        inventory=plan.inventory,
        model=plan.model,
        price=plan.price,
        account_idx = plan.account_idx
    )
    db.add(db_plan)
    db.commit()
    db.refresh(db_plan)
    return db_plan
# plans전체
def get_plans(db: Session):
    return db.query(Plan).all()
# 연도별 plans 따른 데이터
def get_all_plans_for_year(db: Session, year: int) -> List[schemas.PlanResponse]:
    plans_for_year = []

    # 1월부터 12월까지 각 월의 데이터를 계산
    for month in range(1, 13):
        start_date, end_date = get_date_range(year, month)

        # 월별 계획된 생산량과 사업 계획
        prod_plan = db.query(func.sum(Plan.inventory)).filter(Plan.year == year, Plan.month == month).scalar() or 0
        business_plan = db.query(func.sum(Plan.inventory * Plan.price)).filter(Plan.year == year, Plan.month == month).scalar() or 0

        # 월별 실제 생산량 및 사업 실적
        prod_amount = db.query(func.sum(Production.produced_quantity)).filter(Production.date.between(start_date.date(), end_date.date())).scalar() or 0
        business_amount = db.query(func.sum(Production.produced_quantity * Plan.price))\
            .select_from(Production)\
            .join(Plan, Plan.item_name == Production.item_name)\
            .filter(Production.date.between(start_date.date(), end_date.date()))\
            .scalar() or 0

        # 생산 달성률 및 사업 달성률 계산
        production_achievement_rate = round((prod_amount / prod_plan) * 100 if prod_plan > 0 else 0, 2)
        business_achievement_rate = round((business_amount / business_plan) * 100 if business_plan > 0 else 0, 2)

        # 해당 월의 데이터 저장
        monthly_plan = schemas.PlanResponse(
            year=year,
            month=month,
            prod_plan=prod_plan,
            business_plan=business_plan,
            prod_amount=prod_amount,
            business_amount=business_amount,
            production_achievement_rate=production_achievement_rate,
            business_achievement_rate=business_achievement_rate
        )

        plans_for_year.append(monthly_plan)

    return plans_for_year

#plan update
def update_plan(db: Session, plan_id: int, plan_update: schemas.PlanUpdate):
    plan = db.query(Plan).filter(Plan.id == plan_id).first()
    
    if not plan:
        return None  
    
    for var, value in vars(plan_update).items():
        setattr(plan, var, value)  
        
    db.commit()
    db.refresh(plan)  
    return plan

def delete_plan(db: Session, plan_id: int):
    plan = db.query(Plan).filter(Plan.id == plan_id).first()
    
    if not plan:
        return None
    
    db.delete(plan)
    db.commit()
    return plan

# Production CRUD
def create_production(db: Session, production: schemas.ProductionBase):
    db_production = Production(
        date=production.date,
        line=production.line,
        operator=production.operator,
        item_number=production.item_number,
        item_name=production.item_name,
        model=production.model,
        target_quantity=production.target_quantity,
        produced_quantity=production.produced_quantity,
        bad_production_type=production.production_efficiency,
        equipment=production.equipment,
        operating_time=production.operating_time,
        non_operating_time=production.non_operating_time,
        shift=production.shift,
        equipment_efficiency=production.equipment_efficiency,
        specification=production.specification,
        account_idx=production.account_idx
    )
    db.add(db_production)
    db.commit()
    db.refresh(db_production)
    return db_production

def get_production(db: Session, production_id: int):
    return db.query(Production).filter(Production.id == production_id).first()
#productions전체
def get_all_productions(db: Session):
    return db.query(Production).all()
#가장 최근 production반환
def get_latest_production(db: Session):
    return db.query(Production).order_by(desc(Production.date)).first()

# InventoryManagement CRUD
def create_inventory_management(db: Session, inventory: schemas.InventoryManagementBase):
    db_inventory = InventoryManagement(
        date=inventory.date,
        item_number=inventory.item_number,
        item_name=inventory.item_name,
        price=inventory.price,
        basic_quantity=inventory.basic_quantity,
        basic_amount=inventory.basic_amount,
        in_quantity=inventory.in_quantity,
        in_amount=inventory.in_amount,
        defective_in_quantity=inventory.defective_in_quantity,
        defective_in_amount=inventory.defective_in_amount,
        out_quantity=inventory.out_quantity,
        out_amount=inventory.out_amount,
        adjustment_quantity=inventory.adjustment_quantity,
        current_quantity=inventory.current_quantity,
        current_amount=inventory.current_amount,
        lot_current_quantity=inventory.lot_current_quantity,
        difference_quantity=inventory.difference_quantity,
        account_idx=inventory.account_idx
    )
    db.add(db_inventory)
    db.commit()
    db.refresh(db_inventory)
    return db_inventory

def get_inventory(db: Session, inventory_id: int):
    return db.query(InventoryManagement).filter(InventoryManagement.id == inventory_id).first()
#inventories전체
def get_all_inventories(db: Session):
    return db.query(InventoryManagement).all()