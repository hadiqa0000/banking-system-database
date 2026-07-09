import random
import datetime
import string
from enum import Enum
from dataclasses import dataclass
from typing import List, Dict, Optional, Tuple
from faker import Faker

# --- ENGINE DETERMINISM SEEDING ---
GLOBAL_SEED = 42
random.seed(GLOBAL_SEED)
CURRENT_YEAR = datetime.date.today().year

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
    routing_no: Optional[str]
    country_code: str
    created_at: datetime.date
    bank_status: str
    headquarters_city: str
    headquarters_address: str
    license_number: str
    tier: BankTier 
    is_international: bool
    branch_strategy: BranchStrategy = BranchStrategy.BALANCED_HYBRID  # Added a safe default downstream matching your multiplier logic


@dataclass
class Branch:
    bank_id: int
    branch_id: int
    name: str
    region: str
    branch_address: str
    country_code: str
    branch_type: BranchType  # Moved downstream definitions above this step to resolve type lookup


# --- RESOLVED GEOGRAPHIC MATRIX ---
used_localized_addresses: Dict[Tuple[str, str], set] = {}
used_bank_city_names: Dict[Tuple[int, str], set] = {}

FAKERS: Dict[str, Faker] = {'US': Faker('en_US'), 'DE': Faker('de_DE')}
for fk in FAKERS.values():
    fk.seed_instance(GLOBAL_SEED)
    
BRANCH_TYPE_DISTRIBUTIONS = {
    BankTier.LARGE_NATIONAL: {
        'weights': [0.02, 0.60, 0.23, 0.15], 
        'types': [BranchType.FLAGSHIP, BranchType.FULL_SERVICE, BranchType.EXPRESS, BranchType.ATM_ONLY]
    },
    BankTier.REGIONAL: {
        'weights': [0.05, 0.70, 0.20, 0.05],
        'types': [BranchType.FLAGSHIP, BranchType.FULL_SERVICE, BranchType.EXPRESS, BranchType.ATM_ONLY]
    },
    BankTier.COMMUNITY: {
        'weights': [0.85, 0.15],
        'types': [BranchType.FULL_SERVICE, BranchType.EXPRESS] 
    },
    BankTier.INVESTMENT_CORPORATE: {
        'weights': [1.00],
        'types': [BranchType.FLAGSHIP] 
    }
}

FOREIGN_CORRIDOR_WEIGHTS = {
    'US': {
        'targets': ['CA', 'DE', 'GB', 'TR'], 
        'weights': [0.60, 0.15, 0.20, 0.05]  
    },
    'DE': {
        'targets': ['GB', 'US', 'TR'],        
        'weights': [0.50, 0.35, 0.15]  
    },
    'GB': {
        'targets': ['US', 'DE', 'TR'],
        'weights': [0.45, 0.45, 0.10]    
    },
    'TR': {
        'targets': ['DE', 'GB', 'US'],
        'weights': [0.55, 0.25, 0.20]    
    }
}

CITY_CLUSTER_RULES = {
    'US': {
        'anchors': {
            'New York': {'region': 'New York', 'adjacent_cities': ['Philadelphia', 'Boston'], 'far_cities': ['Los Angeles', 'Dallas', 'Miami']},
            'Chicago': {'region': 'Illinois', 'adjacent_cities': ['Indianapolis', 'Milwaukee', 'Detroit'], 'far_cities': ['New York', 'Los Angeles', 'Houston']},
            'Charlotte': {'region': 'North Carolina', 'adjacent_cities': ['Charleston', 'Richmond', 'Atlanta'], 'far_cities': ['New York', 'Miami', 'Chicago']},
            'San Francisco': {'region': 'California', 'adjacent_cities': ['Las Vegas', 'Phoenix', 'Seattle'], 'far_cities': ['New York', 'Dallas', 'Chicago']},
            'Dallas': {'region': 'Texas', 'adjacent_cities': ['Oklahoma City', 'New Orleans', 'Albuquerque'], 'far_cities': ['New York', 'Los Angeles', 'Miami']}
        },
        'city_metadata': {
            'New York': ('New York', ['Downtown', 'Wall Street', 'Brooklyn Heights', 'Midtown']),
            'Philadelphia': ('Pennsylvania', ['Center City', 'Northeast', 'University City']),
            'Boston': ('Massachusetts', ['Back Bay', 'Financial District', 'Cambridge']),
            'Los Angeles': ('California', ['Downtown', 'Century City', 'Santa Monica', 'Pasadena']),
            'Dallas': ('Texas', ['Uptown', 'Downtown', 'North Park', 'Galleria']),
            'Miami': ('Florida', ['Brickell', 'South Beach', 'Coral Gables']),
            'Chicago': ('Illinois', ['The Loop', 'Lincoln Park', 'River North']),
            'Indianapolis': ('Indiana', ['Downtown', 'Meridian Hills']),
            'Milwaukee': ('Wisconsin', ['Downtown', 'Third Ward']),
            'Detroit': ('Michigan', ['Downtown', 'Midtown']),
            'Houston': ('Texas', ['Galleria', 'Downtown', 'Medical Center']),
            'Charleston': ('South Carolina', ['Historic District', 'North Charleston']),
            'Richmond': ('Virginia', ['Downtown', 'West End']),
            'Atlanta': ('Georgia', ['Buckhead', 'Midtown', 'Downtown']),
            'Las Vegas': ('Nevada', ['The Strip', 'Downtown', 'Summerlin']),
            'Phoenix': ('Arizona', ['Downtown', 'Scottsdale', 'Camelback']),
            'Seattle': ('Washington', ['Downtown', 'Capitol Hill', 'South Lake Union']),
            'Oklahoma City': ('Oklahoma', ['Downtown', 'Bricktown']),
            'New Orleans': ('Louisiana', ['French Quarter', 'Garden District']),
            'Albuquerque': ('New Mexico', ['Downtown', 'Nob Hill'])
        }
    },
    'DE': {
        'anchors': {
            'Frankfurt': {'region': 'Hesse', 'adjacent_cities': ['Mainz', 'Wiesbaden'], 'far_cities': ['Berlin', 'Munich', 'Hamburg']},
            'Munich': {'region': 'Bavaria', 'adjacent_cities': ['Stuttgart', 'Nuremberg'], 'far_cities': ['Berlin', 'Frankfurt', 'Hamburg']},
            'Berlin': {'region': 'Berlin', 'adjacent_cities': ['Potsdam', 'Leipzig'], 'far_cities': ['Frankfurt', 'Munich', 'Hamburg']},
            'Hamburg': {'region': 'Hamburg', 'adjacent_cities': ['Hannover', 'Kiel'], 'far_cities': ['Frankfurt', 'Munich', 'Berlin']}
        },
        'city_metadata': {
            'Frankfurt': ('Hesse', ['Innenstadt', 'Westend', 'Sachsenhausen']),
            'Mainz': ('Rhineland-Palatinate', ['Zentrum', 'Neustadt']),
            'Wiesbaden': ('Hesse', ['Mitte', 'Rheingauviertel']),
            'Berlin': ('Berlin', ['Mitte', 'Charlottenburg', 'Kreuzberg']),
            'Munich': ('Bavaria', ['Altstadt', 'Schwabing', 'Maxvorstadt']),
            'Hamburg': ('Hamburg', ['HafenCity', 'Altona', 'Sankt Pauli']),
            'Stuttgart': ('Baden-Württemberg', ['Mitte', 'West']),
            'Nuremberg': ('Bavaria', ['Altstadt', 'Südstadt']),
            'Potsdam': ('Brandenburg', ['Zentrum', 'Babelsberg']),
            'Leipzig': ('Saxony', ['Mitte', 'Plagwitz']),
            'Hannover': ('Lower Saxony', ['Mitte', 'List']),
            'Kiel': ('Schleswig-Holstein', ['Mitte', 'Wik'])
        }
    }
}

used_bank_branch_names: Dict[int, set] = {}
used_branch_addresses: set = {}

# --- REVISED SCALE MATRIX BOUNDS ---
TIER_FOOTPRINT_RULES = {
    BankTier.LARGE_NATIONAL: (250, 700),      
    BankTier.REGIONAL: (20, 80),              
    BankTier.COMMUNITY: (1, 8),               
    BankTier.PRIVATE_WEALTH: (1, 4),          
    BankTier.INVESTMENT_CORPORATE: (1, 3),    
    BankTier.DIGITAL_NEOBANK: (0, 0)          
}

# Fixed closing brace placement so this mapping is properly exposed
CROSS_BORDER_PROBABILITY = {
    BankTier.LARGE_NATIONAL: 0.05,        
    BankTier.INVESTMENT_CORPORATE: 0.20,   
    BankTier.PRIVATE_WEALTH: 0.10,        
    BankTier.REGIONAL: 0.00,              
    BankTier.COMMUNITY: 0.00,             
    BankTier.DIGITAL_NEOBANK: 0.00         
}

def determine_branch_count_by_tier(bank: Bank) -> int:
    min_b, max_b = TIER_FOOTPRINT_RULES[bank.tier]
    if min_b == 0 and max_b == 0:
        return 0 
        
    base_count = random.randint(min_b, max_b)
    
    strategy_multipliers = {
        BranchStrategy.AGGRESSIVE_PHYSICAL: 1.2,
        BranchStrategy.BALANCED_HYBRID:     1.0,
        BranchStrategy.BOUTIQUE_MINIMAL:    0.4
    }
    
    multiplier = strategy_multipliers.get(bank.branch_strategy, 1.0)
    final_count = max(min_b, int(base_count * multiplier))
    
    return min(final_count, max_b)

def resolve_gravity_target(bank: Bank) -> Tuple[str, str, str, str]:
    home_country = bank.country_code
    hq_city = bank.headquarters_city
    
    if bank.is_international and random.random() < 0.05:
        foreign_countries = [c for c in CITY_CLUSTER_RULES.keys() if c != home_country]
        target_country = random.choice(foreign_countries)
        target_city = random.choice(list(CITY_CLUSTER_RULES[target_country]['anchors'].keys()))
    else:
        target_country = home_country
        if target_country not in CITY_CLUSTER_RULES or hq_city not in CITY_CLUSTER_RULES[target_country]['anchors']:
            return target_country, hq_city, "Standard District", "Main Hub"
            
        cluster = CITY_CLUSTER_RULES[target_country]['anchors'][hq_city]
        
        roll = random.random()
        if roll < 0.60:
            target_city = hq_city
        elif roll < 0.90:
            target_city = random.choice(cluster['adjacent_cities'])
        else:
            target_city = random.choice(cluster['far_cities'])
            
    region, modifiers = CITY_CLUSTER_RULES[target_country]['city_metadata'][target_city]
    chosen_modifier = random.choice(modifiers)
    
    return target_country, target_city, region, chosen_modifier

def generate_unique_branch_name(bank_id: int, city: str, modifier: str, is_foreign: bool) -> str:
    if bank_id not in used_bank_branch_names:
        used_bank_branch_names[bank_id] = set()
        
    suffix = "International Hub" if is_foreign else random.choice(["Branch", "Center", "Financial Suite"])
    base_name = f"{city} {modifier} {suffix}"
    
    if base_name not in used_bank_branch_names[bank_id]:
        used_bank_branch_names[bank_id].add(base_name)
        return base_name
        
    for alt in ["North", "South", "Central"]:
        alt_name = f"{city} {modifier} {alt} {suffix}"
        if alt_name not in used_bank_branch_names[bank_id]:
            used_bank_branch_names[bank_id].add(alt_name)
            return alt_name
            
    idx = 1
    while True:
        numbered_name = f"{city} {modifier} #{idx} {suffix}"
        if numbered_name not in used_bank_branch_names[bank_id]:
            used_bank_branch_names[bank_id].add(numbered_name)
            return numbered_name

def generate_localized_unique_address(country: str, city: str, modifier: str, fake: Faker) -> str:
    geo_scope_key = (country, city)
    if geo_scope_key not in used_localized_addresses:
        used_localized_addresses[geo_scope_key] = set()
        
    attempts = 0
    while attempts < 1000:
        street = fake.street_name()
        num = fake.building_number()
        
        raw_address_line = f"{street} {num}" if country == 'DE' else f"{num} {street}"
        
        if raw_address_line not in used_localized_addresses[geo_scope_key]:
            used_localized_addresses[geo_scope_key].add(raw_address_line)
            return f"{raw_address_line}, {city}" if country == 'DE' else f"{raw_address_line}, {city} ({modifier})"
            
        attempts += 1
    return f"{random.randint(1000, 9999)} Commerce St, {city}"

def generate_branches_for_pool(banks_pool: List[Bank]) -> List[Branch]:
    branch_collection: List[Branch] = []
    global_branch_sequence_id = 1 
    
    for bank in banks_pool:
        if bank.tier == BankTier.DIGITAL_NEOBANK:
            continue
            
        total_capacity = determine_branch_count_by_tier(bank)
        
        hq_region, modifiers = CITY_CLUSTER_RULES[bank.country_code]['city_metadata'][bank.headquarters_city]
        hq_address = generate_localized_unique_address(bank.country_code, bank.headquarters_city, modifiers[0], FAKERS[bank.country_code])
        
        hq_branch = Branch(
            bank_id=bank.bank_id,
            branch_id=global_branch_sequence_id,
            name=f"{bank.headquarters_city} Corporate Headquarters",
            region=hq_region,
            branch_address=hq_address,
            country_code=bank.country_code,
            branch_type=BranchType.HEADQUARTERS
        )
        branch_collection.append(hq_branch)
        global_branch_sequence_id += 1
        
        if total_capacity <= 1:
            continue
            
        dist = BRANCH_TYPE_DISTRIBUTIONS[bank.tier]
        
        for _ in range(total_capacity - 1):
            target_country, target_city, region, modifier = resolve_gravity_target(bank)
            fake_inst = FAKERS.get(target_country, FAKERS['US'])
            
            chosen_type = random.choices(dist['types'], weights=dist['weights'], k=1)[0]
            
            is_foreign = (target_country != bank.country_code)
            base_name = generate_unique_branch_name(bank.bank_id, target_city, modifier, is_foreign)
            if chosen_type == BranchType.EXPRESS:
                base_name = base_name.replace("Branch", "Express Kiosk")
            elif chosen_type == BranchType.ATM_ONLY:
                base_name = base_name.replace("Branch", "Automated Teller Vault")
                
            branch_address = generate_localized_unique_address(target_country, target_city, modifier, fake_inst)
            
            branch_obj = Branch(
                bank_id=bank.bank_id,
                branch_id=global_branch_sequence_id,
                name=base_name,
                region=region,
                branch_address=branch_address,
                country_code=target_country,
                branch_type=chosen_type
            )
            
            branch_collection.append(branch_obj)
            global_branch_sequence_id += 1
            
    return branch_collection
    
def generate_natural_branch_name(bank_id: int, city: str, modifier: str) -> str:
    bank_city_scope = (bank_id, city)
    if bank_city_scope not in used_bank_city_names:
        used_bank_city_names[bank_city_scope] = set()

    base_proposal = f"{city} {modifier} Branch"
    if base_proposal not in used_bank_city_names[bank_city_scope]:
        used_bank_city_names[bank_city_scope].add(base_proposal)
        return base_proposal

    directional_markers = ["North", "South", "East", "West", "Airport", "Medical District", "Financial Center"]
    for marker in directional_markers:
        marker_proposal = f"{city} {marker} Branch"
        if marker_proposal not in used_bank_city_names[bank_city_scope]:
            used_bank_city_names[bank_city_scope].add(marker_proposal)
            return marker_proposal

    roman_numerals = ["II", "III", "IV", "V", "VI", "VII"]
    for roman in roman_numerals:
        numeral_proposal = f"{city} {modifier} Branch {roman}"
        if numeral_proposal not in used_bank_city_names[bank_city_scope]:
            used_bank_city_names[bank_city_scope].add(numeral_proposal)
            return numeral_proposal

    idx = 1
    while True:
        fallback_proposal = f"{city} {modifier} Branch #{idx}"
        if fallback_proposal not in used_bank_city_names[bank_city_scope]:
            used_bank_city_names[bank_city_scope].add(fallback_proposal)
            return fallback_proposal

def export_branches_to_sql(branches: List[Branch]) -> None:
    for br in branches:
        # Replaced outer quotes with single quotes to fix string parsing syntax error
        name_escaped = br.name.replace("'", "''")
        region_escaped = br.region.replace("'", "''")
        addr_escaped = br.branch_address.replace("'", "''")
        
        sql_statement = (
            f"INSERT INTO Branch (bank_id, name, region, branch_address, country_code) "
            f"VALUES ({br.bank_id}, '{name_escaped}', '{region_escaped}', "
            f"'{addr_escaped}', '{br.country_code}');"
        )
        print(sql_statement)
        
        
def resolve_strict_geography(bank: Bank) -> Tuple[str, str, str, str]:
    home_country = bank.country_code
    hq_city = bank.headquarters_city
    
    foreign_probability = CROSS_BORDER_PROBABILITY.get(bank.tier, 0.00)
    
    if bank.is_international and random.random() < foreign_probability:
        if home_country in FOREIGN_CORRIDOR_WEIGHTS:
            corridor = FOREIGN_CORRIDOR_WEIGHTS[home_country]
            target_country = random.choices(corridor['targets'], weights=corridor['weights'], k=1)[0]
        else:
            foreign_options = [c for c in CITY_CLUSTER_RULES.keys() if c != home_country]
            target_country = random.choice(foreign_options) if foreign_options else home_country
            
        target_city = random.choice(list(CITY_CLUSTER_RULES[target_country]['anchors'].keys()))
        
    else:
        target_country = home_country
        if target_country not in CITY_CLUSTER_RULES or hq_city not in CITY_CLUSTER_RULES[target_country]['anchors']:
            return target_country, hq_city, "Standard District", "Main Hub"
            
        cluster = CITY_CLUSTER_RULES[target_country]['anchors'][hq_city]
        
        roll = random.random()
        if roll < 0.60:
            target_city = hq_city
        elif roll < 0.90:
            target_city = random.choice(cluster['adjacent_cities'])
        else:
            target_city = random.choice(cluster['far_cities'])
            
    region, modifiers = CITY_CLUSTER_RULES[target_country]['city_metadata'][target_city]
    chosen_modifier = random.choice(modifiers)
    
    return target_country, target_city, region, chosen_modifier

# --- PIPELINE DEMO ---
if __name__ == "__main__":
    mock_banks = [
        Bank(bank_id=1, legal_name="Lone Star Community Bank", bic="LSCUSTX1", routing_no="111000025", country_code="US", created_at=datetime.date(2015, 5, 10), bank_status="active", headquarters_city="Dallas", headquarters_address="Main St 200", license_number="OCC-88219", tier=BankTier.COMMUNITY, is_international=False),
        Bank(bank_id=2, legal_name="Deutsche Continental AG", bic="DCONDEFF", routing_no=None, country_code="DE", created_at=datetime.date(1990, 1, 1), bank_status="active", headquarters_city="Frankfurt", headquarters_address="Taunusanlage 12", license_number="BAFIN-9921", tier=BankTier.REGIONAL, is_international=True)
    ]
    
    export_branches_to_sql(generate_branches_for_pool(mock_banks))
