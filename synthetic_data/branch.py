
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

@dataclass
class Branch:
    bank_id: int
    branch_id: int
    name: str            # Now strictly derived from City + Neighborhood/Modifier
    region: str          # ISO First Administrative Subdivision
    branch_address: str
    country_code: str

# --- RESOLVED GEOGRAPHIC MATRIX ---
# Maps an anchor city to its ISO state/province, plus realistic neighboring and far target cities


FOREIGN_CORRIDOR_WEIGHTS = {
    'US': {
        'targets': ['CA', 'DE', 'GB', 'TR'], 
        'weights': [0.60, 0.15, 0.20, 0.05]  
    },
    'DE': {
        'targets': ['GB', 'US', 'TR'],        # In a full dataset, this would include FR, CH, NL, BE
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

FAKERS: Dict[str, Faker] = {'US': Faker('en_US'), 'DE': Faker('de_DE')}
for fk in FAKERS.values():
    fk.seed_instance(GLOBAL_SEED)

# --- REVISED SCALE MATRIX BOUNDS ---
# Tuned to provide realistic density vectors for downstream dependent tables
TIER_FOOTPRINT_RULES = {
    BankTier.LARGE_NATIONAL: (250, 700),       # High-volume distribution nodes for retail giants
    BankTier.REGIONAL: (20, 80),              # Substantial multi-state or provincial coverage
    BankTier.COMMUNITY: (1, 8),                # Local town/county hyper-focus
    BankTier.PRIVATE_WEALTH: (1, 4),           # Limited high-end localized lounges
    BankTier.INVESTMENT_CORPORATE: (1, 3),    # Minimal presence strictly in global capital capitals
    BankTier.DIGITAL_NEOBANK: (0, 0)          # Headquarter only deployment models
    
    # --- INTERNATIONAL EXPANSION RATES BY TIER ---
# Dictates the probability that any single generated branch will land outside the home country
CROSS_BORDER_PROBABILITY = {
    BankTier.LARGE_NATIONAL: 0.05,        # 5% global hub footprint (e.g., Chase in London)
    BankTier.INVESTMENT_CORPORATE: 0.20,   # 20% global presence (offices in all financial capitals)
    BankTier.PRIVATE_WEALTH: 0.10,        # 10% elite offshore/international lounges
    BankTier.REGIONAL: 0.00,              # 0% Strict domestic multi-state focus
    BankTier.COMMUNITY: 0.00,             # 0% Purely local
    BankTier.DIGITAL_NEOBANK: 0.00         # 0% No physical retail international footprints
}
}

def determine_branch_count_by_tier(bank: Bank) -> int:
    """Calculates branch totals cleanly decoupled from age, matching core strategic intent."""
    min_b, max_b = TIER_FOOTPRINT_RULES[bank.tier]
    if min_b == 0 and max_b == 0:
        return 0 # Neo-banks use digital-only pipelines with no sub-branches
        
    base_count = random.randint(min_b, max_b)
    
    # Optional: We can still layer on your BranchStrategy multiplier 
    # to allow an aggressive community bank to outperform a boutique one.
    strategy_multipliers = {
        BranchStrategy.AGGRESSIVE_PHYSICAL: 1.2,
        BranchStrategy.BALANCED_HYBRID:     1.0,
        BranchStrategy.BOUTIQUE_MINIMAL:    0.4
    }
    
    multiplier = strategy_multipliers.get(bank.branch_strategy, 1.0)
    final_count = max(min_b, int(base_count * multiplier))
    
    # Hard cap at the top limit of the tier to preserve structural control
    return min(final_count, max_b)

def resolve_gravity_target(bank: Bank) -> Tuple[str, str, str, str]:
    """Determines target city using gravity weights, pulling metadata blueprints."""
    home_country = bank.country_code
    hq_city = bank.headquarters_city
    
    if bank.is_international and random.random() < 0.05:
        # Cross border rollout
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
    """Derives naming profiles from City hubs explicitly: e.g.

    'Frankfurt Westend Branch'.
    """
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

def generate_unique_address(country: str, city: str, modifier: str, fake: Faker) -> str:
    attempts = 0
    while attempts < 1000:
        street = fake.street_name()
        num = fake.building_number()
        addr = f"{street} {num}, {city}" if country == 'DE' else f"{num} {street}, {city} ({modifier})"
        
        if addr not in used_branch_addresses:
            used_branch_addresses.add(addr)
            return addr
        attempts += 1
    return f"{random.randint(1000, 9999)} Commerce St, {city}"

def generate_branches_for_pool(banks_pool: List[Bank]) -> List[Branch]:
    branch_collection: List[Branch] = []
    global_branch_sequence_id = 1 
    
    for bank in banks_pool:
        target_num_branches = determine_branch_count_by_tier(bank)
        
        for _ in range(target_num_branches):
            target_country, target_city, region, modifier = resolve_gravity_target(bank)
            fake_inst = FAKERS.get(target_country, FAKERS['US'])
            
            is_foreign = (target_country != bank.country_code)
            branch_name = generate_unique_branch_name(bank.bank_id, target_city, modifier, is_foreign)
            branch_address = generate_unique_address(target_country, target_city, modifier, fake_inst)
            
            branch_obj = Branch(
                bank_id=bank.bank_id,
                branch_id=global_branch_sequence_id,
                name=branch_name,
                region=region,
                branch_address=branch_address,
                country_code=target_country
            )
            
            branch_collection.append(branch_obj)
            global_branch_sequence_id += 1
            
    return branch_collection

def export_branches_to_sql(branches: List[Branch]) -> None:
    for br in branches:
        sql_statement = (
            f"INSERT INTO Branch (bank_id, name, region, branch_address, country_code) "
            f"VALUES ({br.bank_id}, '{br.name.replace("'", "''")}', '{br.region.replace("'", "''")}', "
            f"'{br.branch_address.replace("'", "''")}', '{br.country_code}');"
        )
        print(sql_statement)
        
        
def resolve_strict_geography(bank: Bank) -> Tuple[str, str, str, str]:
    """Determines target city using tier-based international gravity and regional trade corridors."""
    home_country = bank.country_code
    hq_city = bank.headquarters_city
    
    foreign_probability = CROSS_BORDER_PROBABILITY.get(bank.tier, 0.00)
    
    # 1. INTERNATIONAL ROUTING PIPELINE
    if bank.is_international and random.random() < foreign_probability:
        # Check if a custom economic corridor exists for the home country
        if home_country in FOREIGN_CORRIDOR_WEIGHTS:
            corridor = FOREIGN_CORRIDOR_WEIGHTS[home_country]
            target_country = random.choices(corridor['targets'], weights=corridor['weights'], k=1)[0]
        else:
            # Fallback allocation if country profile doesn't have explicit weights yet
            foreign_options = [c for c in CITY_CLUSTER_RULES.keys() if c != home_country]
            target_country = random.choice(foreign_options) if foreign_options else home_country
            
        # Target a primary financial hub city within that chosen target country
        target_city = random.choice(list(CITY_CLUSTER_RULES[target_country]['anchors'].keys()))
        
    # 2. DOMESTIC ROUTING PIPELINE (Anchored by proximity to HQ)
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
