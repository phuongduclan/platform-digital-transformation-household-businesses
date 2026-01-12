"""
Seed domain sample data: categories, products, customers, sellers
"""
import sys
if sys.platform == 'win32':
    try:
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
    except Exception:
        pass

from app import create_app
from infrastructure.databases.mssql import session
from infrastructure.models import Category, Product, Customer, Seller


def seed_domain():
    app = create_app()
    with app.app_context():
        try:
            print('[*] Seeding categories...')
            categories = [
                {'code': 'C001', 'name': 'Thực phẩm'},
                {'code': 'C002', 'name': 'Đồ uống'},
                {'code': 'C003', 'name': 'Văn phòng phẩm'},
            ]
            cat_objs = []
            for c in categories:
                ex = session.query(Category).filter_by(code=c['code']).first()
                if ex:
                    cat_objs.append(ex)
                    print('  [SKIP] category', c['code'])
                else:
                    obj = Category(code=c['code'], name=c['name'], status='ACTIVE', created_by='seed')
                    session.add(obj)
                    session.flush()
                    cat_objs.append(obj)
                    print('  [OK] created category', obj.code)

            print('[*] Seeding products...')
            products = [
                {'code': 'P001', 'name': 'Gạo ST25', 'category_code': 'C001', 'price': 20000},
                {'code': 'P002', 'name': 'Nước lọc 1.5L', 'category_code': 'C002', 'price': 8000},
                {'code': 'P003', 'name': 'Sổ tay A5', 'category_code': 'C003', 'price': 15000},
            ]
            for p in products:
                ex = session.query(Product).filter_by(code=p['code']).first()
                if ex:
                    print('  [SKIP] product', p['code'])
                    continue
                cat = session.query(Category).filter_by(code=p['category_code']).first()
                prod = Product(code=p['code'], name=p['name'], category_id=cat.id if cat else None, price=p['price'], status='ACTIVE', created_by='seed')
                session.add(prod)
                session.flush()
                print('  [OK] created product', prod.code)

            print('[*] Seeding customers...')
            customers = [
                {'code': 'CU001', 'name': 'Khách hàng A', 'phone': '0901000001'},
                {'code': 'CU002', 'name': 'Khách hàng B', 'phone': '0901000002'},
            ]
            for c in customers:
                ex = session.query(Customer).filter_by(code=c['code']).first()
                if ex:
                    print('  [SKIP] customer', c['code'])
                    continue
                cust = Customer(code=c['code'], name=c['name'], phone=c['phone'], status='ACTIVE', created_by='seed')
                session.add(cust)
                session.flush()
                print('  [OK] created customer', cust.code)

            print('[*] Seeding sellers...')
            sellers = [
                {'code': 'S001', 'name': 'Người bán A', 'phone': '0911000001'},
                {'code': 'S002', 'name': 'Người bán B', 'phone': '0911000002'},
            ]
            for s in sellers:
                ex = session.query(Seller).filter_by(code=s['code']).first()
                if ex:
                    print('  [SKIP] seller', s['code'])
                    continue
                seller = Seller(code=s['code'], name=s['name'], phone=s['phone'], status='ACTIVE', created_by='seed')
                session.add(seller)
                session.flush()
                print('  [OK] created seller', seller.code)

            session.commit()
            print('[SUCCESS] Domain sample seeded')
        except Exception as e:
            session.rollback()
            print('[ERROR]', e)
            import traceback
            traceback.print_exc()

if __name__ == '__main__':
    seed_domain()
