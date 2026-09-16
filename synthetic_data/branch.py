import random
import datetime
from .config import countries
from enum import Enum
from dataclasses import dataclass
from typing import List, Dict, Tuple
from faker import Faker

GLOBAL_SEED = 42
random.seed(GLOBAL_SEED)


class BankTier(Enum):
    LARGE_NATIONAL = "Large National Retail"
    REGIONAL = "Regional Commercial"
    COMMUNITY = "Local Community"
    DIGITAL_NEOBANK = "Digital Neobank"
    PRIVATE_WEALTH = "Private Wealth Management"
    INVESTMENT_CORPORATE = "Investment & Corporate Banking"

class BranchStrategy(Enum):
    AGGRESSIVE_PHYSICAL = "Aggressive Physical"
    BALANCED_HYBRID = "Balanced Hybrid"
    BOUTIQUE_MINIMAL = "Boutique Minimal"

class BranchType(Enum):
    HEADQUARTERS = "Corporate Headquarters"
    FLAGSHIP     = "Metropolitan Flagship"
    FULL_SERVICE = "Standard Full Service"
    EXPRESS      = "Express / Retail Kiosk"
    ATM_ONLY     = "Unstaffed ATM Vestibule"

@dataclass
class Bank:
    bank_id: int
    legal_name: str
    bic: str
    routing_no: str | None
    country_code: str
    created_at: datetime.date
    bank_status: str
    license_number: str
    tier: BankTier 
    is_international: bool
    headquarters_city: str  
    branch_strategy: BranchStrategy = BranchStrategy.BALANCED_HYBRID

@dataclass
class Branch:
    bank_id: int
    branch_name: str
    branch_region: str
    branch_address: str
    country_code: str


# --- LOOKUPS & CONFIGURATION ---

FAKERS: Dict[str, Faker] = {'US': Faker('en_US'), 'PK': Faker('pk_PK'), 'GB': Faker('en_GB')}
for fk in FAKERS.values():
    fk.seed_instance(GLOBAL_SEED)

TIER_BOUNDS = {
    BankTier.LARGE_NATIONAL: (250, 700, 450, 65),
    BankTier.REGIONAL: (20, 80, 35, 8),
    BankTier.COMMUNITY: (1, 8, 3, 1),
    BankTier.PRIVATE_WEALTH: (1, 4, 2, 1),
    BankTier.INVESTMENT_CORPORATE: (1, 3, 2, 1),
    BankTier.DIGITAL_NEOBANK: (0, 0, 0, 0)
}

TYPE_DISTRIBUTIONS = {
    BankTier.LARGE_NATIONAL: ([BranchType.FLAGSHIP, BranchType.FULL_SERVICE, BranchType.EXPRESS, BranchType.ATM_ONLY], [0.05, 0.65, 0.25, 0.05]),
    BankTier.REGIONAL: ([BranchType.FLAGSHIP, BranchType.FULL_SERVICE, BranchType.EXPRESS, BranchType.ATM_ONLY], [0.05, 0.70, 0.22, 0.03]),
    BankTier.COMMUNITY: ([BranchType.FULL_SERVICE, BranchType.EXPRESS], [0.85, 0.15]),
    BankTier.INVESTMENT_CORPORATE: ([BranchType.FLAGSHIP], [1.00]),
    BankTier.PRIVATE_WEALTH: ([BranchType.FLAGSHIP], [1.00]),
    BankTier.DIGITAL_NEOBANK: ([], [])
}


# --- GENERATION LOGIC ---

def get_branch_count(bank: Bank) -> int:
    min_b, max_b, mu, sigma = TIER_BOUNDS[bank.tier]
    if max_b == 0:
        return 0
    multipliers = {
        BranchStrategy.AGGRESSIVE_PHYSICAL: 1.2,
        BranchStrategy.BALANCED_HYBRID: 1.0,
        BranchStrategy.BOUTIQUE_MINIMAL: 0.4
    }
    count = int(random.gauss(mu, sigma) * multipliers.get(bank.branch_strategy, 1.0))
    return max(min_b, min(count, max_b))

def generate_address(country: str, city: str, modifier: str) -> str:
    fake = FAKERS.get(country, FAKERS['US'])
    num, street = fake.building_number(), fake.street_name()
    if country == 'TR':
        return f"{modifier} Mh., {street} Sk. No: {num}, {city}"
    elif country == 'DE':
        return f"{street} {num}, {modifier}, {city}"
    return f"{num} {street}, {modifier}, {city}"

def generate_branches_for_pool(banks_pool: List[Bank]) -> List[Branch]:
    branches: List[Branch] = []
    used_names: Dict[Tuple[int, str], set] = {}

    # Standard fallback country key if requested country code isn't in config
    fallback_country = 'US' if 'US' in countries else next(iter(countries.keys()))

    for bank in banks_pool:
        total_branches = get_branch_count(bank)
        if total_branches == 0:
            continue

        for i in range(total_branches):
            is_hq = (i == 0)
            is_foreign = not is_hq and bank.is_international and random.random() < 0.20

            # 1. Determine Location
            if is_hq or not is_foreign:
                country = bank.country_code if bank.country_code in countries else fallback_country
                country_data = countries.get(country, countries[fallback_country])
                cities = list(country_data.keys())
                city = bank.headquarters_city if (is_hq or bank.headquarters_city in cities) else random.choice(cities)
            else:
                foreign_options = [c for c in countries if c != bank.country_code]
                country = random.choice(foreign_options) if foreign_options else bank.country_code
                country_data = countries.get(country, countries[fallback_country])
                city = random.choice(list(country_data.keys()))

            # Safely resolve region & modifiers from the imported structure
            city_info = country_data.get(city, ('General', ['Central']))
            region, modifiers = city_info
            modifier = random.choice(modifiers) if modifiers else 'Central'

            # 2. Determine Branch Type & Name
            if is_hq:
                b_type = BranchType.HEADQUARTERS
                suffix = "Corporate Headquarters"
            else:
                types, weights = TYPE_DISTRIBUTIONS[bank.tier]
                b_type = random.choices(types, weights=weights)[0] if types else BranchType.FULL_SERVICE
                suffix = "International Office" if is_foreign else "Branch"

            # Ensure unique names per bank-city scope
            scope = (bank.bank_id, city)
            used_names.setdefault(scope, set())
            
            base_name = f"{city} {suffix}" if is_hq else f"{city} {modifier} {suffix}"
            branch_name = base_name
            counter = 1
            while branch_name in used_names[scope]:
                branch_name = f"{base_name} #{counter}"
                counter += 1
            used_names[scope].add(branch_name)

            # 3. Build & Collect
            branches.append(Branch(
                bank_id=bank.bank_id,
                branch_name=branch_name,
                branch_region=region,
                branch_address=generate_address(country, city, modifier),
                country_code=country
            ))

    return branches

def export_branches_to_sql(branches: List[Branch]) -> None:
    for br in branches:
        name_esc = br.branch_name.replace("'", "''")
        region_esc = br.branch_region.replace("'", "''")
        addr_esc = br.branch_address.replace("'", "''")
        
        sql = (
            f"INSERT INTO Branch (bank_id, branch_name, branch_region, branch_address, country_code) "
            f"VALUES ({br.bank_id}, '{name_esc}', '{region_esc}', '{addr_esc}', '{br.country_code}');"
        )
        print(sql)

# --- EXECUTION DEMO ---
if __name__ == "__main__":
    mock_banks = [
        Bank(
            bank_id=1, legal_name="Apex National Retailer", bic="APEXUS33", routing_no="122000044", 
            country_code="US", created_at=datetime.date(2010, 3, 15), bank_status="active", 
            license_number="OCC-11204", tier=BankTier.LARGE_NATIONAL, is_international=True, 
            headquarters_city="New York"
        ),
        Bank(
            bank_id=2, legal_name="Hanseatic Commerce Bank", bic="HANSDEBB", routing_no=None, 
            country_code="DE", created_at=datetime.date(2002, 11, 20), bank_status="active", 
            license_number="BAFIN-4410", tier=BankTier.REGIONAL, is_international=False, 
            headquarters_city="Frankfurt"
        )
    ]
    
    export_branches_to_sql(generate_branches_for_pool(mock_banks))
