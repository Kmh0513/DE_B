import random
import time as t
from datetime import datetime, timedelta, time
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Production, InventoryManagement
from schemas import ProductionBase, InventoryManagementBase
from database import SessionLocal

def generate_random_production_data():
    target_quantity = random.randint(200, 500)
    produced_quantity = random.randint(1, target_quantity) 
    production_efficiency =int(produced_quantity / target_quantity * 100)
    operating_time = timedelta(hours=random.randint(0, 23), minutes=random.randint(0, 59))
    non_operating_time = timedelta(hours=random.randint(0, 23), minutes=random.randint(0, 59))
    total_time = operating_time + non_operating_time
    equipment_efficiency = (operating_time.total_seconds() / total_time.total_seconds()) * 100 if total_time.total_seconds() > 0 else 0
    item_number_name = random.randint(1, 10)
    # 생산 데이터 생성
    return ProductionBase(
        date=datetime.now().date(),
        line=f"Line{random.randint(1, 5)}",
        operator=f"Operator{random.randint(1, 10)}",
        item_number=item_number_name,
        item_name=f"Item{item_number_name}",
        model=f"Model{random.randint(1, 5)}",
        target_quantity=target_quantity,
        produced_quantity=produced_quantity,
        production_efficiency=production_efficiency,
        equipment=f"Equipment{random.randint(1, 10)}",
        operating_time=(datetime.min + operating_time).time(),  # time 객체로 변환
        non_operating_time=(datetime.min + non_operating_time).time(),  # time 객체로 변환
        shift=f"Shift{random.randint(1, 3)}",
        equipment_efficiency=equipment_efficiency,
        specification=f"Specification{random.randint(1, 5)}"
    )

def insert_production_data(db: Session, production_data: ProductionBase):
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
        equipment=production_data.equipment,
        operating_time=production_data.operating_time,
        non_operating_time=production_data.non_operating_time,
        shift=production_data.shift,
        equipment_efficiency=production_data.equipment_efficiency,
        specification=production_data.specification,
        account_idx=production_data.account_idx
    )
    db.add(db_production)
    db.commit()

def generate_random_inventory_data():
    item_number = random.randint(1, 10)
    item_name = f"Item{item_number}"
    price = round(random.uniform(10.0, 100.0), 2)
    basic_quantity = random.randint(1, 100)
    quantity_received = random.randint(0, 100)
    defective_quantity_received = random.randint(0, 20)
    quantity_shipped = random.randint(0, 100)
    current_stock = random.randint(0, 200)
    current_LOT_stock = random.randint(0, 200)
    basic_amount = basic_quantity * price
    received_amount = quantity_received * price
    defective_received_amount = defective_quantity_received * price
    shipped_amount = quantity_shipped * price
    current_amount = current_stock * price
    adjustment_quantity = random.randint(-50, 50)
    difference_quantity = current_stock - current_LOT_stock

    return InventoryManagementBase(
        date=datetime.now().date(),
        item_id=item_number,
        item_name=item_name,
        price=price,
        basic_quantity=basic_quantity,
        basic_amount=basic_amount,
        in_quantity=quantity_received,
        in_amount=received_amount,
        defective_in_quantity=defective_quantity_received,
        defective_in_amount=defective_received_amount,
        out_quantity=quantity_shipped,
        out_amount=shipped_amount,
        current_quantity=current_stock,
        current_amount=current_amount,
        lot_current_quantity=current_LOT_stock,
        adjustment_quantity=adjustment_quantity,
        difference_quantity=difference_quantity
    )

def insert_inventory_data(db: Session, Invetory_data: InventoryManagementBase):
    
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

def main():
    db = SessionLocal()
    try:
        while True:
            production_data = generate_random_production_data()
            Invetory_data = generate_random_inventory_data()
            insert_production_data(db, production_data)
            insert_inventory_data(db, Invetory_data)
            print(f"Inserted: {production_data}, {Invetory_data}")
            t.sleep(10)  # 10초 대기
    finally:
        db.close()

if __name__ == "__main__":
    main()