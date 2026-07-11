import random
import datetime
import string
import calendar
from dataclasses import dataclass, field
from typing import List, Dict, Optional
from faker import Faker


GLOBAL_SEED = 42
random.seed(GLOBAL_SEED)

CURRENT_YEAR = datetime.date.today().year #built in function used to initialize current year 

STATUS_MAP = {
    'Active': 'active',
    'Suspended': 'suspended',
    'Closed': 'closed'
}


COUNTRY_MARKET_WEIGHTS = {
    'US': 0.22, 'CN': 0.15, 'JP': 0.10, 'GB': 0.08, 'DE': 0.07, 
    'FR': 0.06, 'CA': 0.05, 'AU': 0.04, 'IN': 0.06, 'BR': 0.05, 
    'CH': 0.04, 'IT': 0.04, 'NL': 0.02, 'TR': 0.02, 'ZA': 0.02
}

COUNTRIES = list(COUNTRY_MARKET_WEIGHTS.keys())

assert abs(sum(COUNTRY_PROBS) - 1.0) < 1e-10, "Probabilities don't sum to 1"

PROB_SUM = sum(COUNTRY_PROBS)
COUNTRY_PROBS = [p / PROB_SUM for p in COUNTRY_PROBS]


FAKERS: Dict[str, Faker] = {
    'US': Faker('en_US'), 'GB': Faker('en_GB'), 'DE': Faker('de_DE'),
    'JP': Faker('ja_JP'), 'TR': Faker('tr_TR'), 'FR': Faker('fr_FR'),
    'CA': Faker('en_CA'), 'AU': Faker('en_AU'), 'IN': Faker('en_IN'),
    'CN': Faker('zh_CN'), 'BR': Faker('pt_BR'), 'CH': Faker('de_CH'),
    'IT': Faker('it_IT'), 'NL': Faker('nl_NL'), 'ZA': Faker('en_ZA')
}
for fake_instance in FAKERS.values():
    fake_instance.seed_instance(GLOBAL_SEED)

COUNTRY_NAMES_MATRIX = {
    'US': {
        'geo': ['Pacific', 'Atlantic', 'Midwest', 'Metropolitan', 'Summit', 'Horizon', 'Valley', 'Coastal'],
        'brand': ['First', 'National', 'Premier', 'United', 'Federal', 'Central', 'Citizens', 'Liberty', 'Alliance'],
        'type': ['Trust', 'Commerce', 'Capital', 'Savings', 'Commercial', 'Merchants'],
        'templates': ["{brand} {type} Bank", "{brand} National Bank", "{geo} {type} Bank", "{brand} Bank & Trust Company"]
    },
    'GB': {
        'geo': ['Thames', 'Caledonian', 'Meridian', 'London', 'Cotswold', 'Severn'],
        'brand': ['Royal', 'British', 'Imperial', 'Anglo', 'Scotia', 'Commonwealth', 'Sterling'],
        'type': ['Commercial', 'Mutual', 'Merchant', 'Alliance', 'Clearing'],
        'templates': ["{brand} {type} Bank", "{geo} Merchant Bank", "{brand} Bank PLC", "{geo} Banking Group PLC"]
    },
    'DE': {
        'geo': ['Rheinische', 'Bayerische', 'Berliner', 'Frankfurter', 'Norddeutsche', 'Alpen'],
        'brand': ['Deutsche', 'Euro', 'Commerz', 'Hansa', 'Volks'],
        'type': ['Handels', 'Kredit', 'Gewerbe', 'Investitions', 'Spar'],
        'templates': ["{brand}bank AG", "{geo} {type}bank GmbH", "{brand} Finanzgruppe", "Deutsche {type}bank AG"]
    },
    'JP': {
        'geo': ['Kanto', 'Kansai', 'Fuji', 'Tokyo', 'Kyoto', 'Hokkaido'],
        'brand': ['Sakura', 'Nippon', 'Sumitomo', 'Mitsubishi', 'Sanwa', 'Dai-Ichi'],
        'type': ['Commercial', 'Trust', 'Industrial', 'Agricultural'],
        'templates': ["{brand} Bank", "{geo} {type} Bank", "{brand} Financial Group", "{brand} {type} Holdings"]
    },
    'TR': {
        'geo': ['Anadolu', 'Avrasya', 'Boğaziçi', 'Ege', 'Akdeniz', 'Marmara'],
        'brand': ['Türkiye', 'Halk', 'Ziraat', 'Kalkınma', 'Vakıf', 'Garanti'],
        'type': ['Finans', 'Ticaret', 'Kredi', 'Katılım', 'Yatırım'],
        'templates': ["{brand} {type} Bankası A.Ş.", "{geo} Katılım Bankası", "{brand} Bankası", "{geo} Ticaret Grubu"]
    },
    'FR': {
        'geo': ['Parisienne', 'de France', 'du Nord', 'Rhône-Alpes'],
        'brand': ['Nationale', 'Mutuel', 'Centrale', 'Agricole', 'Populaire', 'Générale'],
        'type': ['Banque', 'Crédit', 'Société', 'Caisse', 'Union'],
        'templates': ["{type} {brand} SA", "{type} {brand} {geo}", "Crédit {brand}", "Banque {brand}"]
    },
    'CA': {
        'geo': ['Laurentian', 'Maritime', 'Pacific', 'Ontario', 'Toronto'],
        'brand': ['Royal', 'Dominion', 'Imperial', 'National', 'Crown'],
        'type': ['Commerce', 'Trust', 'Savings', 'Financial'],
        'templates': ["{brand} Bank of Canada", "{geo} {type} Bank", "{brand} Financial Corporation", "Bank of {geo}"]
    },
    'AU': {
        'geo': ['Tasman', 'Southern', 'Sydney', 'Melbourne', 'Queensland'],
        'brand': ['Commonwealth', 'National', 'Colonial'],
        'type': ['Commercial', 'Investment', 'Mutual', 'Alliance'],
        'templates': ["{brand} Bank of Australia", "{geo} {type} Bank Limited", "{brand} Banking Group", "National {geo} Bank"]
    },
    'IN': {
        'geo': ['Punjab', 'Bengal', 'Deccan', 'Canara', 'Baroda'],
        'brand': ['State', 'Federal', 'National', 'Central', 'Union', 'Imperial'],
        'type': ['Commercial', 'Development', 'Agricultural', 'Industrial'],
        'templates': ["{brand} Bank of India", "{geo} {type} Bank", "{brand} Central Bank Ltd.", "{geo} National Bank"]
    },
    'CN': {
        'geo': ['China', 'Guangdong', 'Shanghai', 'Bohai'],
        'brand': ['Industrial', 'Agricultural', 'Construction', 'Communications', 'Merchants'],
        'type': ['Commercial', 'Development', 'Savings'],
        'templates': ["{brand} Bank of {geo}", "{geo} {brand} Bank Co., Ltd.", "People's Bank of {geo}", "{brand} Development Bank"]
    },
    'BR': {
        'geo': ['do Brasil', 'Paulista', 'Carioca', 'da Amazônia'],
        'brand': ['Central', 'Mercantil', 'Sudameris'],
        'type': ['Banco', 'Crédito', 'União', 'Progresso', 'Aliança'],
        'templates': ["{type} {geo} S.A.", "{type} {brand}", "{type} Mercantil {geo}", "União de Bancos Brasileiros S.A."]
    },
    'CH': {
        'geo': ['Zürcher', 'Helvetic', 'Alpine', 'Genève', 'Basel'],
        'brand': ['Swiss', 'Credit', 'Union', 'Lombard'],
        'type': ['Cantonal', 'Investment', 'Private', 'Commercial'],
        'templates': ["{brand} Bank Corp", "{geo} Kantonalbank AG", "Swiss {type} Bank", "Crédit {geo} SA"]
    },
    'IT': {
        'geo': ['di Roma', 'Milano', 'Toscana', 'Padana'],
        'brand': ['Nazionale', 'Popolare', 'Italiano', 'Cooperativo'],
        'type': ['Banca', 'Credito', 'Banco', 'Istituto'],
        'templates': ["{type} {brand} SpA", "{type} {geo}", "Banco {brand} S.p.A.", "Istituto Centrale di Credito"]
    },
    'NL': {
        'geo': ['Amsterdamsche', 'Rotterdamsche', 'Nederlandse'],
        'brand': ['Algemene', 'Nationale', 'Delta'],
        'type': ['Handels', 'Investerings', 'Krediet', 'Spaar'],
        'templates': ["{geo} {brand}bank NV", "Nationale {type}bank N.V.", "{brand} Groep NV", "Nederlandse {type} Bank"]
    },
    'ZA': {
        'geo': ['Rand', 'African', 'Cape', 'Gauteng'],
        'brand': ['Standard', 'National', 'Sasfin'],
        'type': ['Mutual', 'Commercial', 'Development', 'Investment'],
        'templates': ["{brand} Bank Ltd", "{geo} {type} Bank", "Standard Bank of South Africa", "{brand} Financial Services"]
    }
}

COUNTRY_DATA = {
    'US': {
        'regulator': 'OCC', 'cities': ['New York', 'Chicago', 'Charlotte', 'San Francisco', 'Dallas'], 'city_probs': [0.45, 0.20, 0.15, 0.12, 0.08],
        'city_streets': {
            'New York': ['Wall St', 'Broadway', 'Park Ave', 'Fifth Ave', 'Madison Ave'],
            'Chicago': ['Michigan Ave', 'Clark St', 'State St', 'Wacker Dr'],
            'Charlotte': ['Tryon St', 'College St', 'Trade St'],
            'San Francisco': ['Market St', 'Montgomery St', 'California St'],
            'Dallas': ['Main St', 'Commerce St', 'Elm St']
        },
        'city_swift_locations': {'New York': 'NY', 'Chicago': 'CH', 'Charlotte': 'NC', 'San Francisco': 'SF', 'Dallas': 'DF'}
    },
    'GB': {
        'regulator': 'FCA', 'cities': ['London', 'Edinburgh', 'Manchester', 'Birmingham'], 'city_probs': [0.65, 0.15, 0.12, 0.08],
        'city_streets': {
            'London': ['Threadneedle St', 'Canary Wharf', 'Lombard St', 'Fleet St'],
            'Edinburgh': ['George St', 'Princes St', 'Royal Mile'],
            'Manchester': ['Deansgate', 'King St', 'Mosley St'],
            'Birmingham': ['Colmore Row', 'Broad St', 'New St']
        },
        'city_swift_locations': {'London': 'LN', 'Edinburgh': 'ED', 'Manchester': 'MC', 'Birmingham': 'BM'}
    },
    'DE': {
        'regulator': 'BAFIN', 'cities': ['Frankfurt', 'Munich', 'Berlin', 'Hamburg'], 'city_probs': [0.55, 0.20, 0.15, 0.10],
        'city_streets': {
            'Frankfurt': ['Kaiserstraße', 'Mainzer Landstraße', 'Neue Mainzer Str.', 'Bockenheimer Landstraße'],
            'Munich': ['Maximilianstraße', 'Ludwigstraße', 'Prinzregentenstraße'],
            'Berlin': ['Friedrichstraße', 'Potsdamer Platz', 'Unter den Linden'],
            'Hamburg': ['Mönckebergstraße', 'Jungfernstieg', 'Neuer Wall']
        },
        'city_swift_locations': {'Frankfurt': 'FF', 'Munich': 'MU', 'Berlin': 'BE', 'Hamburg': 'HH'}
    },
    'JP': {
        'regulator': 'FSA', 'cities': ['Tokyo', 'Osaka', 'Nagoya', 'Yokohama'], 'city_probs': [0.60, 0.20, 0.12, 0.08],
        'city_streets': {
            'Tokyo': ['Marunouchi', 'Otemachi', 'Ginza', 'Chuo-dori'],
            'Osaka': ['Midosuji Ave', 'Nakanoshima', 'Umeda St'],
            'Nagoya': ['Sakae St', 'Meieki', 'Hirokoji-dori'],
            'Yokohama': ['Minato Mirai', 'Bashamichi', 'Motomachi St']
        },
        'city_swift_locations': {'Tokyo': 'TY', 'Osaka': 'OS', 'Nagoya': 'NG', 'Yokohama': 'YK'}
    },
    'TR': {
        'regulator': 'BDDK', 'cities': ['Istanbul', 'Ankara', 'İzmir', 'Bursa'], 'city_probs': [0.45, 0.20, 0.15, 0.20],
        'city_streets': {
            'Istanbul': ['Büyükdere Caddesi', 'Bankalar Caddesi', 'İstiklal Caddesi', 'Bağdat Caddesi'],
            'Ankara': ['Atatürk Bulvarı', 'Cinnah Caddesi', 'Tunalı Hilmi Caddesi'],
            'İzmir': ['Kordon Boyu', 'Atatürk Caddesi', 'Mithatpaşa Caddesi'],
            'Bursa': ['Atatürk Caddesi', 'Fatih Sultan Mehmet Bulvarı', 'Çekirge Caddesi']
        },
        'city_swift_locations': {'Istanbul': 'IS', 'Ankara': 'AK', 'İzmir': 'IZ', 'Bursa': 'BR'}
    },
    'FR': {
        'regulator': 'ACPR', 'cities': ['Paris', 'Lyon', 'Marseille'], 'city_probs': [0.70, 0.18, 0.12],
        'city_streets': {
            'Paris': ['Rue de la Paix', 'Boulevard Haussmann', 'Rue de Rivoli', 'Avenue des Champs-Élysées'],
            'Lyon': ['Rue de la République', 'Rue Garibaldi', 'Avenue Jean Jaurès'],
            'Marseille': ['Rue de la République', 'La Canebière', 'Boulevard Prado']
        },
        'city_swift_locations': {'Paris': 'PP', 'Lyon': 'LY', 'Marseille': 'MR'}
    },
    'CA': {
        'regulator': 'OSFI', 'cities': ['Toronto', 'Montreal', 'Vancouver', 'Calgary'], 'city_probs': [0.50, 0.25, 0.15, 0.10],
        'city_streets': {
            'Toronto': ['Bay St', 'King St W', 'Front St', 'Yonge St'],
            'Montreal': ['Rue Saint-Jacques', 'René-Lévesque Blvd', 'Rue Notre-Dame'],
            'Vancouver': ['Burrard St', 'Georgia St', 'Granville St'],
            'Calgary': ['2 St SW', 'Centre St S', 'Macleod Trail']
        },
        'city_swift_locations': {'Toronto': 'TO', 'Montreal': 'MO', 'Vancouver': 'VA', 'Calgary': 'CA'}
    },
    'AU': {
        'regulator': 'APRA', 'cities': ['Sydney', 'Melbourne', 'Brisbane'], 'city_probs': [0.50, 0.35, 0.15],
        'city_streets': {
            'Sydney': ['George St', 'Martin Pl', 'Pitt St', 'Macquarie St'],
            'Melbourne': ['Collins St', 'Bourke St', 'Flinders St'],
            'Brisbane': ['Queen St', 'Eagle St', 'Charlotte St']
        },
        'city_swift_locations': {'Sydney': 'SY', 'Melbourne': 'ME', 'Brisbane': 'BR'}
    },
    'IN': {
        'regulator': 'RBI', 'cities': ['Mumbai', 'Delhi', 'Bangalore', 'Kolkata'], 'city_probs': [0.45, 0.25, 0.18, 0.12],
        'city_streets': {
            'Mumbai': ['Nariman Point', 'Dalal St', 'Bandra Kurla Complex', 'Mahatma Gandhi Road'],
            'Delhi': ['Connaught Place', 'Barakhamba Rd', 'Janpath Rd'],
            'Bangalore': ['MG Road', 'Residency Rd', 'Brigade Rd'],
            'Kolkata': ['Strand Rd', 'Netaji Subhas Rd', 'Park St']
        },
        'city_swift_locations': {'Mumbai': 'BB', 'Delhi': 'DE', 'Bangalore': 'BL', 'Kolkata': 'CA'}
    },
    'CN': {
        'regulator': 'NFRA', 'cities': ['Beijing', 'Shanghai', 'Shenzhen', 'Guangzhou'], 'city_probs': [0.40, 0.35, 0.15, 0.10],
        'city_streets': {
            'Beijing': ['Financial Street', 'Jianguomenwai St', 'Fuxingmennei St'],
            'Shanghai': ['Lujiazui Ring Rd', 'The Bund', 'Nanjing Road'],
            'Shenzhen': ['Shennan Ave', 'Futian District', 'Huafu Rd'],
            'Guangzhou': ['Zhujiang East Rd', 'Tianhe Rd', 'Zhongshan Rd']
        },
        'city_swift_locations': {'Beijing': 'BJ', 'Shanghai': 'SH', 'Shenzhen': 'SZ', 'Guangzhou': 'GZ'}
    },
    'BR': {
        'regulator': 'BCB', 'cities': ['São Paulo', 'Rio de Janeiro', 'Brasília'], 'city_probs': [0.55, 0.25, 0.20],
        'city_streets': {
            'São Paulo': ['Avenida Paulista', 'Faria Lima', 'Av. São João', 'Av. Brigadeiro Luís Antônio'],
            'Rio de Janeiro': ['Avenida Rio Branco', 'Voluntários da Pátria', 'Av. Presidente Vargas'],
            'Brasília': ['SBS Quadra', 'Eixo Monumental', 'SBN Quadra']
        },
        'city_swift_locations': {'São Paulo': 'SP', 'Rio de Janeiro': 'RJ', 'Brasília': 'BR'}
    },
    'CH': {
        'regulator': 'FINMA', 'cities': ['Zurich', 'Geneva', 'Basel', 'Lugano'], 'city_probs': [0.50, 0.30, 0.12, 0.08],
        'city_streets': {
            'Zurich': ['Bahnhofstrasse', 'Paradeplatz', 'Bleicherweg', 'Talstrasse'],
            'Geneva': ['Rue du Rhône', 'Rue de la Corraterie', 'Rue du Mont-Blanc'],
            'Basel': ['Aeschenvorstadt', 'St. Jakob-Strasse', 'Freie Strasse'],
            'Lugano': ['Via Nassa', 'Piazza Riforma', 'Via Canova']
        },
        'city_swift_locations': {'Zurich': 'ZH', 'Geneva': 'GE', 'Basel': 'BS', 'Lugano': 'LU'}
    },
    'IT': {
        'regulator': 'BI', 'cities': ['Milan', 'Rome', 'Turin'], 'city_probs': [0.55, 0.30, 0.15],
        'city_streets': {
            'Milan': ['Piazza Affari', 'Via Monte Napoleone', 'Via Broletto', 'Corso Matteotti'],
            'Rome': ['Via del Corso', 'Via Veneto', 'Via Nazionale'],
            'Turin': ['Via Roma', 'Corso Vittorio Emanuele II', 'Via Garibaldi']
        },
        'city_swift_locations': {'Milan': 'MM', 'Rome': 'RM', 'Turin': 'TR'}
    },
    'NL': {
        'regulator': 'DNB', 'cities': ['Amsterdam', 'Rotterdam', 'The Hague', 'Utrecht'], 'city_probs': [0.55, 0.20, 0.15, 0.10],
        'city_streets': {
            'Amsterdam': ['Keizersgracht', 'Damrak', 'Zuidas', 'Herengracht'],
            'Rotterdam': ['Coolsingel', 'Weena', 'Schiedamsedijk'],
            'The Hague': ['Spui', 'Kneuterdijk'],
            'Utrecht': ['Jaarbeursplein', 'Oudegracht', 'Vredenburg']
        },
        'city_swift_locations': {'Amsterdam': 'AD', 'Rotterdam': 'RO', 'The Hague': 'GA', 'Utrecht': 'UT'}
    },
    'ZA': {
        'regulator': 'SARB', 'cities': ['Johannesburg', 'Cape Town', 'Pretoria'], 'city_probs': [0.55, 0.30, 0.15],
        'city_streets': {
            'Johannesburg': ['Fox St', 'Rivonia Rd', 'Alice Lane', 'Main St'],
            'Cape Town': ['Adderley St', 'Long St', 'St Georges Mall'],
            'Pretoria': ['Paul Kruger St', 'Stanza Bopape St', 'Francis Baard St']
        },
        'city_swift_locations': {'Johannesburg': 'JJ', 'Cape Town': 'CT', 'Pretoria': 'PR'}
    }
}

#generating empty sets in python to only generate unique names,bics, routings and licenses, as per rwequirement of business rules
used_names = set()
used_bics = set()
used_routings = set()
used_licenses = set()



#very basic, we create a class of the table
@dataclass
class Bank:
    legal_name: str
    bic: str
    routing_no: Optional[str]  # Only assigned for 'US'
    country_code: str
    created_at: datetime.date
    bank_status: str
    headquarters_city: str
    headquarters_address: str
    license_number: str


#for our first requirememnt we generate a unique name


def generate_unique_name(country: str) -> str: #the arrow suggests this likely will return a string
    matrix = COUNTRY_NAMES_MATRIX[country] #look through the dictionary COUNTRY_NAMES_MATRIX for a country and store it as matrix(which is a dictionary)
    #the dictionary has sections geo, brand, type, template
    for _ in range(200):
        template = random.choice(matrix['templates'])
        geo = random.choice(matrix['geo'])
        brand = random.choice(matrix['brand'])
        b_type = random.choice(matrix['type'])
        
        name = template.format(geo=geo, brand=brand, type=b_type)
        if name not in used_names:
            used_names.add(name)
            return name
        
    while True:
        fallback_name = f"{random.choice(matrix['brand'])} Global {random.choice(matrix['type'])} Bank #{random.randint(100, 9999)}"
        if fallback_name not in used_names:
            used_names.add(fallback_name)
            return fallback_name

def derive_bank_code(name: str) -> str:
    cleaned = (name.replace('&', '').replace('.', '').replace('AG', '')
               .replace('GmbH', '').replace('A.Ş.', '').replace('S.A.', '')
               .replace('SpA', '').replace('PLC', '').replace('Co, Ltd', ''))
    words = cleaned.split()
    initials = "".join([word[0].upper() for word in words if word])
    initials = initials.translate(str.maketrans("ÇĞİÖŞÜÂÊÎÛ", "CGIOSUAEIU"))
    
    if len(initials) >= 4:
        return initials[:4]
    return (initials + ''.join(random.choices(string.ascii_uppercase, k=4 - len(initials))))[:4]

def generate_unique_bic(name: str, country: str, city: str) -> str:
    bank_code = derive_bank_code(name)
    loc_code = COUNTRY_DATA[country]['city_swift_locations'][city]
    
    attempts = 0
    while True:
        if random.random() < 0.25:
            branch = ''.join(random.choices(string.ascii_uppercase + string.digits, k=3))
            bic = f"{bank_code}{country}{loc_code}{branch}"
        else:
            bic = f"{bank_code}{country}{loc_code}"
            
        if bic not in used_bics:
            used_bics.add(bic)
            return bic
            
        attempts += 1
        if attempts > 50:
            bank_code = bank_code[:3] + random.choice(string.ascii_uppercase)

def generate_unique_routing(country: str) -> Optional[str]:
    if country != 'US':
        return None
    frb_prefixes = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31", "32"]
    while True:
        prefix = random.choice(frb_prefixes)
        body = "".join(random.choices(string.digits, k=6))
        d = [int(char) for char in (prefix + body)]
        checksum = (3 * (d[0] + d[3] + d[6])) + (7 * (d[1] + d[4] + d[7])) + (1 * (d[2] + d[5]))
        mod = checksum % 10
        check_digit = 0 if mod == 0 else (10 - mod)
        routing = f"{prefix}{body}{check_digit}"
        
        if routing not in used_routings:
            used_routings.add(routing)
            return routing

def generate_unique_license(country: str) -> str:
    reg = COUNTRY_DATA[country]['regulator']
    while True:
        num = random.randint(10, 999999)
        year = random.randint(2000, CURRENT_YEAR)
        
        if country in ['US', 'GB']:
            lic = f"{reg}-{num:06d}"
        elif country == 'DE':
            lic = f"{reg}-{year}-{num:06d}"
        elif country == 'TR':
            lic = f"{country}-{reg}-{year}-{num:06d}"
        elif country == 'JP':
            lic = f"{reg}-{country}-{num:06d}"
        elif country in ['FR', 'IT', 'NL', 'CH']:
            lic = f"{reg}-EU-{year:02d}-{num:05d}"
        else:
            lic = f"{reg}-{country}-{year}-{num:04d}"
            
        if lic not in used_licenses:
            used_licenses.add(lic)
            return lic

def generate_creation_date() -> datetime.date:
    roll = random.random()
    today = datetime.date.today()
    
    if roll < 0.10:
        year = random.randint(1900, 1959)
    elif roll < 0.85:
        year = random.randint(1960, 2015)
    else:
        year = random.randint(2016, CURRENT_YEAR)
        
    month = random.randint(1, today.month if year == CURRENT_YEAR else 12)
    _, max_day = calendar.monthrange(year, month)
    day = random.randint(1, today.day if (year == CURRENT_YEAR and month == today.month) else max_day)
    
    return datetime.date(year, month, day)

def determine_status(created_date: datetime.date) -> str:
    age_years = CURRENT_YEAR - created_date.year
    roll = random.random() * 100
    
    if age_years > 80:
       
        internal_status = 'Active' if roll <= 65.0 else 'Suspended' if roll <= 75.0 else 'Closed'
    elif age_years <= 5:
        internal_status = 'Active' if roll <= 99.0 else 'Suspended'
    elif age_years <= 20:
        internal_status = 'Active' if roll <= 95.0 else 'Suspended' if roll <= 98.0 else 'Closed'
    else:
        internal_status = 'Active' if roll <= 85.0 else 'Suspended' if roll <= 93.0 else 'Closed'
        
    return STATUS_MAP[internal_status]

def generate_localized_address(country: str, city: str, street_name: str, fake: Faker) -> str:
    if country in ['DE', 'FR', 'NL', 'IT', 'CH']:
        building_no = fake.building_number()
        return f"{street_name} {building_no}, {city}"
    elif country == 'JP':
        chome_block = f"{random.randint(1, 5)}-{random.randint(1, 40)}-{random.randint(1, 15)}"
        return f"{chome_block} {street_name}, {city}"
    else:
        building_no = fake.building_number()
        return f"{building_no} {street_name}, {city}"

def validate_bank(bank: Bank) -> None:
    """Rigidly asserts relational metadata constraints, preventing broken table loads."""

    if len(bank.bic) not in [8, 11]:
        raise ValueError(f"Data Integrity Fault: BIC '{bank.bic}' violates structural SWIFT length rules.")
        
  
    if bank.country_code not in COUNTRY_DATA:
        raise ValueError(f"Metadata Fault: Country Code '{bank.country_code}' not defined in runtime specifications.")
    if bank.headquarters_city not in COUNTRY_DATA[bank.country_code]['cities']:
        raise ValueError(f"Metadata Fault: City '{bank.headquarters_city}' is invalid for country '{bank.country_code}'.")
        
  
    if bank.bank_status not in STATUS_MAP.values():
        raise ValueError(f"State Fault: Status target value '{bank.bank_status}' is invalid.")
        
   
    if bank.country_code == 'US':
        if not bank.routing_no or len(bank.routing_no) != 9 or not bank.routing_no.isdigit():
            raise ValueError(f"Routing Fault: US Route token '{bank.routing_no}' lacks explicit 9-digit format.")
        
        d = [int(char) for char in bank.routing_no]
        checksum = (3 * (d[0] + d[3] + d[6])) + (7 * (d[1] + d[4] + d[7])) + (1 * (d[2] + d[5]))
        if checksum % 10 != d[8]:
            raise ValueError(f"Routing Checksum Fault: US Route token '{bank.routing_no}' failed mathematical validation.")
    else:
        if bank.routing_no is not None:
            raise ValueError(f"Routing Boundary Fault: Non-US entity must possess empty route pointer data maps.")


def generate_banks(count: int) -> List[Bank]:
    bank_collection: List[Bank] = []
    
    for _ in range(count):
        country = random.choices(COUNTRIES, weights=COUNTRY_PROBS, k=1)[0]
        c_meta = COUNTRY_DATA[country]
        fake = FAKERS[country]
        
        city = random.choices(c_meta['cities'], weights=c_meta['city_probs'], k=1)[0]
        street_name = random.choice(c_meta['city_streets'][city])
        address = generate_localized_address(country, city, street_name, fake)
            
        legal_name = generate_unique_name(country)
        bic = generate_unique_bic(legal_name, country, city)
        routing_no = generate_unique_routing(country)
        license_no = generate_unique_license(country)
        created_at = generate_creation_date()
        status_val = determine_status(created_at)
        bank_object = Bank(
            legal_name=legal_name,
            bic=bic,
            routing_no=routing_no,
            country_code=country,
            created_at=created_at,
            bank_status=status_val,
            headquarters_city=city,
            headquarters_address=address,
            license_number=license_no
        )
        validate_bank(bank_object)
        bank_collection.append(bank_object)
        
    return bank_collection

def export_banks_to_sql(banks: List[Bank]) -> None:
    print(f"-- Deterministic Generation Active. Row output validation matches checksum maps.")
    print(f"-- Executing Total Targets: {len(banks)} rows\n")
    for b in banks:
        routing_formatted = f"'{b.routing_no}'" if b.routing_no else "NULL"
        sql_statement = (
            f"INSERT INTO Bank (legal_name, bic, routing_no, country_code, "
            f"created_at, bank_status, headquarters_city, headquarters_address, license_number) "
            f"VALUES ('{b.legal_name.replace("'", "''")}', '{b.bic}', {routing_formatted}, '{b.country_code}', "
            f"'{b.created_at}', '{b.bank_status}', '{b.headquarters_city}', '{b.headquarters_address.replace("'", "''")}', '{b.license_number}');"
        )
        print(sql_statement)

if __name__ == "__main__":
    print("-- High-Fidelity Domain Simulation Engine Initialized.")
    
    generated_banks_pool = generate_banks(250)
    
    export_banks_to_sql(generated_banks_pool)
