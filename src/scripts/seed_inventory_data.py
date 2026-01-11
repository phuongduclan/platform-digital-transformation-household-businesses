"""
Seed Data Script - Inventory
Tạo dữ liệu inventory cho các products, units và warehouses

Usage:
    python src/scripts/seed_inventory_data.py                    # Seed inventory cho tất cả households
    python src/scripts/seed_inventory_data.py --household-id 1002 # Seed inventory cho household cụ thể
    python src/scripts/seed_inventory_data.py --clean             # Xóa tất cả inventory trước khi seed
"""
import sys
import os
import argparse
import random
from datetime import datetime

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from infrastructure.databases.mssql import session
from infrastructure.models import Inventory, Product, Unit, Warehouse

def clean_inventory(household_id=None):
    """
    Xóa tất cả inventory (hoặc của household cụ thể)
    
    Args:
        household_id: Nếu có, chỉ xóa inventory của household này
    """
    print("Cleaning inventory data...")
    try:
        if household_id:
            # Xóa inventory của household cụ thể (qua warehouse)
            warehouses = session.query(Warehouse).filter_by(household_id=household_id).all()
            warehouse_ids = [w.id for w in warehouses]
            if warehouse_ids:
                deleted_count = session.query(Inventory).filter(
                    Inventory.warehouse_id.in_(warehouse_ids)
                ).delete(synchronize_session=False)
                session.commit()
                print(f"  Deleted {deleted_count} inventory records for household_id={household_id}")
            else:
                print(f"  No warehouses found for household_id={household_id}")
        else:
            # Xóa tất cả inventory
            deleted_count = session.query(Inventory).delete()
            session.commit()
            print(f"  Deleted {deleted_count} inventory records")
    except Exception as e:
        session.rollback()
        print(f"  ERROR cleaning inventory: {str(e)}")
        raise

def seed_inventory(household_id=None, default_quantity=100):
    """
    Seed inventory data cho tất cả products, units và warehouses
    
    Args:
        household_id: Nếu có, chỉ seed cho household này
        default_quantity: Số lượng mặc định cho mỗi inventory (default: 100)
    """
    print("Seeding inventory data...")
    
    try:
        # Lấy tất cả households hoặc household cụ thể
        if household_id:
            households = session.query(Warehouse).filter_by(household_id=household_id).distinct(Warehouse.household_id).all()
            household_ids = [w.household_id for w in households] if households else []
            if not household_ids:
                print(f"  WARNING: No warehouses found for household_id={household_id}")
                return
        else:
            # Lấy tất cả household_ids từ warehouses
            households = session.query(Warehouse.household_id).distinct().all()
            household_ids = [h[0] for h in households]
        
        if not household_ids:
            print("  WARNING: No households found")
            return
        
        total_created = 0
        
        for h_id in household_ids:
            print(f"\n  Processing household_id={h_id}...")
            
            # Lấy products của household
            products = session.query(Product).filter_by(household_id=h_id, status='Active').all()
            if not products:
                print(f"    No active products found for household_id={h_id}")
                continue
            
            # Lấy units của household
            units = session.query(Unit).filter_by(household_id=h_id, status='Active').all()
            if not units:
                print(f"    No active units found for household_id={h_id}")
                continue
            
            # Lấy warehouses của household
            warehouses = session.query(Warehouse).filter_by(household_id=h_id, status='Active').all()
            if not warehouses:
                print(f"    No active warehouses found for household_id={h_id}")
                continue
            
            print(f"    Found {len(products)} products, {len(units)} units, {len(warehouses)} warehouses")
            
            # Tạo inventory cho mỗi combination: product x unit x warehouse
            created_count = 0
            for product in products:
                for unit in units:
                    for warehouse in warehouses:
                        # Kiểm tra xem inventory đã tồn tại chưa
                        existing = session.query(Inventory).filter_by(
                            product_id=product.id,
                            unit_id=unit.id,
                            warehouse_id=warehouse.id
                        ).first()
                        
                        if existing:
                            # Nếu đã có, skip hoặc update quantity
                            # Ở đây chúng ta skip để không ghi đè dữ liệu hiện có
                            continue
                        
                        # Tạo inventory mới với quantity ngẫu nhiên từ 50-200
                        quantity = random.randint(50, 200) if default_quantity == 100 else default_quantity
                        
                        inventory = Inventory(
                            product_id=product.id,
                            unit_id=unit.id,
                            warehouse_id=warehouse.id,
                            quantity=quantity,
                            created_at=datetime.utcnow(),
                            updated_at=datetime.utcnow()
                        )
                        session.add(inventory)
                        created_count += 1
            
            session.commit()
            print(f"    Created {created_count} inventory records for household_id={h_id}")
            total_created += created_count
        
        print(f"\n  Total created: {total_created} inventory records")
        print("Inventory data seeded successfully!\n")
        
    except Exception as e:
        session.rollback()
        print(f"  ERROR seeding inventory: {str(e)}")
        raise

def main():
    """
    Main function to seed inventory data
    """
    parser = argparse.ArgumentParser(description='Seed Inventory Data')
    parser.add_argument(
        '--household-id',
        type=int,
        help='Seed inventory for specific household_id only'
    )
    parser.add_argument(
        '--clean',
        action='store_true',
        help='Clean all inventory data before seeding'
    )
    parser.add_argument(
        '--quantity',
        type=int,
        default=100,
        help='Default quantity for each inventory (default: 100, or random 50-200 if not specified)'
    )
    args = parser.parse_args()
    
    print("=" * 60)
    print("SEED DATA: Inventory")
    print("=" * 60)
    print()
    
    try:
        # Bước 1: Clean inventory nếu có flag --clean
        if args.clean:
            clean_inventory(household_id=args.household_id)
            print()
        
        # Bước 2: Seed inventory data
        seed_inventory(household_id=args.household_id, default_quantity=args.quantity)
        
        print("=" * 60)
        print("DONE!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\nERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
