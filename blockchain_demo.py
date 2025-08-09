#!/usr/bin/env python3
"""
HRMS Malaysia Blockchain Demo
Demonstrates blockchain integration for HR records
"""

import asyncio
from backend.blockchain.hrms_blockchain import HRMSBlockchain, HRMSSmartContract
from datetime import datetime

async def demo_blockchain():
    print("⛓️  HRMS Malaysia - Blockchain Demo")
    print("=" * 40)
    
    # Initialize blockchain
    blockchain = HRMSBlockchain()
    smart_contract = HRMSSmartContract(blockchain)
    
    print(f"✅ Blockchain initialized with {len(blockchain.chain)} blocks")
    
    # Record payroll transactions
    print("\n💰 Recording Payroll Transactions:")
    
    payroll_data = {
        "basic_salary": 5500,
        "epf_employee": 605,
        "epf_employer": 715,
        "net_salary": 4867.5,
        "month": "2024-12"
    }
    
    tx1_hash = smart_contract.record_payroll("EMP001", payroll_data)
    print(f"   Employee EMP001: {tx1_hash[:16]}...")
    
    tx2_hash = smart_contract.record_attendance("EMP001", {
        "check_in": "09:00",
        "check_out": "18:00",
        "hours": 8,
        "date": "2024-12-09"
    })
    print(f"   Attendance EMP001: {tx2_hash[:16]}...")
    
    # Mine block
    print("\n⛏️  Mining Block:")
    block = blockchain.mine_block()
    print(f"   Block #{block['index']} mined")
    print(f"   Hash: {block['hash'][:32]}...")
    print(f"   Transactions: {len(block['transactions'])}")
    
    # Verify blockchain
    print("\n🔍 Verifying Blockchain:")
    is_valid = blockchain.verify_chain()
    print(f"   Blockchain valid: {is_valid}")
    print(f"   Total blocks: {len(blockchain.chain)}")
    
    # Get employee history
    print("\n📋 Employee History:")
    history = blockchain.get_employee_history("EMP001")
    for record in history:
        tx = record["transaction"]
        print(f"   {tx['type']}: {tx['timestamp'][:19]}")
    
    # Verify employment
    print("\n✅ Employment Verification:")
    verification = smart_contract.verify_employment("EMP001")
    print(f"   Verified: {verification['verified']}")
    print(f"   Total records: {verification.get('total_records', 0)}")
    
    print("\n🎉 Blockchain demo completed!")

if __name__ == "__main__":
    asyncio.run(demo_blockchain())