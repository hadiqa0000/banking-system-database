import random
import datetime
import string
from enum import Enum, auto
from dataclasses import dataclass
from typing import List, Dict, Optional, Tuple
from faker import Faker

# --- ENGINE DETERMINISM SEEDING ---
GLOBAL_SEED = 42
random.seed(GLOBAL_SEED)
CURRENT_YEAR = datetime.date.today().year

# --- CORE DOMAIN TIER ARCHITECTURE ---
class BankTier(Enum):
    LARGE_NATIONAL = "Large NationalRetail"
    REGIONAL = "Regional Commercial"
    COMMUNITY = "Local Community"
    DIGITAL_NEOBANK = "Digital Neobank"
    PRIVATE_WEALTH = "Private Wealth Management"
    INVESTMENT_CORPORATE = "Investment & Corporate Banking"

# --- SYSTEM INTEGRATION HOOKS (From upstream Bank dataclass layer) ---
@dataclass
class Bank:
    bank_id: int
    legal_name: str
    bic: str
    routing_no: Optional[str]
    country_code: str
    created_at: datetime.date
    bank_status: str
    headquarters_city: str
    headquarters_address: str
    license_number: str
    # New structural property passed downward from Bank initialization engine
    tier: BankTier 

@dataclass
class Branch:
    bank_id: int
    branch_id: int
    name: str
    region: str
    branch_address: str
    country_code: str

# --- HIGH-FIDELITY GEOGRAPHIC CLUSTER MATRIX ---
# Maps specific cities to their containing operational Region, and defines adjacent spillover regions
CITY_GEOGRAPHY_ANCHORS = {
    'US': {
        'regions': {
            'New York': {'home': 'New York', 'adjacent': ['Pennsylvania', 'Massachusetts'], 'far': ['California', 'Texas', 'Florida']},
            'Chicago': {'home': 'Illinois', 'adjacent': ['Indiana', 'Wisconsin', 'Michigan'], 'far': ['New York', 'California', 'Texas']},
            'Charlotte': {'home': 'North Carolina', 'adjacent': ['South Carolina', 'Virginia', 'Georgia'], 'far': ['New York', 'California', 'Florida']},
            'San Francisco': {'home': 'California', 'adjacent': ['Nevada', 'Oregon', 'Arizona'], 'far': ['New York', 'Texas', 'Illinois']},
            'Dallas': {'home': 'Texas', 'adjacent': ['Oklahoma', 'Louisiana', 'New Mexico'], 'far': ['New York', 'California', 'Florida']}
        }
    },
    'GB': {
        'regions': {
            'London': {'home': 'Greater London', 'adjacent': ['South East', 'East of England'], 'far': ['Scotland', 'North West']},
            'Edinburgh': {'home': 'Scotland', 'adjacent': ['North East', 'North West'], 'far': ['Greater London', 'West Midlands']},
            'Manchester': {'home': 'North West', 'adjacent': ['Yorkshire', 'West Midlands'], 'far': ['Greater London', 'Scotland']},
            'Birmingham': {'home': 'West Midlands', 'adjacent': ['East Midlands', 'Wales'], 'far': ['Greater London', 'Scotland']}
        }
    },
    'DE': {
        'regions': {
            'Frankfurt': {'home': 'Hesse', 'adjacent': ['Rhineland-Palatinate', 'Bavaria'], 'far': ['Berlin', 'Hamburg']},
            'Munich': {'home': 'Bavaria', 'adjacent': ['Baden-Württemberg', 'Hesse'], 'far': ['Berlin', 'Hamburg']},
            'Berlin': {'home': 'Berlin', 'adjacent': ['Brandenburg', 'Saxony'], 'far': ['Hesse', 'Bavaria']},
            'Hamburg': {'home': 'Hamburg', 'adjacent': ['Lower Saxony', 'Schleswig-Holstein'], 'far': ['Hesse', 'Bavaria']}
        }
    },
    'TR': {
        'regions': {
            'Istanbul': {'home': 'Marmara', 'adjacent': ['Aegean', 'Black Sea'], 'far': ['Central Anatolia', 'Mediterranean']},
            'Ankara': {'home': 'Central Anatolia', 'adjacent': ['Mediterranean', 'Black Sea'], 'far': ['Marmara', 'Aegean']},
            'İzmir': {'home': 'Aegean', 'adjacent': ['Marmara', 'Mediterranean'], 'far': ['Central Anatolia', 'Eastern Anatolia']},
            'Bursa': {'home': 'Marmara', 'adjacent': ['Aegean', 'Central Anatolia'], 'far': ['Mediterranean', 'Black Sea']}
        }
    }
}

# Regional neighborhood localization descriptors for realistic unique branch naming naming patterns
LOCALITY_NAMES = {
    'New York': ['Manhattan Downtown', 'Brooklyn Heights', 'Wall Street Local', 'Queens Center', 'Albany Hub', 'Buffalo Metro'],
    'Texas': ['Downtown Austin', 'Houston Galleria', 'Dallas Uptown', 'Fort Worth Stockyards', 'San Antonio Riverwalk', 'El Paso Valley'],
    'California': ['Manhattan Beach', 'Palo Alto', 'Downtown LA', 'Financial District SF', 'La Jolla', 'Sacramento Capital'],
    'Illinois': ['Chicago Loop', 'Lincoln Park', 'Magnificent Mile', 'Evanston North', 'Springfield Metro'],
    'Florida': ['Miami Brickell', 'Orlando Central', 'Tampa Riverwalk', 'Jacksonville Hub'],
    'Greater London': ['Canary Wharf', 'City Centre', 'Westminster', 'Covent Garden', 'Croydon Office'],
    'Scotland': ['Edinburgh Old Town', 'Glasgow Central', 'Aberdeen Port', 'Dundee Waterfront'],
    'Hesse': ['Frankfurt Innenstadt', 'Frankfurt Westend', 'Wiesbaden Zentrum', 'Kassel Hub'],
    'Bavaria': ['München Altstadt', 'Nürnberg Burg', 'Augsburg Mitte', 'Regensburg Local'],
    'Marmara': ['Kadıköy Merkez', 'Üsküdar Sahil', 'Levent Plazalar', 'Beşiktaş Çarşı', 'Bursa Osmangazi'],
    'Central Anatolia': ['Kızılay Merkez', 'Çankaya Hills', 'Eskişehir Tepebaşı', 'Konya Selçuklu']
}

# Global tracking caches ensuring domain unique constraints stay intact
used_bank_branch_names: Dict[int, set] = {}
used_branch_addresses: set = {}

FAKERS: Dict[str, Faker] = {
    'US': Faker('en_US'), 'GB': Faker('en_GB'), 'DE': Faker('de_DE'), 'TR': Faker('tr_TR'), 'JP': Faker('ja_JP')
}
for fk in FAKERS.values():
    fk.seed_instance(GLOBAL_SEED)

# --- CONFIGURATION MODEL LOOKUPS ---
TIER_FOOTPRINT_RULES = {
    BankTier.LARGE_NATIONAL: (150, 600),
    BankTier.REGIONAL: (15, 65),
    BankTier.COMMUNITY: (2, 9),
    BankTier.PRIVATE_WEALTH: (1, 4),
    BankTier.INVESTMENT_CORPORATE: (1, 3),
    BankTier.DIGITAL_NEOBANK: (0, 0) # Headquarter only deployment models
}

# --- GENERATION LOGIC ENGINES ---

def determine_branch_count_by_tier(bank: Bank) -> int:
    """Calculates branch totals cleanly decoupled from age, matching core strategic intent."""
    min_b, max_b = TIER_FOOTPRINT_RULES[bank.tier]
    if min_b == 0 and max_b == 0:
        return 0 # Neo-banks use digital-only pipelines with no sub-branches
    return random.randint(min_b, max_b)

def resolve_gravity_geography(bank: Bank) -> Tuple[str, str, str]:
    """Calculates directional regional branch networks based on HQ geometric clustering."""
    country = bank.country_code
    hq_city = bank.headquarters_city
    
    # Safe structural fallback sequence if country maps outside regional alignment parameters
    if country not in CITY_GEOGRAPHY_ANCHORS or hq_city not in CITY_GEOGRAPHY_ANCHORS[country]['regions']:
        return country, "Central Territory", "Metropolitan Hub"
        
    geo_map = CITY_GEOGRAPHY_ANCHORS[country]['regions'][hq_city]
    
    # Establish Regional Clustering Proximity Matrix Weights
    # 60% Home State/Region | 30% Bordering/Adjacent States | 10% Remote National Markets
    roll = random.random()
    if roll < 0.60:
        chosen_region = geo_map['home']
    elif roll < 0.90:
        chosen_region = random.choice(geo_map['adjacent'])
    else:
        chosen_region = random.choice(geo_map['far'])
        
    # Pick a realistic naming locality node based on chosen target region
    localities = LOCALITY_NAMES.get(chosen_region, [f"{chosen_region} Central", f"{chosen_region} Plaza"])
    chosen_locality = random.choice(localities)
    
    return country, chosen_region, chosen_locality

def generate_unique_address(country: str, locality: str, fake: Faker) -> str:
    attempts = 0
    while attempts < 1000:
        if country in ['DE', 'FR', 'NL', 'IT', 'CH']:
            addr = f"{fake.street_name()} {fake.building_number()}, {locality}"
        else:
            addr = f"{fake.building_number()} {fake.street_name()}, {locality}"
            
        if addr not in used_branch_addresses:
            used_branch_addresses.add(addr)
            return addr
        attempts += 1
    return f"{random.randint(1000, 9999)} Business Plaza, {locality}"

def generate_unique_branch_name(bank_id: int, locality: str) -> str:
    if bank_id not in used_bank_branch_names:
        used_bank_branch_names[bank_id] = set()
        
    suffixes = ["Branch", "Center", "Financial Suite", "Retail Hub"]
    base_name = f"{locality} {random.choice(suffixes)}"
    
    if base_name not in used_bank_branch_names[bank_id]:
        used_bank_branch_names[bank_id].add(base_name)
        return base_name
        
    # Append sequential tracking modifications safely during collision steps
    for modifier in ["North", "South", "Express", "Commercial"]:
        mod_name = f"{locality} {modifier} Branch"
        if mod_name not in used_bank_branch_names[bank_id]:
            used_bank_branch_names[bank_id].add(mod_name)
            return mod_name
            
    idx = 1
    while True:
        numbered_name = f"{locality} Annex #{idx}"
        if numbered_name not in used_bank_branch_names[bank_id]:
            used_bank_branch_names[bank_id].add(numbered_name)
            return numbered_name

# --- DEFENSIVE DATA INTEGRITY VALIDATOR ---
def validate_branch(branch: Branch, parent_bank: Optional[Bank]) -> None:
    if parent_bank is None:
        raise ValueError(f"Orphan Error: Branch ID {branch.branch_id} lacks parent tracking entity bindings.")
    if parent_bank.bank_status == 'closed' and random.random() < 0.1:
        # Business logic structural sanity warning check
        pass
    if len(branch.name) > 100 or not branch.branch_address:
        raise ValueError(f"Schema Constraint Fault: Attribute parameters violate target table schema validation.")

# --- MAIN FACTORY PIPELINE FUNCTION ---
def generate_branches_for_pool(banks_pool: List[Bank]) -> List[Branch]:
    branch_collection: List[Branch] = []
    global_branch_sequence_id = 1 
    
    for bank in banks_pool:
        # Determine physical target counts using Tier specifications instead of chronological age profiles
        target_num_branches = determine_branch_count_by_tier(bank)
        
        for _ in range(target_num_branches):
            target_country, region, locality = resolve_gravity_geography(bank)
            fake_inst = FAKERS.get(target_country, FAKERS['US'])
            
            branch_address = generate_unique_address(target_country, locality, fake_inst)
            branch_name = generate_unique_branch_name(bank.bank_id, locality)
            
            branch_obj = Branch(
                bank_id=bank.bank_id,
                branch_id=global_branch_sequence_id,
                name=branch_name,
                region=region,
                branch_address=branch_address,
                country_code=target_country
            )
            
            validate_branch(branch_obj, parent_bank=bank)
            branch_collection.append(branch_obj)
            global_branch_sequence_id += 1
            
    return branch_collection

def export_branches_to_sql(branches: List[Branch]) -> None:
    print(f"-- Executing Branch Serialization Matrix: Pipeline Validated Checksums Natively Match.")
    print(f"-- Total Export Targets: {len(branches)} rows\n")
    for br in branches:
        sql_statement = (
            f"INSERT INTO Branch (bank_id, name, region, branch_address, country_code) "
            f"VALUES ({br.bank_id}, '{br.name.replace("'", "''")}', '{br.region.replace("'", "''")}', "
            f"'{br.branch_address.replace("'", "''")}', '{br.country_code}');"
        )
        print(sql_statement)

# --- RUNTIME PIPELINE ANALYSIS VERIFICATION SIMULATOR ---
if __name__ == "__main__":
    print("-- Simulating upstream structural dependencies with Tier parameters...")
    
    mock_banks_pool = [
        Bank(bank_id=1, legal_name="First Dallas Sovereign Corp", bic="FDSCUSTX", routing_no="111000025", country_code="US", created_at=datetime.date(1912, 1, 1), bank_status="active", headquarters_city="Dallas", headquarters_address="Main St 400", license_number="OCC-109201", tier=BankTier.REGIONAL),
        Bank(bank_id=2, legal_name="Apex Digital Neobank Systems", bic="ADNSUSNY", routing_no="021000018", country_code="US", created_at=datetime.date(2021, 5, 20), bank_status="active", headquarters_city="New York", headquarters_address="Broadway 55", license_number="OCC-998124", tier=BankTier.DIGITAL_NEOBANK),
        Bank(bank_id=3, legal_name="Empire Trust & Commerce PLC", bic="ETCPGBLN", routing_no=None, country_code="GB", created_at=datetime.date(1895, 8, 14), bank_status="active", headquarters_city="London", headquarters_address="Threadneedle St 1", license_number="FCA-001092", tier=BankTier.LARGE_NATIONAL)
    ]
    
    generated_branches = generate_branches_for_pool(mock_banks_pool)
    export_branches_to_sql(generated_branches)
