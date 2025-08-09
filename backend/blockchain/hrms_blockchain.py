import hashlib
import json
from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass

@dataclass
class HRTransaction:
    employee_id: str
    transaction_type: str  # payroll, attendance, leave, performance
    data: Dict
    timestamp: datetime
    hash: Optional[str] = None

class HRMSBlockchain:
    def __init__(self):
        self.chain: List[Dict] = []
        self.pending_transactions: List[HRTransaction] = []
        self.create_genesis_block()
    
    def create_genesis_block(self):
        """Create the first block in the chain"""
        genesis_block = {
            "index": 0,
            "timestamp": datetime.now().isoformat(),
            "transactions": [],
            "previous_hash": "0",
            "nonce": 0,
            "hash": self.calculate_hash(0, datetime.now().isoformat(), [], "0", 0)
        }
        self.chain.append(genesis_block)
    
    def calculate_hash(self, index: int, timestamp: str, transactions: List, previous_hash: str, nonce: int) -> str:
        """Calculate SHA-256 hash of block"""
        block_string = f"{index}{timestamp}{json.dumps(transactions, default=str)}{previous_hash}{nonce}"
        return hashlib.sha256(block_string.encode()).hexdigest()
    
    def add_transaction(self, transaction: HRTransaction):
        """Add transaction to pending pool"""
        transaction.hash = hashlib.sha256(
            f"{transaction.employee_id}{transaction.transaction_type}{json.dumps(transaction.data)}{transaction.timestamp}".encode()
        ).hexdigest()
        self.pending_transactions.append(transaction)
    
    def mine_block(self) -> Dict:
        """Mine a new block with pending transactions"""
        if not self.pending_transactions:
            return {"error": "No pending transactions"}
        
        previous_block = self.chain[-1]
        new_index = previous_block["index"] + 1
        timestamp = datetime.now().isoformat()
        
        # Convert transactions to dict format
        transactions = [
            {
                "employee_id": tx.employee_id,
                "type": tx.transaction_type,
                "data": tx.data,
                "timestamp": tx.timestamp.isoformat(),
                "hash": tx.hash
            }
            for tx in self.pending_transactions
        ]
        
        # Simple proof of work (find hash starting with "00")
        nonce = 0
        while True:
            hash_value = self.calculate_hash(new_index, timestamp, transactions, previous_block["hash"], nonce)
            if hash_value.startswith("00"):
                break
            nonce += 1
        
        new_block = {
            "index": new_index,
            "timestamp": timestamp,
            "transactions": transactions,
            "previous_hash": previous_block["hash"],
            "nonce": nonce,
            "hash": hash_value
        }
        
        self.chain.append(new_block)
        self.pending_transactions = []
        
        return new_block
    
    def verify_chain(self) -> bool:
        """Verify blockchain integrity"""
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i-1]
            
            # Verify current block hash
            calculated_hash = self.calculate_hash(
                current_block["index"],
                current_block["timestamp"],
                current_block["transactions"],
                current_block["previous_hash"],
                current_block["nonce"]
            )
            
            if current_block["hash"] != calculated_hash:
                return False
            
            # Verify link to previous block
            if current_block["previous_hash"] != previous_block["hash"]:
                return False
        
        return True
    
    def get_employee_history(self, employee_id: str) -> List[Dict]:
        """Get all transactions for an employee"""
        history = []
        for block in self.chain[1:]:  # Skip genesis block
            for tx in block["transactions"]:
                if tx["employee_id"] == employee_id:
                    history.append({
                        "block_index": block["index"],
                        "transaction": tx,
                        "block_hash": block["hash"]
                    })
        return history

class HRMSSmartContract:
    def __init__(self, blockchain: HRMSBlockchain):
        self.blockchain = blockchain
    
    def record_payroll(self, employee_id: str, salary_data: Dict):
        """Record payroll transaction"""
        transaction = HRTransaction(
            employee_id=employee_id,
            transaction_type="payroll",
            data=salary_data,
            timestamp=datetime.now()
        )
        self.blockchain.add_transaction(transaction)
        return transaction.hash
    
    def record_attendance(self, employee_id: str, attendance_data: Dict):
        """Record attendance transaction"""
        transaction = HRTransaction(
            employee_id=employee_id,
            transaction_type="attendance",
            data=attendance_data,
            timestamp=datetime.now()
        )
        self.blockchain.add_transaction(transaction)
        return transaction.hash
    
    def verify_employment(self, employee_id: str) -> Dict:
        """Verify employment history from blockchain"""
        history = self.blockchain.get_employee_history(employee_id)
        
        if not history:
            return {"verified": False, "message": "No employment records found"}
        
        return {
            "verified": True,
            "employee_id": employee_id,
            "total_records": len(history),
            "first_record": history[0]["transaction"]["timestamp"] if history else None,
            "latest_record": history[-1]["transaction"]["timestamp"] if history else None
        }