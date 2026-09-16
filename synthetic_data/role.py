from dataclasses import dataclass
from typing import List, Dict

@dataclass
class Role:
    bank_id: int
    role_id : int
    role_name: str

# Standard job title templates grouped logically
BASE_RETAIL_ROLES = [
    "Branch Manager",
    "Assistant Branch Manager",
    "Senior Teller",
    "Teller",
    "Customer Service Representative",
    "Personal Banker",
    "Financial Advisor",
    "Loan Officer"
]

CORPORATE_INVESTMENT_ROLES = [
    "Managing Director",
    "VP Investment Banking",
    "Relationship Manager",
    "Risk & Compliance Officer",
    "Corporate Credit Analyst",
    "Portfolio Manager"
]

DIGITAL_ROLES = [
    "Customer Support Specialist",
    "Fraud & AML Analyst",
    "Operations Specialist",
    "Product Specialist"
]

def generate_roles_for_pool(banks_pool: List[Bank]) -> List[Role]:
    roles: List[Role] = []

    for bank in banks_pool:
        # Determine appropriate role templates based on BankTier
        if bank.tier in (BankTier.LARGE_NATIONAL, BankTier.REGIONAL, BankTier.COMMUNITY):
            role_names = BASE_RETAIL_ROLES
        elif bank.tier in (BankTier.INVESTMENT_CORPORATE, BankTier.PRIVATE_WEALTH):
            role_names = CORPORATE_INVESTMENT_ROLES
        elif bank.tier == BankTier.DIGITAL_NEOBANK:
            role_names = DIGITAL_ROLES
        else:
            role_names = BASE_RETAIL_ROLES

        # Instantiate unique roles for this bank
        for name in role_names:
            roles.append(Role(
                bank_id=bank.bank_id,
                role_name=name
            ))

    return roles

def export_roles_to_sql(roles: List[Role]) -> None:
    for r in roles:
        name_esc = r.role_name.replace("'", "''")
        sql = (
            f"INSERT INTO Role (bank_id, role_name) "
            f"VALUES ({r.bank_id}, '{name_esc}');"
        )
        print(sql)
