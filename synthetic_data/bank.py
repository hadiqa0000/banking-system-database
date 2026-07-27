from __future__ import annotations
import random
from typing import Dict, List
from datetime import date
from dataclasses import dataclass
from typing import Set, tuple 


 
@dataclass
class Address:
    building_no: str
    street_no: str
    district: str
    city: str  
    country: str
    
    def to_string(self) -> str:
        return f"Sk. {self.street_no}, bina: {self.building_no}, {self.district}/{self.city}, {self.country}"
        
        



def generate_unique_addresses() -> Address:



@dataclass 
class Bank:
    bank_id: int
    bank_legal_name: str
    bic: str
    bank_routing_no: str
    bank_country_code: str
    bank_opened_at: date
    bank_status: str
    bank_headquarters_address: Address
    license_number: str
    @property
    def bank_headquarters_city(self) -> str:
        return self.bank_headquarters_address.city
        
        
def generate_bank_legal_name():
    generated_addresses: Set[Tuple] = set() 
    while True:
       country = random.choice(list(ALL_GEOGRAPHIES.keys()))
       city_map = ALL_GEOGRAPHIES[country]
       
       
       city = random.choice(list(city_map.keys())
       district = random.choice(city_map[city])
       
       building_no = str(random.randint(1,50))
       street_no = str(random.randint(1,40))
       
       
       
      




        
        
        

