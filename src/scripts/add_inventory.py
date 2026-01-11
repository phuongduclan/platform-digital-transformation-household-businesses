"""
Script đơn giản để thêm inventory
Thêm 10 sản phẩm vào inventory với product_id=1, unit_id=1
"""
import sys
import os
from datetime import datetime

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from infrastructure.databases.mssql import session
from infrastructure.models import Inventory, Warehouse, Product, Unit

def add_inventory(product_id=1, unit_id=1, quantity=10):
    """
    Thêm inventory với product_id, unit_id và quantity cụ thể
    Tự động tìm warehouse_id đầu tiên của household có product này
    """
    try:
        # Lấy product để biết household_id
        product = session.query(Product).filter_by(id=product_id).first()
        if not product:
            print(f"ERROR: Product với id={product_id} không tồn tại")
            return
        
        household_id = product.household_id
        print(f"Found product_id={product_id} in household_id={household_id}")
        
        # Lấy warehouse đầu tiên của household
        warehouse = session.query(Warehouse).filter_by(
            household_id=household_id,
            status='Active'
        ).first()
        
        if not warehouse:
            print(f"ERROR: Không tìm thấy warehouse cho household_id={household_id}")
            return
        
        warehouse_id = warehouse.id
        print(f"Using warehouse_id={warehouse_id}")
        
        # Kiểm tra xem inventory đã tồn tại chưa
        existing = session.query(Inventory).filter_by(
            product_id=product_id,
            unit_id=unit_id,
            warehouse_id=warehouse_id
        ).first()
        
        if existing:
            # Nếu đã có, tăng quantity thêm 10
            old_quantity = existing.quantity
            existing.quantity += quantity
            existing.updated_at = datetime.utcnow()
            session.commit()
            print(f"[OK] Updated inventory: {old_quantity} -> {existing.quantity}")
            print(f"  (product_id={product_id}, unit_id={unit_id}, warehouse_id={warehouse_id})")
        else:
            # Nếu chưa có, tạo mới
            inventory = Inventory(
                product_id=product_id,
                unit_id=unit_id,
                warehouse_id=warehouse_id,
                quantity=quantity,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            session.add(inventory)
            session.commit()
            print(f"[OK] Created new inventory: quantity={quantity}")
            print(f"  (product_id={product_id}, unit_id={unit_id}, warehouse_id={warehouse_id})")
        
        # Hiển thị inventory hiện tại
        current = session.query(Inventory).filter_by(
            product_id=product_id,
            unit_id=unit_id,
            warehouse_id=warehouse_id
        ).first()
        
        if current:
            print(f"\nCurrent inventory:")
            print(f"  Product ID: {current.product_id}")
            print(f"  Unit ID: {current.unit_id}")
            print(f"  Warehouse ID: {current.warehouse_id}")
            print(f"  Quantity: {current.quantity}")
            print(f"  Created: {current.created_at}")
            print(f"  Updated: {current.updated_at}")
        
    except Exception as e:
        session.rollback()
        print(f"ERROR: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    print("=" * 60)
    print("ADD INVENTORY")
    print("=" * 60)
    print()
    
    # Thêm 10 sản phẩm
    add_inventory(product_id=1, unit_id=1, quantity=10)
    
    print()
    print("=" * 60)
    print("DONE!")
    print("=" * 60)
