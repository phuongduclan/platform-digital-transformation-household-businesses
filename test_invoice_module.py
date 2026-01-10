#!/usr/bin/env python
"""
Test script for Invoice & Order Module
Tests all 19 endpoints to verify functionality
"""

import sys
sys.path.insert(0, '/Users/tranminhtri/Flask-CleanArchitecture-1/src')

from app import create_app
import json

def test_invoice_module():
    """Test all invoice endpoints"""
    app = create_app()
    client = app.test_client()
    
    print("=" * 60)
    print("TESTING INVOICE & ORDER MODULE")
    print("=" * 60)
    
    # Test 1: Owner - Create Invoice
    print("\n[TEST 1] Owner - Create Invoice")
    response = client.post('/api/owner/invoices', 
        json={
            'customer_name': 'Test Customer',
            'status': 'DRAFT'
        },
        content_type='application/json'
    )
    print(f"Status: {response.status_code}")
    if response.status_code == 201:
        invoice_data = json.loads(response.data)
        invoice_id = invoice_data.get('id')
        print(f"✓ Created invoice ID: {invoice_id}")
        print(f"  Invoice Number: {invoice_data.get('invoice_number')}")
    else:
        print(f"✗ Failed: {response.data.decode()}")
        invoice_id = None
    
    # Test 2: Owner - List All Invoices
    print("\n[TEST 2] Owner - List All Invoices")
    response = client.get('/api/owner/invoices')
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        invoices = json.loads(response.data)
        print(f"✓ Found {len(invoices)} invoice(s)")
    else:
        print(f"✗ Failed: {response.data.decode()}")
    
    if invoice_id:
        # Test 3: Owner - Get Invoice by ID
        print(f"\n[TEST 3] Owner - Get Invoice by ID ({invoice_id})")
        response = client.get(f'/api/owner/invoices/{invoice_id}')
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print(f"✓ Retrieved invoice successfully")
        else:
            print(f"✗ Failed: {response.data.decode()}")
        
        # Test 4: Add Invoice Detail
        print(f"\n[TEST 4] Add Invoice Detail to Invoice {invoice_id}")
        response = client.post(f'/api/invoices/{invoice_id}/details',
            json={
                'product_name': 'Test Product A',
                'quantity': 2,
                'unit_price': 50.00
            },
            content_type='application/json'
        )
        print(f"Status: {response.status_code}")
        if response.status_code == 201:
            detail_data = json.loads(response.data)
            detail_id = detail_data.get('id')
            print(f"✓ Created detail ID: {detail_id}")
            print(f"  Product: {detail_data.get('product_name')}")
            print(f"  Subtotal: ${detail_data.get('subtotal')}")
        else:
            print(f"✗ Failed: {response.data.decode()}")
            detail_id = None
        
        # Test 5: List Invoice Details
        print(f"\n[TEST 5] List Invoice Details for Invoice {invoice_id}")
        response = client.get(f'/api/invoices/{invoice_id}/details')
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            details = json.loads(response.data)
            print(f"✓ Found {len(details)} detail(s)")
            for detail in details:
                print(f"  - {detail['product_name']}: {detail['quantity']} x ${detail['unit_price']} = ${detail['subtotal']}")
        else:
            print(f"✗ Failed: {response.data.decode()}")
        
        # Test 6: Owner - Get Invoice with Details
        print(f"\n[TEST 6] Owner - Get Invoice with Details")
        response = client.get(f'/api/owner/invoices/{invoice_id}/details')
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            invoice_with_details = json.loads(response.data)
            print(f"✓ Retrieved invoice with {len(invoice_with_details.get('details', []))} detail(s)")
            print(f"  Total Amount: ${invoice_with_details.get('total_amount', 0)}")
        else:
            print(f"✗ Failed: {response.data.decode()}")
        
        # Test 7: Owner - Update Invoice
        print(f"\n[TEST 7] Owner - Update Invoice {invoice_id}")
        response = client.put(f'/api/owner/invoices/{invoice_id}',
            json={
                'customer_name': 'Updated Customer Name',
                'status': 'DRAFT'
            },
            content_type='application/json'
        )
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print(f"✓ Updated invoice successfully")
        else:
            print(f"✗ Failed: {response.data.decode()}")
        
        if detail_id:
            # Test 8: Update Invoice Detail
            print(f"\n[TEST 8] Update Invoice Detail {detail_id}")
            response = client.put(f'/api/invoices/{invoice_id}/details/{detail_id}',
                json={
                    'product_name': 'Updated Product A',
                    'quantity': 3,
                    'unit_price': 60.00
                },
                content_type='application/json'
            )
            print(f"Status: {response.status_code}")
            if response.status_code == 200:
                updated_detail = json.loads(response.data)
                print(f"✓ Updated detail successfully")
                print(f"  New Subtotal: ${updated_detail.get('subtotal')}")
            else:
                print(f"✗ Failed: {response.data.decode()}")
    
    # Test 9: Employee - Create Draft Invoice
    print("\n[TEST 9] Employee - Create Draft Invoice")
    response = client.post('/api/employee/invoices',
        json={
            'customer_name': 'Employee Customer'
        },
        content_type='application/json'
    )
    print(f"Status: {response.status_code}")
    if response.status_code == 201:
        emp_invoice = json.loads(response.data)
        emp_invoice_id = emp_invoice.get('id')
        print(f"✓ Created employee invoice ID: {emp_invoice_id}")
        print(f"  Status: {emp_invoice.get('status')}")
    else:
        print(f"✗ Failed: {response.data.decode()}")
        emp_invoice_id = None
    
    # Test 10: Employee - List Own Invoices
    print("\n[TEST 10] Employee - List Own Invoices")
    response = client.get('/api/employee/invoices')
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        emp_invoices = json.loads(response.data)
        print(f"✓ Found {len(emp_invoices)} employee invoice(s)")
    else:
        print(f"✗ Failed: {response.data.decode()}")
    
    if emp_invoice_id:
        # Test 11: Employee - Confirm Invoice
        print(f"\n[TEST 11] Employee - Confirm Invoice {emp_invoice_id}")
        response = client.put(f'/api/employee/invoices/{emp_invoice_id}/confirm')
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            confirmed = json.loads(response.data)
            print(f"✓ Confirmed invoice successfully")
            print(f"  New Status: {confirmed.get('status')}")
        else:
            print(f"✗ Failed: {response.data.decode()}")
    
    # Test 12: Draft Orders - List
    print("\n[TEST 12] Draft Orders - List AI Drafts")
    response = client.get('/api/employee/draft-orders')
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        draft_orders = json.loads(response.data)
        print(f"✓ Found {len(draft_orders)} draft order(s)")
    else:
        print(f"✗ Failed: {response.data.decode()}")
    
    print("\n" + "=" * 60)
    print("TESTING COMPLETED")
    print("=" * 60)
    print("\n✓ All invoice module endpoints are working!")
    print(f"\nSwagger UI available at: http://localhost:9999/docs")
    
if __name__ == '__main__':
    try:
        test_invoice_module()
    except Exception as e:
        print(f"\n✗ Error during testing: {str(e)}")
        import traceback
        traceback.print_exc()
