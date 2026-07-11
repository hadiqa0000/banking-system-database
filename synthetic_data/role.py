import random
import datetime
import string
import calendar
from dataclasses import dataclass, field
from typing import List, Dict, Optional
from faker import Faker
from enum import Enum

# Define BranchType since it's referenced
class BranchType(Enum):
    HEADQUARTERS = "headquarters"
    REGIONAL = "regional"
    LOCAL = "local"
    DIGITAL = "digital"

@dataclass
class Bank:
    legal_name: str
    bic: str
    routing_no: Optional[str]  # Only assigned for 'US'
    country_code: str
    created_at: datetime.date
    bank_status: str
    headquarters_city: str
    headquarters_address: str
    license_number: str

@dataclass
class Branch:
    bank_id: int
    name: str
    region: str
    city: str               
    branch_address: str
    country_code: str
    branch_type: BranchType

@dataclass
class Role:
    bank_id: int
    role_id: int
    role_name: str  # Fixed: added missing comma and colon

# Set seed for reproducibility
GLOBAL_SEED = 42
random.seed(GLOBAL_SEED)

# Fixed typos and removed extra space
ROLE_NAMES = [
    'Branch Manager', 
    'Teller', 
    'Customer Service Rep',  # Fixed: removed leading space
    'Loan Officer', 
    'Compliance Officer',  # Fixed: spelling
    'Accountant'
]

def generate_roles_for_bank(bank_id):
    # Fixed: proper indentation and added role_id
    return [
        {
            'bank_id': bank_id, 
            'role_id': idx + 1,  # Added role_id
            'role_name': name
        } 
        for idx, name in enumerate(ROLE_NAMES)
    ]

# Example usage:
if __name__ == "__main__":
    # Test the function
    roles = generate_roles_for_bank(1)
    print("Generated roles:")
    for role in roles:
        print(f"  Bank {role['bank_id']}: {role['role_name']} (ID: {role['role_id']})")
