from __future__ import annotations
from datetime import date
from dataclasses import dataclass

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
    bank_country_code: str
    bank_opened_at: date
    bank_status: str
    bank_headquarters_address: Address  # This holds the Address object
    license_number: str
    @property
    def bank_headquarters_city(self) -> str:
        return self.bank_headquarters_address.city
        
        
        

