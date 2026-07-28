from __future__ import annotations
import random
from typing import Dict, List, Optional, Union,Tuple
from datetime import date
from dataclasses import dataclass
from typing import Set, tuple 
from .config import countries
import re
import string



 
@dataclass
class Address:
    building_no: str
    street_no: str
    district: str
    city: str  
    country: str
    
    def to_string(self) -> str:
        return f"Sk. {self.street_no}, bina: {self.building_no}, {self.district}/{self.city}, {self.country}"


@dataclass 
class Bank:
    bank_id: int
    bank_legal_name: str
    bic: str
    bank_routing_no: str
    bank_sort_code : str
    bank_country_code: str
    bank_opened_at: date
    bank_status: str
    bank_headquarters_address: Address
    license_number: str
    @property
    def bank_headquarters_city(self) -> str:
        return self.bank_headquarters_address.city
        
def generate_unique_addresses() -> Address:
    generated_addresses: Set[Tuple] = set() 
    while True:
       country = random.choice(list(ALL_GEOGRAPHIES.keys()))
       city_map = ALL_GEOGRAPHIES[country]
       
       
       city = random.choice(list(city_map.keys())
       district = random.choice(city_map[city])
       
       building_no = str(random.randint(1,50))
       street_no = str(random.randint(1,40))
       
       
       addr = Address(
           building_no = building_no,
           street_no = street_no,
           district= district,
           city= city,
           country=country
           
           )
        generated_addr= (country,city,district,street_no,building_no)
        
        if generated_addr not in generated_addresses:
          generated_addresses.add(generated_addr)
          return addr
def generate_bank_legal_name(
    country: str = "US",
    geography_data: Dict = None,
    city: str = None,
    district: str = None,
    name_type: str = "random",
    include_abbreviation: bool = True,
    include_holding_company: bool = False,
    bank_type: str = "commercial",
) -> str:
    if geography_data is None:
        if country.upper() == "US":
            geography_data = UNITED_STATES_GEOGRAPHY
        elif country.upper() == "UK":
            geography_data = UNITED_KINGDOM_GEOGRAPHY
        elif country.upper() == "PAKISTAN":
            geography_data = PAKISTAN_GEOGRAPHY
        else:
            raise ValueError("Country must be 'US', 'UK', or 'Pakistan'")

    if city is None and geography_data:
        selected_city = random.choice(list(geography_data.keys()))
    elif city and city in geography_data:
        selected_city = city
    else:
        selected_city = random.choice(list(geography_data.keys()))

    if district is None and geography_data.get(selected_city):
        selected_district = random.choice(geography_data[selected_city])
    elif district and district in geography_data.get(selected_city, []):
        selected_district = district
    else:
        selected_district = random.choice(geography_data[selected_city])

    
    def _get_location_based_name():
        components = []

        if random.choice([True, False]):
            components.append(selected_district)

        if selected_city and random.choice([True, False]):
            components.append(selected_city)

        if country.upper() == "PAKISTAN":
            if bank_type == "islamic":
                islamic_name = random.choice(
                    PAKISTAN_COMPONENTS["islamic_prefixes"]
                )
                if components:
                    components.insert(0, islamic_name)
                else:
                    components.append(islamic_name)
                suffix = random.choice(["Islamic Bank", "Bank Limited"])
                components.append(suffix)
            else:
                suffix = random.choice(PAKISTAN_COMPONENTS["suffixes"])
                if len(components) < 2:
                    components.append(
                        random.choice(PAKISTAN_COMPONENTS["prefixes"])
                    )
                components.append(suffix)
        elif country.upper() == "US":
            suffix = random.choice(US_COMPONENTS["suffixes"])
            if len(components) < 2:
                components.insert(
                    0, random.choice(US_COMPONENTS["prefixes"])
                )
            components.append(suffix)
        else:  
            suffix = random.choice(UK_COMPONENTS["suffixes"])
            if len(components) < 2:
                components.insert(
                    0, random.choice(UK_COMPONENTS["prefixes"])
                )
            components.append(suffix)

        return " ".join(components)

    def _get_abbreviation_based_name():
        if country.upper() == "PAKISTAN":
            abbreviations = {
                "UBL": "United Bank Limited",
                "MCB": "Muslim Commercial Bank",
                "ABL": "Allied Bank Limited",
                "HBL": "Habib Bank Limited",
                "NBP": "National Bank of Pakistan",
                "MBL": "Meezan Bank Limited",
                "FBL": "Faysal Bank Limited",
            }
        elif country.upper() == "US":
            abbreviations = {
                "JPM": "JPMorgan Chase Bank",
                "WFC": "Wells Fargo Bank",
                "BAC": "Bank of America",
                "CITI": "Citibank",
                "USB": "US Bank",
                "PNC": "PNC Bank",
                "TFC": "Truist Financial",
            }
        else:  # UK
            abbreviations = {
                "HSBC": "Hong Kong and Shanghai Banking Corporation",
                "BARC": "Barclays Bank",
                "LLOY": "Lloyds Banking Group",
                "NWG": "NatWest Group",
                "SANT": "Santander UK",
                "STD": "Standard Chartered",
            }

        abbrev = random.choice(list(abbreviations.keys()))
        full_name = abbreviations[abbrev]

        
        if country.upper() == "PAKISTAN":
            legal = random.choice(PAKISTAN_COMPONENTS["legal_status"])
        elif country.upper() == "US":
            legal = random.choice(US_COMPONENTS["legal_status"])
        else:  
            legal = random.choice(UK_COMPONENTS["legal_status"])

        return f"{full_name} {legal} ({abbrev})"

    def _get_holding_company_name():
        if country.upper() == "PAKISTAN":
            prefix = random.choice(PAKISTAN_COMPONENTS["prefixes"])
            holding = random.choice(PAKISTAN_COMPONENTS["holding"])
            return f"{prefix} {selected_city} {holding}"
        elif country.upper() == "US":
            prefix = random.choice(US_COMPONENTS["prefixes"])
            holding = random.choice(US_COMPONENTS["holding"])
            return f"{prefix} {selected_city} {holding}"
        else:  # UK
            prefix = random.choice(UK_COMPONENTS["prefixes"])
            holding = random.choice(UK_COMPONENTS["holding"])
            return f"{prefix} {selected_city} {holding}"

    def _get_random_name():
        
        components = []

        if country.upper() == "PAKISTAN":
            
            if bank_type == "islamic" and random.choice([True, False]):
                components.append(
                    random.choice(PAKISTAN_COMPONENTS["islamic_prefixes"])
                )

            
            if random.choice([True, False]):
                components.append(
                    random.choice(PAKISTAN_COMPONENTS["prefixes"])
                )

           
            if random.choice([True, False]):
                components.append(selected_city)

            
            components.append(random.choice(PAKISTAN_COMPONENTS["suffixes"]))

            
            if random.choice([True, False]):
                components.append(
                    random.choice(PAKISTAN_COMPONENTS["legal_status"])
                )

        elif country.upper() == "US":
            
            if random.choice([True, False]):
                components.append(random.choice(US_COMPONENTS["prefixes"]))

            
            if random.choice([True, False]):
                components.append(selected_city)

            
            components.append(random.choice(US_COMPONENTS["suffixes"]))

            
            if random.choice([True, False]):
                components.append(
                    random.choice(US_COMPONENTS["legal_status"])
                )

        else: 
            
            if random.choice([True, False]):
                components.append(random.choice(UK_COMPONENTS["prefixes"]))

            if random.choice([True, False]):
                components.append(selected_city)

           
            components.append(random.choice(UK_COMPONENTS["suffixes"]))
            if random.choice([True, False]):
                components.append(
                    random.choice(UK_COMPONENTS["legal_status"])
                )

        return " ".join(components)

    
    generation_methods = {
        "random": _get_random_name,
        "location_based": _get_location_based_name,
        "abbreviation": _get_abbreviation_based_name,
        "holding_company": _get_holding_company_name,
    }

    
    method = generation_methods.get(name_type, _get_random_name)
    name = method()

   
    if include_abbreviation and name_type != "abbreviation":
        
        words = re.findall(r"\b[A-Za-z]+\b", name)
        if len(words) >= 2:
            initials = "".join(
                [
                    word[0]
                    for word in words
                    if len(word) > 1 and word[0].isalpha()
                ]
            )
            if 2 <= len(initials) <= 4 and f"({initials})" not in name:
                name = f"{name} ({initials})"

    return name
used_bic: Set[str] = set()
used_routing_numbers: Set[str] = set()
used_sort_code: Set[str] = set()

country_codes = {}


def generate_bic(bank_name: str, country: str, city: str) -> str:
    country_code = country_codes.get(country, "XX")
    bank_code = "".join([c for c in bank_name.upper() if c.isalpha()])[:4]
    while len(bank_code) < 4:
        bank_code += "X"

    if city:
        city_code = "".join([c for c in city.upper() if c.isalpha()])[:2]
        while len(city_code) < 2:
            city_code += "0"
    else:
        city_code = random.choice(["01", "02", "03", "XX"])

    bic_8 = f"{bank_code}{country_code}{city_code}"
    bic_11 = f"{bic_8}XXX"

    while True:
        bic = bic_11 if random.choice([True, False]) else bic_8
        if bic not in used_bic:
            used_bic.add(bic)
            return bic


def generate_us_routing_number(bank_country_code: str) -> Optional[str]:
    if bank_country_code.upper() != "US":
        return None

    valid_prefixes = [f"{i:02d}" for i in range(1, 13)] + [
        str(i) for i in range(21, 33)
    ]

    while True:
        prefix = random.choice(valid_prefixes)
        middle_digits = "".join(random.choices("0123456789", k=6))
        first_8_digits = prefix + middle_digits

        weights = [3, 7, 1, 3, 7, 1, 3, 7]
        digit_weight_pairs = zip(first_8_digits, weights)

        weighted_products = [
            int(digit) * weight for digit, weight in digit_weight_pairs
        ]
        weighted_sum = sum(weighted_products)
        checksum_digit = (10 - (weighted_sum % 10)) % 10

        routing_no = f"{first_8_digits}{checksum_digit}"
        if routing_no not in used_routing_numbers:
            used_routing_numbers.add(routing_no)
            return routing_no


def validate_us_routing_number(routing_number: str) -> bool:
    if (
        not routing_number
        or len(routing_number) != 9
        or not routing_number.isdigit()
    ):
        return False

    weights = [3, 7, 1, 3, 7, 1, 3, 7, 1]
    weighted_sum = sum(
        int(digit) * weight for digit, weight in zip(routing_number, weights)
    )

    return weighted_sum % 10 == 0


def generate_sort_code(bank_country_code: str) -> Optional[str]:
    if bank_country_code.upper() != "UK":
        return None

    while True:
        digits = "".join(random.choices("0123456789", k=6))
        sort_code = f"{digits[0:2]}-{digits[2:4]}-{digits[4:6]}"

        if sort_code not in used_sort_code:
            used_sort_code.add(sort_code)
            return sort_code


def validate_uk_sort_code(sort_code: str) -> bool:
    if not sort_code:
        return False

    clean_sort_code = sort_code.replace("-", "")
    if len(clean_sort_code) != 6 or not clean_sort_code.isdigit():
        return False

    if "-" in sort_code:
        parts = sort_code.split("-")
        if len(parts) != 3:
            return False
        for part in parts:
            if len(part) != 2 or not part.isdigit():
                return False

    return True
        

