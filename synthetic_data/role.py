import random
import datetime
import string
import calendar
from dataclasses import dataclass, field
from typing import List, Dict, Optional
from faker import Faker
from enum import Enum


GLOBAL_SEED = 42
random.seed(GLOBAL_SEED)






class BranchType(Enum):
    HEADQUARTERS = "headquarters"
    REGIONAL = "regional"
    LOCAL = "local"
    DIGITAL = "digital"
    


class BankTier(Enum):
    LARGE_NATIONAL = "Large National Retail"
    REGIONAL = "Regional Commercial"
    COMMUNITY = "Local Community"
    DIGITAL_NEOBANK = "Digital Neobank"
    PRIVATE_WEALTH = "Private Wealth Management"
    INVESTMENT_CORPORATE = "Investment & Corporate Banking"
    
    # Define how many specialized roles per tier (min, max)
# Format: (minimum_specialized_roles, maximum_specialized_roles)
SPECIALIZED_ROLE_COUNTS = {
    BankTier.COMMUNITY: (0, 1),              # Community banks: 0-1 specialized
    BankTier.REGIONAL: (2, 4),               # Regional banks: 2-4 specialized
    BankTier.LARGE_NATIONAL: (5, 10),        # Large banks: 5-10 specialized
    BankTier.PRIVATE_WEALTH: (3, 6),         # Wealth management: 3-6 specialized
    BankTier.INVESTMENT_CORPORATE: (4, 8),   # Investment banks: 4-8 specialized
    BankTier.DIGITAL_NEOBANK: (3, 5)         # Digital banks: 3-5 specialized
}

SERVICE_AREA_DENSITY = {
    'wealth_management': 0.30,      # 30% of specialized roles
    'investment_banking': 0.20,     # 20% of specialized roles
    'risk_compliance': 0.20,        # 20% of specialized roles
    'technology': 0.15,             # 15% of specialized roles
    'corporate_banking': 0.10,      # 10% of specialized roles
    'retail_banking': 0.05          # 5% of specialized roles
}


# Specialized roles organized by service area
SPECIALIZED_ROLE_POOLS = {
    'wealth_management': [
        'Investment Advisor',
        'Wealth Manager',
        'Portfolio Manager',
        'Trust Officer',
        'Estate Planning Specialist',
        'Tax Specialist',
        'Private Banker',
        'Asset Allocation Specialist'
    ],
    'investment_banking': [
        'Investment Banker',
        'M&A Analyst',
        'Financial Analyst',
        'Structured Finance Specialist',
        'Derivatives Specialist',
        'Private Equity Analyst',
        'Venture Capital Analyst',
        'Capital Markets Specialist'
    ],
    'risk_compliance': [
        'Risk Analyst',
        'Credit Risk Manager',
        'Internal Auditor',
        'Fraud Investigator',
        'AML Compliance Officer',
        'Regulatory Reporting Specialist',
        'Operational Risk Manager',
        'Model Risk Analyst'
    ],
    'technology': [
        'DevOps Engineer',
        'Software Engineer',
        'Data Analyst',
        'Data Scientist',
        'Cybersecurity Analyst',
        'Cloud Architect',
        'Database Administrator',
        'Machine Learning Engineer',
        'Blockchain Developer'
    ],
    'corporate_banking': [
        'Corporate Banking Officer',
        'Relationship Manager',
        'Treasury Analyst',
        'Trade Finance Specialist',
        'Cash Management Specialist',
        'Commercial Lending Officer'
    ],
    'retail_banking': [
        'Branch Manager',
        'Teller',
        'Customer Service Rep',
        'Loan Officer',
        'Mortgage Specialist',
        'Small Business Banking Officer'
    ]
}

# Define which service types each bank tier offers
TIER_SERVICES = {
    BankTier.COMMUNITY: ['retail_banking'],
    BankTier.REGIONAL: ['retail_banking', 'corporate_banking', 'risk_compliance'],
    BankTier.LARGE_NATIONAL: ['retail_banking', 'corporate_banking', 'risk_compliance', 'wealth_management', 'technology'],
    BankTier.PRIVATE_WEALTH: ['wealth_management', 'retail_banking', 'risk_compliance'],
    BankTier.INVESTMENT_CORPORATE: ['investment_banking', 'corporate_banking', 'risk_compliance', 'technology'],
    BankTier.DIGITAL_NEOBANK: ['retail_banking', 'technology', 'risk_compliance']
}
ROLE_SETS_BY_TIER = {
    BankTier.COMMUNITY: {
        'core': [
            'Branch Manager',
            'Teller', 
            'Customer Service Rep',
            'Loan Officer',
            'Accountant'
        ],
        'specialized': [], 
        'executive': [
            'Chief Executive Officer',
            'Chief Financial Officer'
        ],
        'probability_specialized': 0.1 
    },
    
    BankTier.REGIONAL: {
        'core': [
            'Branch Manager',
            'Teller',
            'Customer Service Rep',
            'Loan Officer',
            'Compliance Officer',
            'Accountant',
            'Security Officer',
            'Human Resources Officer'
        ],
        'specialized': [
            'Risk Analyst',
            'Internal Auditor',
            'IT Support Specialist',
            'Relationship Manager'
        ],
        'executive': [
            'Chief Executive Officer',
            'Chief Financial Officer',
            'Chief Operating Officer'
        ],
        'probability_specialized': 0.4 
    },
    
    BankTier.LARGE_NATIONAL: {
        'core': [
            'Branch Manager',
            'Teller',
            'Customer Service Rep',
            'Loan Officer',
            'Compliance Officer',
            'Accountant',
            'Security Officer',
            'Human Resources Officer',
            'IT Support Specialist'
        ],
        'specialized': [
            'Investment Advisor',
            'Wealth Manager',
            'Risk Analyst',
            'Treasury Analyst',
            'Internal Auditor',
            'Fraud Investigator',
            'Data Analyst',
            'Cybersecurity Analyst',
            'Credit Risk Manager',
            'Relationship Manager',
            'AML Compliance Officer'
        ],
        'executive': [
            'Chief Executive Officer',
            'Chief Financial Officer',
            'Chief Operating Officer',
            'Chief Risk Officer',
            'Chief Technology Officer'
        ],
        'probability_specialized': 0.7  
    },
    
    BankTier.PRIVATE_WEALTH: {
        'core': [
            'Branch Manager',
            'Customer Service Rep',
            'Accountant',
            'Compliance Officer'
        ],
        'specialized': [
            'Investment Advisor',
            'Wealth Manager',
            'Portfolio Manager',
            'Trust Officer',
            'Estate Planning Specialist',
            'Tax Specialist',
            'Relationship Manager'
        ],
        'executive': [
            'Chief Executive Officer',
            'Chief Financial Officer',
            'Chief Investment Officer'
        ],
        'probability_specialized': 0.8  
    },
    
    BankTier.INVESTMENT_CORPORATE: {
        'core': [
            'Compliance Officer',
            'Accountant',
            'Security Officer'
        ],
        'specialized': [
            'Investment Banker',
            'M&A Analyst',
            'Financial Analyst',
            'Risk Analyst',
            'Treasury Analyst',
            'Portfolio Manager',
            'Trader',
            'Research Analyst',
            'Corporate Banking Officer',
            'Structured Finance Specialist',
            'Derivatives Specialist',
            'Private Equity Analyst'
        ],
        'executive': [
            'Chief Executive Officer',
            'Chief Financial Officer',
            'Chief Investment Officer',
            'Chief Risk Officer',
            'Managing Director'
        ],
        'probability_specialized': 0.95 
    },
    
    BankTier.DIGITAL_NEOBANK: {
        'core': [
            'Customer Service Rep',
            'Compliance Officer',
            'Accountant'
        ],
        'specialized': [
            'DevOps Engineer',
            'Software Engineer',
            'Data Analyst',
            'Cybersecurity Analyst',
            'Product Manager',
            'UX Designer',
            'Data Scientist',
            'Cloud Architect'
        ],
        'executive': [
            'Chief Executive Officer',
            'Chief Technology Officer',
            'Chief Product Officer'
        ],
        'probability_specialized': 0.9 
    }
}


@dataclass
class Bank:
    legal_name: str
    bic: str
    routing_no: Optional[str]  
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
    role_name: str

# Set seed for reproducibility
GLOBAL_SEED = 42
random.seed(GLOBAL_SEED)

# Fixed typos and removed extra space
ROLE_NAMES = [
    'Branch Manager', 
    'Teller', 
    'Customer Service Rep',
    'Loan Officer', 
    'Compliance Officer',
    'Accountant'
]



def generate_multiple_banks_roles_with_tiers(bank_data_list):
    """
    Generate roles for multiple banks with their assigned tiers
    
    Args:
        bank_data_list: List of dicts with bank_id and bank_tier
    
    Returns:
        List of all generated roles
    """
    all_roles = []
    for bank_data in bank_data_list:
        bank_id = bank_data['bank_id']
        bank_tier = bank_data['bank_tier']
        
        bank_roles = generate_roles_for_bank(bank_id, bank_tier)
        all_roles.extend(bank_roles)
    
    return all_roles
    
    
    
def select_specialized_roles(bank_tier, bank_size_factor=1.0):
    """
    Select specialized roles for a bank based on its tier and size
    
    Args:
        bank_tier: BankTier enum
        bank_size_factor: Multiplier for number of roles (1.0 = normal)
    
    Returns:
        List of selected specialized role names
    """
    # Get available services for this tier
    available_services = TIER_SERVICES.get(bank_tier, [])
    if not available_services:
        return []
    
    # Determine how many specialized roles to add
    min_roles, max_roles = SPECIALIZED_ROLE_COUNTS.get(bank_tier, (0, 0))
    
    # Adjust for bank size factor (larger banks get more roles)
    adjusted_max = int(max_roles * bank_size_factor)
    adjusted_min = int(min_roles * bank_size_factor)
    
    # Ensure we don't exceed available roles
    total_available = 0
    for service in available_services:
        total_available += len(SPECIALIZED_ROLE_POOLS.get(service, []))
    
    num_roles = random.randint(
        max(0, min(adjusted_min, total_available)),
        min(max(adjusted_max, adjusted_min), total_available)
    )
    
    if num_roles == 0:
        return []
    
    # Build pool of available roles from services
    role_pool = []
    for service in available_services:
        roles = SPECIALIZED_ROLE_POOLS.get(service, [])
        # Add roles with slight weighting based on service density
        density = SERVICE_AREA_DENSITY.get(service, 0.1)
        count_to_add = max(1, int(len(roles) * density * 2))
        role_pool.extend(random.sample(roles, min(count_to_add, len(roles))))
    
    # Ensure we have enough unique roles
    role_pool = list(set(role_pool))  # Remove duplicates
    
    # If we need more roles than available, use all
    if num_roles > len(role_pool):
        return role_pool
    
    # Select random roles from the pool
    return random.sample(role_pool, num_roles)

def generate_roles_for_bank(bank_id, bank_tier, bank_size_factor=1.0, bank_name=""):
    """
    Generate roles for a bank with specialized roles
    
    Args:
        bank_id: The bank's ID
        bank_tier: BankTier enum value
        bank_size_factor: Multiplier for role count (1.0 = normal)
        bank_name: Bank name for context
    
    Returns:
        List of role dictionaries
    """
    tier_config = ROLE_SETS_BY_TIER.get(bank_tier)
    if not tier_config:
        raise ValueError(f"Unknown bank tier: {bank_tier}")
    
    roles = []
    role_counter = 1
    
    # 1. Add all core roles (mandatory)
    for role_name in tier_config['core']:
        roles.append({
            'bank_id': bank_id,
            'role_id': role_counter,
            'role_name': role_name,
            'role_category': 'core',
            'bank_tier': bank_tier.value,
            'bank_name': bank_name,
            'specialization_area': 'core_operations'
        })
        role_counter += 1
    
    # 2. Add executive roles (mandatory)
    for role_name in tier_config['executive']:
        roles.append({
            'bank_id': bank_id,
            'role_id': role_counter,
            'role_name': role_name,
            'role_category': 'executive',
            'bank_tier': bank_tier.value,
            'bank_name': bank_name,
            'specialization_area': 'leadership'
        })
        role_counter += 1
    
    # 3. Add specialized roles
    specialized_roles = select_specialized_roles(bank_tier, bank_size_factor)
    
    for role_name in specialized_roles:
        # Determine which service area this role belongs to
        service_area = 'general'
        for area, roles_list in SPECIALIZED_ROLE_POOLS.items():
            if role_name in roles_list:
                service_area = area
                break
        
        roles.append({
            'bank_id': bank_id,
            'role_id': role_counter,
            'role_name': role_name,
            'role_category': 'specialized',
            'bank_tier': bank_tier.value,
            'bank_name': bank_name,
            'specialization_area': service_area
        })
        role_counter += 1
    
    return roles


def create_bank_data_with_tiers(num_banks):
    """Create sample bank data with assigned tiers"""
    bank_data = []
    tiers = list(BankTier)
    
   
    tier_weights = {
        BankTier.LARGE_NATIONAL: 15,
        BankTier.REGIONAL: 25,
        BankTier.COMMUNITY: 30,
        BankTier.DIGITAL_NEOBANK: 15,
        BankTier.PRIVATE_WEALTH: 10,
        BankTier.INVESTMENT_CORPORATE: 5
    }
    
   
    weighted_tiers = []
    for tier, weight in tier_weights.items():
        weighted_tiers.extend([tier] * weight)
    
    for i in range(num_banks):
        bank_data.append({
            'bank_id': i + 1,
            'bank_tier': random.choice(weighted_tiers)
        })
    
    return bank_data
    
def create_bank_data_with_size_and_tier(num_banks):
    """
    Create bank data with assigned tiers and size factors
    
    Args:
        num_banks: Number of banks to create
    
    Returns:
        List of dictionaries with bank_id, bank_tier, size_factor, and bank_name
    """
    # Define tier distribution with their size ranges
    # Format: (tier, probability, (min_size_factor, max_size_factor))
    tier_configs = [
        (BankTier.COMMUNITY, 0.30, (0.5, 1.2)),          # 30% community banks
        (BankTier.REGIONAL, 0.25, (0.8, 1.5)),           # 25% regional banks
        (BankTier.LARGE_NATIONAL, 0.15, (1.0, 2.0)),     # 15% large banks
        (BankTier.DIGITAL_NEOBANK, 0.12, (0.7, 1.3)),    # 12% digital banks
        (BankTier.PRIVATE_WEALTH, 0.10, (0.6, 1.4)),     # 10% private wealth
        (BankTier.INVESTMENT_CORPORATE, 0.08, (0.8, 1.8)) # 8% investment banks
    ]
    
    # Create weighted list for random selection
    weighted_tiers = []
    for tier, prob, size_range in tier_configs:
        # Convert probability to count
        count = int(prob * num_banks)
        for _ in range(count):
            weighted_tiers.append((tier, size_range))
    
    # Add remaining banks if needed (fill with random tiers)
    while len(weighted_tiers) < num_banks:
        # Pick a random tier based on probabilities
        rand = random.random()
        cumulative = 0
        for tier, prob, size_range in tier_configs:
            cumulative += prob
            if rand <= cumulative:
                weighted_tiers.append((tier, size_range))
                break
    
    # Shuffle to randomize order
    random.shuffle(weighted_tiers)
    
    # Create bank names pool
    bank_name_prefixes = [
        "First", "United", "National", "Community", "Global",
        "Pacific", "Atlantic", "Mountain", "Coastal", "Central",
        "American", "International", "Metropolitan", "Regional", "Premier",
        "Liberty", "Republic", "Heritage", "Summit", "Gateway"
    ]
    
    bank_name_suffixes = [
        "Bank", "Trust", "Savings", "Financial", "National Bank",
        "Capital", "Investment", "Wealth", "Commerce", "Community Bank"
    ]
    
    bank_data = []
    for i, (tier, size_range) in enumerate(weighted_tiers[:num_banks]):
        # Generate a size factor within the range
        size_factor = round(random.uniform(size_range[0], size_range[1]), 2)
        
        # Generate a bank name
        prefix = random.choice(bank_name_prefixes)
        suffix = random.choice(bank_name_suffixes)
        bank_name = f"{prefix} {suffix}"
        
        # Add variation based on tier
        if tier == BankTier.LARGE_NATIONAL:
            bank_name = f"{prefix} National Bank"
        elif tier == BankTier.INVESTMENT_CORPORATE:
            bank_name = f"{prefix} Investment Partners"
        elif tier == BankTier.PRIVATE_WEALTH:
            bank_name = f"{prefix} Wealth Management"
        elif tier == BankTier.DIGITAL_NEOBANK:
            bank_name = f"{prefix} Digital Bank"
        
        bank_data.append({
            'bank_id': i + 1,
            'bank_tier': tier,
            'size_factor': size_factor,
            'bank_name': f"{bank_name} {i + 1}"  # Add ID to make unique
        })
    
    return bank_data    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

if __name__ == "__main__":
    # Set seed for reproducibility
    random.seed(42)
    
    print("=" * 70)
    print("SPECIALIZED ROLE GENERATION BY BANK TIER")
    print("=" * 70)
    
    # Create bank data with tiers and size factors
    num_banks = 10
    bank_data = create_bank_data_with_size_and_tier(num_banks)
    
    print(f"\nGenerating roles for {num_banks} banks...")
    print("\nBank Details:")
    print("-" * 70)
    for bank in bank_data:
        print(f"Bank {bank['bank_id']}: {bank['bank_name']}")
        print(f"  Tier: {bank['bank_tier'].value}")
        print(f"  Size Factor: {bank['size_factor']:.2f}")
        print("-" * 70)
    
    # Generate all roles
    all_roles = []
    for bank in bank_data:
        roles = generate_roles_for_bank(
            bank['bank_id'],
            bank['bank_tier'],
            bank['size_factor'],
            bank['bank_name']
        )
        all_roles.extend(roles)
    
    print(f"\nTotal roles generated: {len(all_roles)}")
    
    # Analyze specialization
    roles_by_bank = defaultdict(list)
    roles_by_tier = defaultdict(list)
    specialization_by_tier = defaultdict(lambda: defaultdict(int))
    specialization_by_area = Counter()
    
    for role in all_roles:
        roles_by_bank[role['bank_id']].append(role)
        roles_by_tier[role['bank_tier']].append(role)
        specialization_by_tier[role['bank_tier']][role['role_category']] += 1
        specialization_by_area[role['specialization_area']] += 1
    
    # Display detailed results
    print("\n" + "=" * 70)
    print("DETAILED ROLE BREAKDOWN BY BANK")
    print("=" * 70)
    
    for bank_id, roles in sorted(roles_by_bank.items()):
        core_roles = [r for r in roles if r['role_category'] == 'core']
        exec_roles = [r for r in roles if r['role_category'] == 'executive']
        spec_roles = [r for r in roles if r['role_category'] == 'specialized']
        
        print(f"\nBank {bank_id}: {roles[0]['bank_name']} ({roles[0]['bank_tier']})")
        print(f"  Total Roles: {len(roles)}")
        print(f"  Core: {len(core_roles)} | Executive: {len(exec_roles)} | Specialized: {len(spec_roles)}")
        
        if spec_roles:
            print(f"  Specialized Roles: {', '.join(r['role_name'] for r in spec_roles[:5])}")
            if len(spec_roles) > 5:
                print(f"    ... and {len(spec_roles) - 5} more")
        else:
            print("  No specialized roles")
        
        areas = Counter(r['specialization_area'] for r in spec_roles)
        if areas:
            print(f"  Specialization Areas: {', '.join(f'{area}({count})' for area, count in areas.items())}")
    
    # Summary by tier
    print("\n" + "=" * 70)
    print("SUMMARY BY BANK TIER")
    print("=" * 70)
    
    for tier, roles in sorted(roles_by_tier.items()):
        core_count = sum(1 for r in roles if r['role_category'] == 'core')
        exec_count = sum(1 for r in roles if r['role_category'] == 'executive')
        spec_count = sum(1 for r in roles if r['role_category'] == 'specialized')
        
        print(f"\n{tier.value}:")
        print(f"  Banks: {len(set(r['bank_id'] for r in roles))}")
        print(f"  Roles per bank: {len(roles) / len(set(r['bank_id'] for r in roles)):.1f}")
        print(f"  Core: {core_count} | Executive: {exec_count} | Specialized: {spec_count}")
        print(f"  Specialization Density: {spec_count / len(roles) * 100:.1f}%")
        
        spec_roles = [r['role_name'] for r in roles if r['role_category'] == 'specialized']
        if spec_roles:
            most_common = Counter(spec_roles).most_common(3)
            print(f"  Top Specialized Roles: {', '.join(f'{name}({count})' for name, count in most_common)}")
    
    # Overall specialization areas
    print("\n" + "=" * 70)
    print("OVERALL SPECIALIZATION AREAS")
    print("=" * 70)
    for area, count in specialization_by_area.most_common():
        print(f"  {area}: {count} roles")
    for tier, roles in sorted(roles_by_tier.items()):
        core_count = sum(1 for r in roles if r['role_category'] == 'core')
        exec_count = sum(1 for r in roles if r['role_category'] == 'executive')
        spec_count = sum(1 for r in roles if r['role_category'] == 'specialized')
        
        print(f"\n{tier.value}:")
        print(f"  Banks: {len(set(r['bank_id'] for r in roles))}")
        print(f"  Roles per bank: {len(roles) // len(set(r['bank_id'] for r in roles)):.1f}")
        print(f"  Core: {core_count} | Executive: {exec_count} | Specialized: {spec_count}")
        print(f"  Specialization Density: {spec_count / len(roles) * 100:.1f}%")
        
        # Most common specialized roles
        spec_roles = [r['role_name'] for r in roles if r['role_category'] == 'specialized']
        if spec_roles:
            most_common = Counter(spec_roles).most_common(3)
            print(f"  Top Specialized Roles: {', '.join(f'{name}({count})' for name, count in most_common)}")
    
    # Overall specialization areas
    print("\n" + "=" * 70)
    print("OVERALL SPECIALIZATION AREAS")
    print("=" * 70)
    for area, count in specialization_by_area.most_common():
        print(f"  {area}: {count} roles")
