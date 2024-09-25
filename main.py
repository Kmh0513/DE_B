
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import crud, models, schemas, datetime
from database import get_db
from typing import List

app = FastAPI()

#plan 엔드포인트
@app.post("/plans/", response_model=schemas.PlanCreate)
def create_plan(plan: schemas.PlanCreate, db: Session = Depends(get_db)):
    return crud.create_plan(db, plan)

@app.get("/plans/all", response_model=List[schemas.PlanBase])
def get_plans(db: Session = Depends(get_db)):
    return crud.get_plans(db)

@app.get("/plans_rate/{year}", response_model=List[schemas.PlanResponse])
def read_plans(year: int, db: Session = Depends(get_db)):
    return crud.get_all_plans_for_year(db, year)

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

#production 엔드포인트
@app.post("/productions/", response_model=schemas.ProductionBase)
def create_production(production: schemas.ProductionBase, db: Session = Depends(get_db)):
    return crud.create_production(db, production)

@app.get("/productions/{production_id}", response_model=schemas.ProductionBase)
def get_production(production_id: int, db: Session = Depends(get_db)):
    production = crud.get_production(db, production_id)
    if production is None:
        raise HTTPException(status_code=404, detail="Production not found")
    return production.__dict__

@app.get("/productions/", response_model=List[schemas.ProductionBase])
def get_all_productions(db: Session = Depends(get_db)):
    return crud.get_all_productions(db)

@app.get("/production/{year},{month},{day}", response_model=List[schemas.ProductionBase])
def get_day_production_data(year: int, month: int, day: int, db: Session = Depends(get_db)):
    production = crud.get_day_production(db, year, month, day)
    if production is None:
        raise HTTPException(status_code=404, detail="Production not found")
    return production

#inventory 엔드포인트
@app.post("/inventories/{year}", response_model=schemas.InventoryManagementBase)
def create_inventory_management(inventory: schemas.InventoryManagementBase, db: Session = Depends(get_db)):
    return crud.create_inventory_management(db=db, inventory=inventory)

@app.get("/inventories/{inventory_id}", response_model=schemas.InventoryManagementBase)
def get_inventory(inventory_id: int, db: Session = Depends(get_db)):
    inventory = crud.get_inventory(db=db, inventory_id=inventory_id)
    if inventory is None:
        raise HTTPException(status_code=404, detail="Inventory not found")
    return inventory.__dict__

@app.get("/inventories/", response_model=List[schemas.InventoryManagementBase])
def get_all_inventories(db: Session = Depends(get_db)):
    return crud.get_all_inventories(db=db)

#material 엔드포인트
@app.post("/materials/", response_model=schemas.MaterialBase)
def create_material(material: schemas.MaterialBase, db: Session = Depends(get_db)):
    return crud.create_materials(db=db, material=material)

@app.get("/materials/all", response_model=List[schemas.MaterialBase])
def get_materials(db: Session = Depends(get_db)):
    return crud.get_materials(db=db)

@app.put("/materials/{material_id}", response_model=schemas.MaterialUpdate)
def update_material_route(material_id: int, material_update: schemas.MaterialUpdate, db: Session = Depends(get_db)):
    updated_plan = crud.update_material(db, material_id, material_update)
    if not updated_plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    return updated_plan

@app.delete("/materials/{material_id}")
def delete_material_route(material_id: int, db: Session = Depends(get_db)):
    deleted_material = crud.delete_material(db, material_id)
    if not deleted_material:
        raise HTTPException(status_code=404, detail="Material not found")
    return {"detail": "Material deleted"}

@app.get("/materials/", response_model=List[schemas.MaterialResponse])
def read_material_performance(year: int, month: int, db: Session = Depends(get_db)):
    materials = crud.get_material_for_month(db, year, month)
    return materials

@app.get("/material_invens/", response_model=List[schemas.MaterialInvenBase])
def get_all_materialsinven(db: Session = Depends(get_db)):
    return crud.get_all_material_invens(db=db)