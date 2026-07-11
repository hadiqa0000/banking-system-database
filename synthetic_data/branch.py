import random
import datetime
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
    license_number: str
    tier: BankTier 
    is_international: bool
    headquarters_city: str  
    branch_strategy: BranchStrategy = BranchStrategy.BALANCED_HYBRID


@dataclass
class Branch:
    bank_id: int
    name: str
    region: str
    city: str               
    branch_address: str
    country_code: str
    branch_type: BranchType


# --- GEOGRAPHIC REGIONAL MATRIX ---
used_localized_addresses: Dict[Tuple[str, str], set] = {}
used_bank_city_names: Dict[Tuple[int, str], set] = {}

FAKERS: Dict[str, Faker] = {'US': Faker('en_US'), 'DE': Faker('de_DE')}
for fk in FAKERS.values():
    fk.seed_instance(GLOBAL_SEED)
    
BRANCH_TYPE_DISTRIBUTIONS = {
    BankTier.LARGE_NATIONAL: {
        # Streamlined ATM distribution down to 5% to match industry asset tracking profiles
        'weights': [0.05, 0.65, 0.25, 0.05], 
        'types': [BranchType.FLAGSHIP, BranchType.FULL_SERVICE, BranchType.EXPRESS, BranchType.ATM_ONLY]
    },
    BankTier.REGIONAL: {
        'weights': [0.05, 0.70, 0.22, 0.03],
        'types': [BranchType.FLAGSHIP, BranchType.FULL_SERVICE, BranchType.EXPRESS, BranchType.ATM_ONLY]
    },
    BankTier.COMMUNITY: {
        'weights': [0.85, 0.15],
        'types': [BranchType.FULL_SERVICE, BranchType.EXPRESS] 
    },
    BankTier.INVESTMENT_CORPORATE: {
        'weights': [1.00],
        'types': [BranchType.FLAGSHIP] 
    },
    BankTier.PRIVATE_WEALTH: {
        'weights': [1.00],
        'types': [BranchType.FLAGSHIP]
    },
    BankTier.DIGITAL_NEOBANK: {
        'weights': [],
        'types': []
    }
}


# Quick ISO region mapping to append true state/postal region short-codes for US/GB
STATE_REGION_CODES = {
    'New York': 'NY', 'Illinois': 'IL', 'California': 'CA', 'Texas': 'TX', 'North Carolina': 'NC',
    'Greater London': 'LND', 'Berkshire': 'BRK', 'East Sussex': 'SSX', 'Greater Manchester': 'GMC',
    'Merseyside': 'MSY', 'West Yorkshire': 'WYK', 'West Midlands': 'WMD', 'Midlothian': 'MLN',
    'Lanarkshire': 'LNK', 'Bristol': 'BST'
}

FOREIGN_CORRIDOR_WEIGHTS = {
    'US': { 'targets': ['CA', 'DE', 'GB', 'TR'], 'weights': [0.60, 0.15, 0.20, 0.05] },
    'DE': { 'targets': ['GB', 'US', 'TR'], 'weights': [0.50, 0.35, 0.15] },
    'GB': { 'targets': ['US', 'DE', 'TR'], 'weights': [0.45, 0.45, 0.10] },
    'TR': { 'targets': ['DE', 'GB', 'US'], 'weights': [0.55, 0.25, 0.20] }
}

CITY_CLUSTER_RULES = {
    'US': {
        'anchors': {
            'New York': {'weight': 0.65, 'region': 'New York', 'adjacent_cities': ['Philadelphia', 'Boston'], 'far_cities': ['Los Angeles', 'Dallas', 'Miami']},
            'Chicago': {'weight': 0.15, 'region': 'Illinois', 'adjacent_cities': ['Indianapolis', 'Milwaukee', 'Detroit'], 'far_cities': ['New York', 'Los Angeles', 'Houston']},
            'San Francisco': {'weight': 0.10, 'region': 'California', 'adjacent_cities': ['Las Vegas', 'Phoenix', 'Seattle'], 'far_cities': ['New York', 'Dallas', 'Chicago']},
            'Dallas': {'weight': 0.06, 'region': 'Texas', 'adjacent_cities': ['Oklahoma City', 'New Orleans', 'Albuquerque'], 'far_cities': ['New York', 'Los Angeles', 'Miami']},
            'Charlotte': {'weight': 0.04, 'region': 'North Carolina', 'adjacent_cities': ['Charleston', 'Richmond', 'Atlanta'], 'far_cities': ['New York', 'Miami', 'Chicago']}
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
            'Frankfurt': {'weight': 0.60, 'region': 'Hesse', 'adjacent_cities': ['Mainz', 'Wiesbaden'], 'far_cities': ['Berlin', 'Munich', 'Hamburg']},
            'Berlin': {'weight': 0.20, 'region': 'Berlin', 'adjacent_cities': ['Potsdam', 'Leipzig'], 'far_cities': ['Frankfurt', 'Munich', 'Hamburg']},
            'Munich': {'weight': 0.15, 'region': 'Bavaria', 'adjacent_cities': ['Stuttgart', 'Nuremberg'], 'far_cities': ['Berlin', 'Frankfurt', 'Hamburg']},
            'Hamburg': {'weight': 0.05, 'region': 'Hamburg', 'adjacent_cities': ['Hannover', 'Kiel'], 'far_cities': ['Frankfurt', 'Munich', 'Berlin']}
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
    },
    'GB': {  # Added missing GB entry
        'anchors': {
            'London': {'weight': 0.70, 'region': 'Greater London', 'adjacent_cities': ['Bristol', 'Reading'], 'far_cities': ['Manchester', 'Birmingham']},
            'Manchester': {'weight': 0.15, 'region': 'Greater Manchester', 'adjacent_cities': ['Liverpool', 'Leeds'], 'far_cities': ['London', 'Edinburgh']},
            'Edinburgh': {'weight': 0.10, 'region': 'Midlothian', 'adjacent_cities': ['Glasgow', 'Dundee'], 'far_cities': ['London', 'Birmingham']},
            'Birmingham': {'weight': 0.05, 'region': 'West Midlands', 'adjacent_cities': ['Nottingham', 'Coventry'], 'far_cities': ['London', 'Manchester']}
        },
        'city_metadata': {
            'London': ('Greater London', ['City of London', 'Canary Wharf', 'Mayfair', 'Soho']),
            'Manchester': ('Greater Manchester', ['City Centre', 'Salford Quays', 'Spinningfields']),
            'Edinburgh': ('Midlothian', ['New Town', 'Old Town', 'Leith']),
            'Birmingham': ('West Midlands', ['City Centre', 'Brindleyplace', 'Jewellery Quarter']),
            'Bristol': ('Bristol', ['City Centre', 'Harbourside', 'Clifton']),
            'Reading': ('Berkshire', ['Town Centre', 'Reading Green Park']),
            'Liverpool': ('Merseyside', ['City Centre', 'Albert Dock']),
            'Leeds': ('West Yorkshire', ['City Centre', 'Leeds Dock']),
            'Glasgow': ('Lanarkshire', ['City Centre', 'West End']),
            'Dundee': ('Angus', ['City Centre', 'Docks']),
            'Nottingham': ('Nottinghamshire', ['City Centre', 'Lace Market']),
            'Coventry': ('West Midlands', ['City Centre', 'University Quarter'])
        }
    },
    'TR': {  # Added missing TR entry for completeness
        'anchors': {
            'Istanbul': {'weight': 0.70, 'region': 'Marmara', 'adjacent_cities': ['Ankara', 'Izmir'], 'far_cities': ['Antalya', 'Bursa']},
            'Ankara': {'weight': 0.20, 'region': 'Central Anatolia', 'adjacent_cities': ['Konya', 'Eskisehir'], 'far_cities': ['Istanbul', 'Izmir']},
            'Izmir': {'weight': 0.10, 'region': 'Aegean', 'adjacent_cities': ['Aydin', 'Manisa'], 'far_cities': ['Istanbul', 'Antalya']}
        },
        'city_metadata': {
            'Istanbul': ('Marmara', ['Levent', 'Maslak', 'Taksim', 'Besiktas']),
            'Ankara': ('Central Anatolia', ['Kizilay', 'Cankaya', 'Sogutozu']),
            'Izmir': ('Aegean', ['Alsancak', 'Konak', 'Bornova']),
            'Antalya': ('Mediterranean', ['Konyaalti', 'Lara']),
            'Bursa': ('Marmara', ['Nilufer', 'Osmangazi']),
            'Konya': ('Central Anatolia', ['Selcuklu', 'Meram']),
            'Eskisehir': ('Central Anatolia', ['Odunpazari', 'Tepebasi']),
            'Aydin': ('Aegean', ['Efeler', 'Kusadasi']),
            'Manisa': ('Aegean', ['Soma', 'Turgutlu'])
        }
    }
}

TIER_FOOTPRINT_GAUSSIAN_RULES = {
    BankTier.LARGE_NATIONAL: (250, 700, 450, 65),      
    BankTier.REGIONAL: (20, 80, 35, 8),                
    BankTier.COMMUNITY: (1, 8, 2.8, 1.1),              
    BankTier.PRIVATE_WEALTH: (1, 4, 2, 0.8),          
    BankTier.INVESTMENT_CORPORATE: (1, 3, 2, 0.5),    
    BankTier.DIGITAL_NEOBANK: (0, 0, 0, 0)          
}

BANK_LEVEL_INTERNATIONAL_PROBABILITY = {
    BankTier.LARGE_NATIONAL: 0.40,         
    BankTier.INVESTMENT_CORPORATE: 0.85,   
    BankTier.PRIVATE_WEALTH: 0.30,        
    BankTier.REGIONAL: 0.05,               
    BankTier.COMMUNITY: 0.00,             
    BankTier.DIGITAL_NEOBANK: 0.00         
}

def determine_branch_count_by_tier(bank: Bank) -> int:
    min_b, max_b, mu, sigma = TIER_FOOTPRINT_GAUSSIAN_RULES[bank.tier]
    if min_b == 0 and max_b == 0:
        return 0 
        
    base_count = int(random.gauss(mu, sigma))
    strategy_multipliers = {
        BranchStrategy.AGGRESSIVE_PHYSICAL: 1.2,
        BranchStrategy.BALANCED_HYBRID:     1.0,
        BranchStrategy.BOUTIQUE_MINIMAL:    0.4
    }
    multiplier = strategy_multipliers.get(bank.branch_strategy, 1.0)
    return min(max(min_b, int(base_count * multiplier)), max_b)
    
    
def generate_localized_unique_address(country: str, city: str, modifier: str, fake: Faker) -> str:
    geo_scope_key = (country, city)
    if geo_scope_key not in used_localized_addresses:
        used_localized_addresses[geo_scope_key] = set()
        
    attempts = 0
    while attempts < 1000:
        street = fake.street_name()
        num = fake.building_number()
        
        # Construct realistic, clean domestic standard string lines without weird parentheses
        if country == 'US':
            state_code = STATE_REGION_CODES.get(modifier, 'USA')
            # Format: 123 Wall Street, Midtown, New York, NY
            address_formatted = f"{num} {street}, {modifier}, {city}, {state_code}"
            
        elif country == 'GB':
            region_name = list(CITY_CLUSTER_RULES['GB']['anchors'].get(city, {'region': 'UK'}).values())[1] if city in CITY_CLUSTER_RULES['GB']['anchors'] else 'UK'
            # Format: 40 Canary Wharf, London, Greater London
            address_formatted = f"{num} {street}, {modifier}, {city}, {region_name}"
            
        elif country == 'DE':
            # Format: Innenstadt, Westendstraße 44, Frankfurt
            address_formatted = f"{street} {num}, {modifier}, {city}"
            
        elif country == 'TR':
            # Format: Levent Mh., Nispetiye Sk. No: 12, Istanbul
            address_formatted = f"{modifier} Mh., {street} Sk. No: {num}, {city}"
            
        else:
            address_formatted = f"{num} {street}, {city}"
        
        if address_formatted not in used_localized_addresses[geo_scope_key]:
            used_localized_addresses[geo_scope_key].add(address_formatted)
            return address_formatted
        attempts += 1
        
    return f"100 Financial Way, {modifier}, {city}"

def generate_natural_branch_name(bank_id: int, city: str, modifier: str, is_foreign: bool, branch_type: BranchType) -> str:
    bank_city_scope = (bank_id, city)
    if bank_city_scope not in used_bank_city_names:
        used_bank_city_names[bank_city_scope] = set()

    if branch_type == BranchType.HEADQUARTERS:
        suffix = "Corporate Headquarters"
    elif is_foreign:
        foreign_mapping = {
            BranchType.FLAGSHIP: "International Office",
            BranchType.FULL_SERVICE: "Foreign Branch",
            BranchType.EXPRESS: "Representative Office",  
            BranchType.ATM_ONLY: "ATM Center"              
        }
        suffix = foreign_mapping.get(branch_type, "Foreign Branch")
    else:
        domestic_mapping = {
            BranchType.FLAGSHIP: "Flagship Center",
            BranchType.FULL_SERVICE: "Branch",
            BranchType.EXPRESS: "Express Branch",          
            BranchType.ATM_ONLY: "ATM Center"              
        }
        suffix = domestic_mapping.get(branch_type, "Branch")

    if branch_type in [BranchType.HEADQUARTERS] or (is_foreign and branch_type == BranchType.FLAGSHIP):
        proposal = f"{city} {suffix}"
        if proposal not in used_bank_city_names[bank_city_scope]:
            used_bank_city_names[bank_city_scope].add(proposal)
            return proposal

    base_proposal = f"{city} {modifier} {suffix}"
    if base_proposal not in used_bank_city_names[bank_city_scope]:
        used_bank_city_names[bank_city_scope].add(base_proposal)
        return base_proposal

    directional_markers = ["North", "South", "East", "West", "Financial District", "Metro Mall"]
    for marker in directional_markers:
        marker_proposal = f"{city} {marker} {suffix}"
        if marker_proposal not in used_bank_city_names[bank_city_scope]:
            used_bank_city_names[bank_city_scope].add(marker_proposal)
            return marker_proposal

    idx = 1
    while True:
        fallback_proposal = f"{city} {modifier} {suffix} #{idx}"
        if fallback_proposal not in used_bank_city_names[bank_city_scope]:
            used_bank_city_names[bank_city_scope].add(fallback_proposal)
            return fallback_proposal
        idx += 1  # Fixed: removed trailing '=' and added increment

def validate_branch_integrity(branch: Branch) -> None:
    """Rigid validation pass checking code types before writing execution files."""
    assert branch.bank_id > 0, f"Malformed Bank Reference ID: {branch.bank_id}"
    assert len(branch.country_code) == 2, f"Invalid ISO Country Code Format: {branch.country_code}"
    assert branch.name.strip(), "Branch name string field cannot be blank."
    assert branch.city.strip(), "City structural field variant cannot be blank."
    assert branch.region.strip(), "Regional geographic tracking component cannot be blank."
    assert branch.branch_address.strip(), "Physical location text line address missing."
    assert isinstance(branch.branch_type, BranchType), "Unrecognized object enum branch variant type"
    assert branch.country_code in CITY_CLUSTER_RULES, f"Country {branch.country_code} not in CITY_CLUSTER_RULES"
    assert branch.city in CITY_CLUSTER_RULES[branch.country_code]["city_metadata"], f"City {branch.city} not found in metadata for {branch.country_code}"

def generate_branches_for_pool(banks_pool: List[Bank]) -> List[Branch]:
    branch_collection: List[Branch] = []
    
    for bank in banks_pool:
        if bank.tier == BankTier.DIGITAL_NEOBANK:
            continue
            
        total_capacity = determine_branch_count_by_tier(bank)
        hq_city = bank.headquarters_city
        
        # 1. MATERIALIZE TRUE CORPORATE HQ ROW FIRST
        hq_region, modifiers = CITY_CLUSTER_RULES[bank.country_code]['city_metadata'][hq_city]
        hq_address = generate_localized_unique_address(bank.country_code, hq_city, modifiers[0], FAKERS[bank.country_code])
        hq_name = generate_natural_branch_name(bank.bank_id, hq_city, modifiers[0], False, BranchType.HEADQUARTERS)
        
        hq_branch = Branch(
            bank_id=bank.bank_id, name=hq_name, region=hq_region, city=hq_city, 
            branch_address=hq_address, country_code=bank.country_code, branch_type=BranchType.HEADQUARTERS
        )
        validate_branch_integrity(hq_branch)
        branch_collection.append(hq_branch)
        
        if total_capacity <= 1:
            continue
            
        # 2. RUN CORPORATE EXPANSION POLICY OVER ONCE PER BANK
        has_global_presence = (
            bank.is_international and 
            random.random() < BANK_LEVEL_INTERNATIONAL_PROBABILITY.get(bank.tier, 0.00)
        )
        
        foreign_branch_budget = 0
        if has_global_presence:
            if bank.tier in [BankTier.LARGE_NATIONAL, BankTier.INVESTMENT_CORPORATE]:
                foreign_branch_budget = random.randint(5, 30)
            else:
                foreign_branch_budget = random.randint(1, 3)
            foreign_branch_budget = min(foreign_branch_budget, total_capacity - 1)

        # 3. FILL BALANCED RETAIL NETWORK
        dist = BRANCH_TYPE_DISTRIBUTIONS[bank.tier]
        for _ in range(total_capacity - 1):
            if foreign_branch_budget > 0:
                is_foreign = True
                foreign_branch_budget -= 1
            else:
                is_foreign = False

            if is_foreign:
                home_country = bank.country_code
                if home_country in FOREIGN_CORRIDOR_WEIGHTS:
                    corridor = FOREIGN_CORRIDOR_WEIGHTS[home_country]
                    target_country = random.choices(corridor['targets'], weights=corridor['weights'], k=1)[0]
                else:
                    foreign_options = [c for c in CITY_CLUSTER_RULES.keys() if c != home_country]
                    target_country = random.choice(foreign_options) if foreign_options else home_country
                    
                # Upgraded: Non-uniform city selection rules applied smoothly
                anchors_dict = CITY_CLUSTER_RULES[target_country]['anchors']
                cities_list = list(anchors_dict.keys())
                city_weights = [anchors_dict[city]['weight'] for city in cities_list]
                
                target_city = random.choices(cities_list, weights=city_weights, k=1)[0]
                region, modifiers = CITY_CLUSTER_RULES[target_country]['city_metadata'][target_city]
                modifier = random.choice(modifiers)
            else:
                target_country = bank.country_code
                cluster = CITY_CLUSTER_RULES[target_country]['anchors'][hq_city]
                roll = random.random()
                if roll < 0.60:
                    target_city = hq_city
                elif roll < 0.90:
                    target_city = random.choice(cluster['adjacent_cities'])
                else:
                    target_city = random.choice(cluster['far_cities'])
                region, modifiers = CITY_CLUSTER_RULES[target_country]['city_metadata'][target_city]
                modifier = random.choice(modifiers)

            # Ensure we have a valid Faker instance
            fake_inst = FAKERS.get(target_country, FAKERS['US'])
            
            # Ensure we have valid branch types and weights
            if not dist['types'] or not dist['weights']:
                # Fallback for empty distributions
                chosen_type = BranchType.FULL_SERVICE
            else:
                chosen_type = random.choices(dist['types'], weights=dist['weights'], k=1)[0]
            
            branch_name = generate_natural_branch_name(bank.bank_id, target_city, modifier, is_foreign, chosen_type)
            branch_address = generate_localized_unique_address(target_country, target_city, modifier, fake_inst)
            
            branch_obj = Branch(
                bank_id=bank.bank_id, name=branch_name, region=region, city=target_city, 
                branch_address=branch_address, country_code=target_country, branch_type=chosen_type
            )
            
            validate_branch_integrity(branch_obj)
            branch_collection.append(branch_obj)
            
    return branch_collection

def export_branches_to_sql(branches: List[Branch]) -> None:
    for br in branches:
        name_escaped = br.name.replace("'", "''")
        region_escaped = br.region.replace("'", "''")
        city_escaped = br.city.replace("'", "''")
        addr_escaped = br.branch_address.replace("'", "''")
        
        # Clean AUTO_INCREMENT schema compatibility: branch_id column explicitly omitted
        sql_statement = (
            f"INSERT INTO Branch (bank_id, name, region, city, branch_address, country_code, branch_type) "
            f"VALUES ({br.bank_id}, '{name_escaped}', '{region_escaped}', '{city_escaped}', "
            f"'{addr_escaped}', '{br.country_code}', '{br.branch_type.value}');"
        )
        print(sql_statement)

# --- PIPELINE DEMO ---
if __name__ == "__main__":
    mock_banks = [
        Bank(bank_id=1, legal_name="Apex National Retailer", bic="APEXUS33", routing_no="122000044", country_code="US", created_at=datetime.date(2010, 3, 15), bank_status="active", license_number="OCC-11204", tier=BankTier.LARGE_NATIONAL, is_international=True, headquarters_city="New York"),
        Bank(bank_id=2, legal_name="Hanseatic Commerce Bank", bic="HANSDEBB", routing_no=None, country_code="DE", created_at=datetime.date(2002, 11, 20), bank_status="active", license_number="BAFIN-4410", tier=BankTier.REGIONAL, is_international=False, headquarters_city="Frankfurt")
    ]
    
    export_branches_to_sql(generate_branches_for_pool(mock_banks))
