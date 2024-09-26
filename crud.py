from sqlalchemy.orm import Session
from models import Plan, Production, InventoryManagement, Material, MaterialInven
import schemas
from sqlalchemy import func, desc
from typing import List
from datetime import datetime, timedelta

#기간 계산 함수
def get_month_range(year: int, month: int):
    start_date = datetime(year, month, 1)
    end_date = (start_date + timedelta(days=31)).replace(day=1) - timedelta(days=1)
    return start_date, end_date

#plan CRUD
def create_plan(db: Session, plan: schemas.PlanCreate):
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
    return db_plan.__dict__

#plan전체
def get_all_plans(db: Session):
    plan_get=db.query(Plan).all()
    return [plan.__dict__ for plan in plan_get]

#연도별 plan rate 데이터
def get_plans_rate_for_year(db: Session, year: int) -> List[schemas.PlanResponse]:
    plans_for_year = []

    for month in range(1, 13):
        start_date, end_date = get_month_range(year, month)

        prod_plan = db.query(func.sum(Plan.inventory)).filter(Plan.year == year, Plan.month == month).scalar() or 0
        business_plan = db.query(func.sum(Plan.inventory * Plan.price)).filter(Plan.year == year, Plan.month == month).scalar() or 0

        prod_amount = db.query(func.sum(Production.produced_quantity)).filter(Production.date.between(start_date.date(), end_date.date())).scalar() or 0
        business_amount = db.query(func.sum(Production.produced_quantity * Plan.price))\
            .select_from(Production)\
            .join(Plan, Plan.item_name == Production.item_name)\
            .filter(Production.date.between(start_date.date(), end_date.date()))\
            .scalar() or 0

        production_achievement_rate = round((prod_amount / prod_plan) * 100 if prod_plan > 0 else 0, 2)
        business_achievement_rate = round((business_amount / business_plan) * 100 if business_plan > 0 else 0, 2)

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

#production CRUD
def create_production(db: Session, production: schemas.ProductionCreate):
    db_production = Production(
        date=production.date,
        line=production.line,
        operator=production.operator,
        item_number=production.item_number,
        item_name=production.item_name,
        model=production.model,
        target_quantity=production.target_quantity,
        produced_quantity=production.produced_quantity,
        production_efficiency=production.production_efficiency,
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
    return db_production.__dict__

def get_production(db: Session, production_id: int):
    production_get = db.query(Production).filter(Production.id == production_id).first()
    return  production_get

#production전체
def get_all_productions(db: Session):
    production_get = db.query(Production).all()
    return [production.__dict__ for production in production_get]

def get_days_production(db: Session, start_date: datetime.date, end_date: datetime.date, operator: str , item_number: int , item_name: str):
    querys = db.query(Production).filter(Production.date.between(start_date, end_date))
    if operator:
        querys = querys.filter(Production.operator == operator)
    if item_number:
        querys = querys.filter(Production.item_number == item_number)
    if item_name:
        querys = querys.filter(Production.item_name == item_name)
    
    production_get = querys.order_by(desc(Production.id)).all()
    return [production.__dict__ for production in production_get]

#특정날짜 production반환
def get_day_production(db: Session, date: datetime.date):
    production_get = db.query(Production).filter(Production.date == date).order_by(desc(Production.id)).limit(20).all()
    return [production.__dict__ for production in production_get]

#inventory_management CRUD
def create_inventory_management(db: Session, inventory: schemas.InventoryManagementCreate):
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
    return db_inventory.__dict__

def get_inventory(db: Session, inventory_id: int):
    inventory_get = db.query(InventoryManagement).filter(InventoryManagement.id == inventory_id).first()
    return  inventory_get
    
#inventory전체
def get_all_inventories(db: Session):
    inventory_get = db.query(InventoryManagement).all()
    return [inventory.__dict__ for inventory in inventory_get]

#material CRUD
def create_materials(db: Session, material: schemas.MaterialCreate):
    db_material = Material(
        date=material.date,
        client=material.client,
        item_number=material.item_number,
        item_name=material.item_name,
        item_category=material.item_category,
        model=material.model,
        process=material.process,
        quantity=material.quantity,
        account_idx=material.account_idx
    )
    db.add(db_material)
    db.commit()
    db.refresh(db_material)
    return db_material.__dict__

#material 전체
def get_all_materials(db: Session):
    material_get = db.query(Material).all()
    return [material.__dict__ for material in material_get]

def update_material(db: Session, material_id: int, material_update: schemas.MaterialUpdate):
    material = db.query(Material).filter(Material.id == material_id).first()
    
    if not material:
        return None  
    
    for var, value in vars(material_update).items():
        setattr(material, var, value)  
        
    db.commit()
    db.refresh(material)  
    return material

def delete_material(db: Session, material_id: int):
    material = db.query(Material).filter(Material.id == material_id).first()
    
    if not material:
        return None
    
    db.delete(material)
    db.commit()
    return material

#월별 material 상승률
def get_material_rate_for_month(db: Session, year: int, month: int):

    current_start_date = datetime(year, month, 1)
    next_month = month % 12 + 1
    current_end_date = datetime(year, next_month, 1) - timedelta(days=1)

    previous_month = (month - 1) or 12
    previous_year = year - 1 if month == 1 else year
    previous_start_date = datetime(previous_year, previous_month, 1)
    previous_end_date = datetime(year, month, 1) - timedelta(days=1)

    current_data = db.query(func.sum(Material.quantity*MaterialInven.price).label("current_amount"), Material.client)\
        .select_from(MaterialInven)\
        .join(Material, Material.item_name == MaterialInven.item_name)\
        .filter(Material.date >= current_start_date, Material.date <= current_end_date)\
        .group_by(Material.client).all()

    previous_data = db.query(func.sum(Material.quantity*MaterialInven.price).label("previous_amount"), Material.client)\
        .select_from(MaterialInven)\
        .join(Material, Material.item_name == MaterialInven.item_name)\
        .filter(Material.date >= previous_start_date, Material.date <= previous_end_date)\
        .group_by(Material.client).all()

    previous_map = {data.client: data.previous_amount for data in previous_data}

    results = []
    for current in current_data:
        previous_amount = previous_map.get(current.client, 0)
        growth_rate = ((current.current_amount - previous_amount) / previous_amount * 100) if previous_amount else 0

        result = schemas.MaterialResponse(
            year=year,
            month=month,
            client=current.client,
            previous_amount=previous_amount,
            current_amount=current.current_amount,
            growth_rate=growth_rate
        )
        results.append(result)
    
    return results

#material_inven 전체
def get_all_material_invens(db: Session):
    material_get = db.query(MaterialInven).all()
    return [material.__dict__ for material in material_get]