import random
import time as t
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from models import Production, InventoryManagement,  MaterialInven
from schemas import ProductionCreate, InventoryManagementCreate, MaterialInvenCreate
from database import SessionLocal
from get_companies_list import company_names


#production generate
def generate_random_production_data():
    number = random.randint(1, 10)
    date=datetime.now().date()
    line=f"Line{random.randint(1, 10)}"
    operator=f"Operator{random.randint(1, 10)}"
    item_number = f"Item_Number{number}"
    item_name = f"Item{number}"
    target_quantity = random.randint(200, 500)
    produced_quantity = random.randint(1, target_quantity) 
    production_efficiency = (produced_quantity / target_quantity) * 100
    process = random.choice(["검사/조립", "사출"])
    operating_time = timedelta(hours=random.randint(0, 23), minutes=random.randint(0, 59))
    non_operating_time = timedelta(hours=random.randint(0, 23), minutes=random.randint(0, 59))
    shift=f"Shift{random.randint(1, 3)}"
    total_time = operating_time + non_operating_time
    line_efficiency = (operating_time.total_seconds() / total_time.total_seconds()) * 100 if total_time.total_seconds() > 0 else 0    
    model = random.choice(['가전', '건조기', '세탁기', '식기세척기', '에어컨', '중장비', '포장박스', 'LX2PE', 'GEN3.5', 'MX5'])
    specification=f"Specification{random.randint(1, 5)}"

    return ProductionCreate(
        date=date,
        line=line,
        operator=operator,
        item_number=item_number,
        item_name=item_name,
        model=model,
        target_quantity=target_quantity,
        produced_quantity=produced_quantity,
        production_efficiency=int(production_efficiency),
        process=process,
        operating_time=(datetime.min + operating_time).time(),  
        non_operating_time=(datetime.min + non_operating_time).time(),  
        shift=shift,
        line_efficiency=int(line_efficiency),
        specification=specification
    )

def insert_production_data(db: Session, production_data: ProductionCreate):
    db_production = Production(
        date=production_data.date,
        line=production_data.line,
        operator=production_data.operator,
        item_number=production_data.item_number,
        item_name=production_data.item_name,
        model=production_data.model,
        target_quantity=production_data.target_quantity,
        produced_quantity=production_data.produced_quantity,
        production_efficiency=production_data.production_efficiency,
        process=production_data.process,
        operating_time=production_data.operating_time,
        non_operating_time=production_data.non_operating_time,
        shift=production_data.shift,
        line_efficiency=production_data.line_efficiency,
        specification=production_data.specification,
        account_idx=production_data.account_idx
    )
    db.add(db_production)
    db.commit()

#inventory generate
def generate_random_inventory_data(db: Session):
    item_number_query = db.query(Production.item_number).order_by(Production.id.desc()).first()
    item_number = item_number_query[0] if item_number_query else None
    item_name_query = db.query(Production.item_name).filter(Production.item_number == item_number).order_by(Production.id.desc()).first()
    item_name = item_name_query[0] if item_name_query else None
    price = round(random.uniform(10, 100), 2)
    last_inventory = db.query(InventoryManagement).filter(InventoryManagement.item_number == item_number).order_by(InventoryManagement.id.desc()).first()
    basic_quantity = last_inventory.current_quantity if last_inventory else 0
    produced_quantity_query = db.query(Production.produced_quantity).filter(Production.item_number == item_number).order_by(Production.id.desc()).first()
    in_quantity = produced_quantity_query[0] if produced_quantity_query else 0
    defective_in_quantity = random.randint(0, in_quantity)
    quantity = basic_quantity+in_quantity-defective_in_quantity
    out_quantity = random.randint(0, quantity)
    quantity2 = quantity-out_quantity
    adjustment_quantity = random.randint(-quantity2, 50)
    current_quantity = quantity2+adjustment_quantity
    lot_current_quantity_query = db.query(MaterialInven.overall_status_quantity).filter(MaterialInven.item_number == item_number).order_by(MaterialInven.id.desc()).first()
    lot_current_quantity = lot_current_quantity_query[0] if lot_current_quantity_query else 0
    basic_amount = basic_quantity * price
    in_amount = in_quantity * price
    defective_in_amount = defective_in_quantity * price
    out_amount = out_quantity * price
    current_amount = current_quantity * price
    
    difference_quantity = current_quantity - lot_current_quantity

    return InventoryManagementCreate(
        date=datetime.now().date(),
        item_number=item_number,
        item_name=item_name,
        price=price,
        basic_quantity=basic_quantity,
        basic_amount=basic_amount,
        in_quantity=in_quantity,
        in_amount=in_amount,
        defective_in_quantity=defective_in_quantity,
        defective_in_amount=defective_in_amount,
        out_quantity=out_quantity,
        out_amount=out_amount,
        current_quantity=current_quantity,
        current_amount=current_amount,
        lot_current_quantity=lot_current_quantity,
        adjustment_quantity=adjustment_quantity,
        difference_quantity=difference_quantity
    )

def insert_inventory_data(db: Session, Invetory_data: InventoryManagementCreate):
        
    db_inventory = InventoryManagement(
        date=Invetory_data.date,
        item_number=Invetory_data.item_number,
        item_name=Invetory_data.item_name,
        price=Invetory_data.price,
        basic_quantity=Invetory_data.basic_quantity,
        basic_amount=Invetory_data.basic_amount,
        in_quantity=Invetory_data.in_quantity,
        in_amount=Invetory_data.in_amount,
        defective_in_quantity=Invetory_data.defective_in_quantity,
        defective_in_amount=Invetory_data.defective_in_amount,
        out_quantity=Invetory_data.out_quantity,
        out_amount=Invetory_data.out_amount,
        adjustment_quantity=Invetory_data.adjustment_quantity,
        current_quantity=Invetory_data.current_quantity,
        current_amount=Invetory_data.current_amount,
        lot_current_quantity=Invetory_data.lot_current_quantity,
        difference_quantity=Invetory_data.difference_quantity,
        account_idx=Invetory_data.account_idx
    )
    db.add(db_inventory)
    db.commit()

#material generate
def generate_random_material_data():
    number = random.randint(1, 10)
    item_number = f"Item_Number{number}"
    item_name = f"Item{number}"
    item_category = random.choice(['원재료', '부재료', '재공품', '제품', '반제품'])
    price = round(random.uniform(10, 100), 2)
    process = random.choice(["검사/조립", "사출"])
    client = random.choice(company_names)
    model = random.choice(['가전', '건조기', '세탁기', '식기세척기', '에어컨', '중장비', '포장박스', 'LX2PE', 'GEN3.5', 'MX5'])
    overall_status_quantity = random.randint(1, 100)
    overall_status_amount = overall_status_quantity*price

    return MaterialInvenCreate(
        date=datetime.now().date(),
        item_number=item_number,
        item_name=item_name,
        price=price,
        item_category=item_category,
        process=process,
        client=client,
        model=model,
        overall_status_quantity=overall_status_quantity,
        overall_status_amount=overall_status_amount
    )

def insert_material_data(db: Session, Material_data: MaterialInvenCreate):
        
    db_material = MaterialInven(
        date=datetime.now().date(),
        item_number=Material_data.item_number,
        item_name=Material_data.item_name,
        price=Material_data.price,
        item_category=Material_data.item_category,
        process=Material_data.process,
        client=Material_data.client,
        model=Material_data.model,
        overall_status_quantity=Material_data.overall_status_quantity,
        overall_status_amount=Material_data.overall_status_amount,
        account_idx=Material_data.account_idx
    )
    db.add(db_material)
    db.commit()

def main():
    db = SessionLocal()
    try:
        while True:
            
            production_data = generate_random_production_data()
            insert_production_data(db, production_data)
            material_inven_data = generate_random_material_data()
            insert_material_data(db, material_inven_data)
            invetory_data = generate_random_inventory_data(db)
            insert_inventory_data(db, invetory_data)
            print(f"Inserted: {production_data}, {invetory_data}, {material_inven_data}")
            t.sleep(10) 
    finally:
        db.close()

if __name__ == "__main__":
    main()