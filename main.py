
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import crud, models, schemas, datetime
from database import get_db
from typing import List

app = FastAPI()

@app.post("/plans/", response_model=schemas.PlanCreate)
def create_plan(plan: schemas.PlanCreate, db: Session = Depends(get_db)):
    return crud.create_plan(db=db, plan=plan)

@app.get("/plans/all", response_model=List[schemas.PlanBase])
def get_plans(db: Session = Depends(get_db)):
    return crud.get_plans(db=db)

@app.get("/plans/{year}", response_model=List[schemas.PlanResponse])
def read_plans(year: int, db: Session = Depends(get_db)):
    return crud.get_all_plans_for_year(db, year)

@app.put("/plans/{plan_id}", response_model=schemas.PlanUpdate)
def update_plan_route(plan_id: int, plan_update: schemas.PlanUpdate, db: Session = Depends(get_db)):
    updated_plan = crud.update_plan(db, plan_id, plan_update)
    if not updated_plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    return updated_plan

@app.delete("/plans/{plan_id}", response_model=schemas.PlanUpdate)
def delete_plan_route(plan_id: int, db: Session = Depends(get_db)):
    deleted_plan = crud.delete_plan(db, plan_id)
    if not deleted_plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    return {"detail": "Plan deleted"}

# Production Endpoints
@app.post("/productions/", response_model=schemas.ProductionBase)
def create_production(production: schemas.ProductionBase, db: Session = Depends(get_db)):
    return crud.create_production(db=db, production=production)

@app.get("/productions/{production_id}", response_model=schemas.ProductionBase)
def get_production(production_id: int, db: Session = Depends(get_db)):
    production = crud.get_production(db=db, production_id=production_id)
    if production is None:
        raise HTTPException(status_code=404, detail="Production not found")
    return production

@app.get("/productions/", response_model=List[schemas.ProductionBase])
def get_all_productions(db: Session = Depends(get_db)):
    return crud.get_all_productions(db=db)

@app.get("/production/latest", response_model=schemas.ProductionBase)
def get_latest_production_data(db: Session = Depends(get_db)):
    return crud.get_latest_production(db)

# Inventory Management Endpoints
@app.post("/inventories/", response_model=schemas.InventoryManagementBase)
def create_inventory_management(inventory: schemas.InventoryManagementBase, db: Session = Depends(get_db)):
    return crud.create_inventory_management(db=db, inventory=inventory)

@app.get("/inventories/{inventory_id}", response_model=schemas.InventoryManagementBase)
def get_inventory(inventory_id: int, db: Session = Depends(get_db)):
    inventory = crud.get_inventory(db=db, inventory_id=inventory_id)
    if inventory is None:
        raise HTTPException(status_code=404, detail="Inventory not found")
    return inventory

@app.get("/inventories/", response_model=List[schemas.InventoryManagementBase])
def get_all_inventories(db: Session = Depends(get_db)):
    return crud.get_all_inventories(db=db)

@app.post("/materials/", response_model=schemas.MaterialBase)
def create_material(material: schemas.MaterialBase, db: Session = Depends(get_db)):
    return crud.create_materials(db=db, material=material)

@app.get("/materials/all", response_model=List[schemas.MaterialBase])
def get_materials(db: Session = Depends(get_db)):
    return crud.get_materials(db=db)

@app.put("/materials/{material_id}", response_model=schemas.MaterialUpdate)
def update_material_route(material_id: int, material_update: schemas.MaterialUpdate, db: Session = Depends(get_db)):
    updated_plan = crud.update_materials(db, material_id, material_update)
    if not updated_plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    return updated_plan

@app.delete("/materials/{material_id}", response_model=schemas.MaterialUpdate)
def delete_material_route(material_id: int, db: Session = Depends(get_db)):
    deleted_material = crud.delete_material(db, material_id)
    if not deleted_material:
        raise HTTPException(status_code=404, detail="Material not found")
    return {"detail": "Material deleted"}

@app.get("/materials/", response_model=List[schemas.MaterialResponse])
def read_material_performance(year: int, month: int, db: Session = Depends(get_db)):
    materials = crud.get_material_for_month(db, year, month)
    return materials