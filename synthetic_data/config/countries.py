    
from dataclasses import dataclass, field
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


@dataclass
class CountryConfig:
    regulator: str
    cities: dict[str, CityConfig]
    
    
    


@dataclass
class CityConfig:
    name: str
    probability: float
    swift_location: str
    streets: list[str] = field(default_factory=list)
    
    def __post_init__(self):
        # Validate probability is between 0 and 1
        if not 0 <= self.probability <= 1:
            raise ValueError(f"Probability must be between 0 and 1, got {self.probability}")
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

# NEW STRUCTURE
COUNTRY_DATA = {
    'US': {
        'regulator': 'OCC',
        'cities': {
            'New York': {
                'probability': 0.45,
                'swift_location': 'NY',
                'streets': ['Wall St', 'Broadway', 'Park Ave', 'Fifth Ave', 'Madison Ave']
            },
            'Chicago': {
                'probability': 0.20,
                'swift_location': 'CH',
                'streets': ['Michigan Ave', 'Clark St', 'State St', 'Wacker Dr']
            },
            'Charlotte': {
                'probability': 0.15,
                'swift_location': 'NC',
                'streets': ['Tryon St', 'College St', 'Trade St']
            },
            'San Francisco': {
                'probability': 0.12,
                'swift_location': 'SF',
                'streets': ['Market St', 'Montgomery St', 'California St']
            },
            'Dallas': {
                'probability': 0.08,
                'swift_location': 'DF',
                'streets': ['Main St', 'Commerce St', 'Elm St']
            }
        }
    },
    
}
    'GB': {
        'regulator': 'FCA',
        'cities': {
            'London': {
                'probability': 0.65,
                'swift_location': 'LN',
                'streets': ['Threadneedle St', 'Canary Wharf', 'Lombard St', 'Fleet St']
            },
            'Edinburgh': {
                'probability': 0.15,
                'swift_location': 'ED',
                'streets': ['George St', 'Princes St', 'Royal Mile']
            },
            'Manchester': {
                'probability': 0.12,
                'swift_location': 'MC',
                'streets': ['Deansgate', 'King St', 'Mosley St']
            },
            'Birmingham': {
                'probability': 0.08,
                'swift_location': 'BM',
                'streets': ['Colmore Row', 'Broad St', 'New St']
            }
        }
    },
    'DE': {
    'regulator': 'BAFIN',
    'cities': {
        'Frankfurt': {
            'probability': 0.55,
            'swift_location': 'FF',
            'streets': ['Kaiserstraße', 'Mainzer Landstraße', 'Neue Mainzer Str.', 'Bockenheimer Landstraße']
        },
        'Munich': {
            'probability': 0.20,
            'swift_location': 'MU',
            'streets': ['Maximilianstraße', 'Ludwigstraße', 'Prinzregentenstraße']
        },
        'Berlin': {
            'probability': 0.15,
            'swift_location': 'BE',
            'streets': ['Friedrichstraße', 'Potsdamer Platz', 'Unter den Linden']
        },
        'Hamburg': {
            'probability': 0.10,
            'swift_location': 'HH',
            'streets': ['Mönckebergstraße', 'Jungfernstieg', 'Neuer Wall']
        }
    }
},
    'JP': {
    'regulator': 'FSA',
    'cities': {
        'Tokyo': {
            'probability': 0.60,
            'swift_location': 'TY',
            'streets': ['Marunouchi', 'Otemachi', 'Ginza', 'Chuo-dori']
        },
        'Osaka': {
            'probability': 0.20,
            'swift_location': 'OS',
            'streets': ['Midosuji Ave', 'Nakanoshima', 'Umeda St']
        },
        'Nagoya': {
            'probability': 0.12,
            'swift_location': 'NG',
            'streets': ['Sakae St', 'Meieki', 'Hirokoji-dori']
        },
        'Yokohama': {
            'probability': 0.08,
            'swift_location': 'YK',
            'streets': ['Minato Mirai', 'Bashamichi', 'Motomachi St']
        }
    }
},
    'TR': {
    'regulator': 'BDDK',
    'cities': {
        'Istanbul': {
            'probability': 0.45,
            'swift_location': 'IS',
            'streets': ['Büyükdere Caddesi', 'Bankalar Caddesi', 'İstiklal Caddesi', 'Bağdat Caddesi']
        },
        'Ankara': {
            'probability': 0.20,
            'swift_location': 'AK',
            'streets': ['Atatürk Bulvarı', 'Cinnah Caddesi', 'Tunalı Hilmi Caddesi']
        },
        'İzmir': {
            'probability': 0.15,
            'swift_location': 'IZ',
            'streets': ['Kordon Boyu', 'Atatürk Caddesi', 'Mithatpaşa Caddesi']
        },
        'Bursa': {
            'probability': 0.20,
            'swift_location': 'BR',
            'streets': ['Atatürk Caddesi', 'Fatih Sultan Mehmet Bulvarı', 'Çekirge Caddesi']
        }
    }
},
    'FR': {
    'regulator': 'ACPR',
    'cities': {
        'Paris': {
            'probability': 0.70,
            'swift_location': 'PP',
            'streets': ['Rue de la Paix', 'Boulevard Haussmann', 'Rue de Rivoli', 'Avenue des Champs-Élysées']
        },
        'Lyon': {
            'probability': 0.18,
            'swift_location': 'LY',
            'streets': ['Rue de la République', 'Rue Garibaldi', 'Avenue Jean Jaurès']
        },
        'Marseille': {
            'probability': 0.12,
            'swift_location': 'MR',
            'streets': ['Rue de la République', 'La Canebière', 'Boulevard Prado']
        }
    }
},'CA': {
    'regulator': 'OSFI',
    'cities': {
        'Toronto': {
            'probability': 0.50,
            'swift_location': 'TO',
            'streets': ['Bay St', 'King St W', 'Front St', 'Yonge St']
        },
        'Montreal': {
            'probability': 0.25,
            'swift_location': 'MO',
            'streets': ['Rue Saint-Jacques', 'René-Lévesque Blvd', 'Rue Notre-Dame']
        },
        'Vancouver': {
            'probability': 0.15,
            'swift_location': 'VA',
            'streets': ['Burrard St', 'Georgia St', 'Granville St']
        },
        'Calgary': {
            'probability': 0.10,
            'swift_location': 'CA',
            'streets': ['2 St SW', 'Centre St S', 'Macleod Trail']
        }
    }
},
    'AU': {
    'regulator': 'APRA',
    'cities': {
        'Sydney': {
            'probability': 0.50,
            'swift_location': 'SY',
            'streets': ['George St', 'Martin Pl', 'Pitt St', 'Macquarie St']
        },
        'Melbourne': {
            'probability': 0.35,
            'swift_location': 'ME',
            'streets': ['Collins St', 'Bourke St', 'Flinders St']
        },
        'Brisbane': {
            'probability': 0.15,
            'swift_location': 'BR',
            'streets': ['Queen St', 'Eagle St', 'Charlotte St']
        }
    }
},
    'IN': {
    'regulator': 'RBI',
    'cities': {
        'Mumbai': {
            'probability': 0.45,
            'swift_location': 'BB',
            'streets': ['Nariman Point', 'Dalal St', 'Bandra Kurla Complex', 'Mahatma Gandhi Road']
        },
        'Delhi': {
            'probability': 0.25,
            'swift_location': 'DE',
            'streets': ['Connaught Place', 'Barakhamba Rd', 'Janpath Rd']
        },
        'Bangalore': {
            'probability': 0.18,
            'swift_location': 'BL',
            'streets': ['MG Road', 'Residency Rd', 'Brigade Rd']
        },
        'Kolkata': {
            'probability': 0.12,
            'swift_location': 'CA',
            'streets': ['Strand Rd', 'Netaji Subhas Rd', 'Park St']
        }
    }
},
    'CN': {
    'regulator': 'NFRA',
    'cities': {
        'Beijing': {
            'probability': 0.40,
            'swift_location': 'BJ',
            'streets': ['Financial Street', 'Jianguomenwai St', 'Fuxingmennei St']
        },
        'Shanghai': {
            'probability': 0.35,
            'swift_location': 'SH',
            'streets': ['Lujiazui Ring Rd', 'The Bund', 'Nanjing Road']
        },
        'Shenzhen': {
            'probability': 0.15,
            'swift_location': 'SZ',
            'streets': ['Shennan Ave', 'Futian District', 'Huafu Rd']
        },
        'Guangzhou': {
            'probability': 0.10,
            'swift_location': 'GZ',
            'streets': ['Zhujiang East Rd', 'Tianhe Rd', 'Zhongshan Rd']
        }
    }
},
   'BR': {
    'regulator': 'BCB',
    'cities': {
        'São Paulo': {
            'probability': 0.55,
            'swift_location': 'SP',
            'streets': ['Avenida Paulista', 'Faria Lima', 'Av. São João', 'Av. Brigadeiro Luís Antônio']
        },
        'Rio de Janeiro': {
            'probability': 0.25,
            'swift_location': 'RJ',
            'streets': ['Avenida Rio Branco', 'Voluntários da Pátria', 'Av. Presidente Vargas']
        },
        'Brasília': {
            'probability': 0.20,
            'swift_location': 'BR',
            'streets': ['SBS Quadra', 'Eixo Monumental', 'SBN Quadra']
        }
    }
},
    'CH': {
    'regulator': 'FINMA',
    'cities': {
        'Zurich': {
            'probability': 0.50,
            'swift_location': 'ZH',
            'streets': ['Bahnhofstrasse', 'Paradeplatz', 'Bleicherweg', 'Talstrasse']
        },
        'Geneva': {
            'probability': 0.30,
            'swift_location': 'GE',
            'streets': ['Rue du Rhône', 'Rue de la Corraterie', 'Rue du Mont-Blanc']
        },
        'Basel': {
            'probability': 0.12,
            'swift_location': 'BS',
            'streets': ['Aeschenvorstadt', 'St. Jakob-Strasse', 'Freie Strasse']
        },
        'Lugano': {
            'probability': 0.08,
            'swift_location': 'LU',
            'streets': ['Via Nassa', 'Piazza Riforma', 'Via Canova']
        }
    }
},
    'IT': {
    'regulator': 'BI',
    'cities': {
        'Milan': {
            'probability': 0.55,
            'swift_location': 'MM',
            'streets': ['Piazza Affari', 'Via Monte Napoleone', 'Via Broletto', 'Corso Matteotti']
        },
        'Rome': {
            'probability': 0.30,
            'swift_location': 'RM',
            'streets': ['Via del Corso', 'Via Veneto', 'Via Nazionale']
        },
        'Turin': {
            'probability': 0.15,
            'swift_location': 'TR',
            'streets': ['Via Roma', 'Corso Vittorio Emanuele II', 'Via Garibaldi']
        }
    }
},
    'NL': {
    'regulator': 'DNB',
    'cities': {
        'Amsterdam': {
            'probability': 0.55,
            'swift_location': 'AD',
            'streets': ['Keizersgracht', 'Damrak', 'Zuidas', 'Herengracht']
        },
        'Rotterdam': {
            'probability': 0.20,
            'swift_location': 'RO',
            'streets': ['Coolsingel', 'Weena', 'Schiedamsedijk']
        },
        'The Hague': {
            'probability': 0.15,
            'swift_location': 'GA',
            'streets': ['Spui', 'Kneuterdijk']
        },
        'Utrecht': {
            'probability': 0.10,
            'swift_location': 'UT',
            'streets': ['Jaarbeursplein', 'Oudegracht', 'Vredenburg']
        }
    }
},
'ZA': {
    'regulator': 'SARB',
    'cities': {
        'Johannesburg': {
            'probability': 0.55,
            'swift_location': 'JJ',
            'streets': ['Fox St', 'Rivonia Rd', 'Alice Lane', 'Main St']
        },
        'Cape Town': {
            'probability': 0.30,
            'swift_location': 'CT',
            'streets': ['Adderley St', 'Long St', 'St Georges Mall']
        },
        'Pretoria': {
            'probability': 0.15,
            'swift_location': 'PR',
            'streets': ['Paul Kruger St', 'Stanza Bopape St', 'Francis Baard St']
        }
    }
}
}

