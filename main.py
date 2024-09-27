
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import crud, schemas
from database import get_db
from typing import List
import datetime

app = FastAPI()
@app.get("/")
def root():
    return None

#plan 엔드포인트
@app.post("/plans/", response_model=schemas.PlanCreate)
def create_plan(plan: schemas.PlanCreate, db: Session = Depends(get_db)):
    return crud.create_plan(db, plan)

@app.get("/plans/all/", response_model=List[schemas.PlanBase])
def get_all_plans(db: Session = Depends(get_db)):
    return crud.get_all_plans(db)

@app.get("/plans/rate/{year}", response_model=List[schemas.PlanResponse])
def get_plans_rate(year: int, db: Session = Depends(get_db)):
    return crud.get_plans_rate_for_year(db, year)

@app.put("/plans/{plan_id}", response_model=schemas.PlanUpdate)
def update_plan_route(plan_id: int, plan_update: schemas.PlanUpdate, db: Session = Depends(get_db)):
    updated_plan = crud.update_plan(db, plan_id, plan_update)
    if not updated_plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    return updated_plan

@app.delete("/plans/{plan_id}")
def delete_plan_route(plan_id: int, db: Session = Depends(get_db)):
    deleted_plan = crud.delete_plan(db, plan_id)
    if not deleted_plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    return {"detail": "Plan deleted"}

@app.get("/plans/rates/{year},{month}", response_model=List[schemas.PlanResponse2])
def get_plan_rate_month(year: int, month: int, db: Session = Depends(get_db)):
    plans = crud.get_plan_rate_for_month(db, year, month)
    return plans

#production 엔드포인트
@app.post("/productions/", response_model=schemas.ProductionCreate)
def create_production(production: schemas.ProductionCreate, db: Session = Depends(get_db)):
    return crud.create_production(db, production)

@app.get("/productions/all/", response_model=List[schemas.ProductionBase])
def get_all_productions(db: Session = Depends(get_db)):
    return crud.get_all_productions(db)

@app.get("/productions/day/{date}", response_model=List[schemas.ProductionBase])
def get_day_production_data(date: datetime.date,  db: Session = Depends(get_db)):
    production = crud.get_day_production(db, date)
    if production is None:
        raise HTTPException(status_code=404, detail="Production not found")
    return production

@app.get("/productions/days/", response_model=List[schemas.ProductionBase])
def get_days_production_data(start_date: datetime.date, end_date: datetime.date, operator: str=None, item_number: str=None, item_name: str=None, db: Session = Depends(get_db)):
    production = crud.get_days_production(db, start_date, end_date, operator, item_number, item_name)
    if production is None:
        raise HTTPException(status_code=404, detail="Production not found")
    return production

@app.get("/productions/{production_id}", response_model=schemas.ProductionBase)
def get_production(production_id: int, db: Session = Depends(get_db)):
    production = crud.get_production(db, production_id)
    if production is None:
        raise HTTPException(status_code=404, detail="Production not found")
    return production.__dict__

#inventory 엔드포인트
@app.post("/inventories/", response_model=schemas.InventoryManagementCreate)
def create_inventory_management(inventory: schemas.InventoryManagementCreate, db: Session = Depends(get_db)):
    return crud.create_inventory_management(db=db, inventory=inventory)

@app.get("/inventories/all/", response_model=List[schemas.InventoryManagementBase])
def get_all_inventories(db: Session = Depends(get_db)):
    return crud.get_all_inventories(db=db)

@app.get("/inventories/{inventory_id}", response_model=schemas.InventoryManagementBase)
def get_inventory(inventory_id: int, db: Session = Depends(get_db)):
    inventory = crud.get_inventory(db=db, inventory_id=inventory_id)
    if inventory is None:
        raise HTTPException(status_code=404, detail="Inventory not found")
    return inventory.__dict__

#material 엔드포인트
@app.post("/materials/", response_model=schemas.MaterialCreate)
def create_material(material: schemas.MaterialCreate, db: Session = Depends(get_db)):
    return crud.create_materials(db=db, material=material)

@app.get("/materials/all/", response_model=List[schemas.MaterialBase])
def get_all_materials(db: Session = Depends(get_db)):
    return crud.get_all_materials(db=db)

@app.get("/material/rate/{year}", response_model=List[schemas.MaterialResponse2])
def get_material_rate(year: int, db: Session = Depends(get_db)):
    return crud.get_material_rate_for_year(db, year)

@app.get("/materials/rates/{year},{month}", response_model=List[schemas.MaterialResponse])
def get_material_rate(year: int, month: int, db: Session = Depends(get_db)):
    materials = crud.get_material_rate_for_month(db, year, month)
    return materials

@app.put("/materials/{material_id}", response_model=schemas.MaterialUpdate)
def update_material_route(material_id: int, material_update: schemas.MaterialUpdate, db: Session = Depends(get_db)):
    updated_plan = crud.update_material(db, material_id, material_update)
    if not updated_plan:
        raise HTTPException(status_code=404, detail="Material not found")
    return updated_plan

@app.delete("/materials/{material_id}")
def delete_material_route(material_id: int, db: Session = Depends(get_db)):
    deleted_material = crud.delete_material(db, material_id)
    if not deleted_material:
        raise HTTPException(status_code=404, detail="Material not found")
    return {"detail": "Material deleted"}

@app.get("/material_invens/all/", response_model=List[schemas.MaterialInvenCreate])
def get_all_materialsinven(db: Session = Depends(get_db)):
    return crud.get_all_material_invens(db=db)