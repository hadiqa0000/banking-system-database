CREATE TABLE Bank(
	bank_id BIGINT GENERATED ALWAYS AS IDENTITY,
	legal_name VARCHAR(100) NOT NULL UNIQUE,
	swift_code VARCHAR(11) NOT NULL UNIQUE CHECK(LENGTH(swift_code) =15),
	routing_no VARCHAR(9) NULL CHECK(LENGTH(routing_no)=9),
	country VARCHAR(50) NOT NULL,
	created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	
);

CREATE TABLE Branch(
	bank_id BIGINT NOT NULL,
	branch_id BIGINT GENERATED ALWAYS AS IDENTITY,
	name VARCHAR(100) NOT NULL,
	region VARCHAR(50) NOT NULL,
PRIMARY KEY (bank_id, branch_id), FOREIGN KEY(bank_id) REFERENCES Bank(bank_id) ON DELETE CASCADE, CONSTRAINT uniq_bank_branch_name UNIQUE(bank_id,name)
);

CREATE TABLE Role (
    bank_id BIGINT NOT NULL,
    role_id BIGINT NOT NULL,
    role_name VARCHAR(50) NOT NULL,
    PRIMARY KEY (bank_id, role_id),
    FOREIGN KEY (bank_id) REFERENCES Bank(bank_id) ON DELETE CASCADE,
    CONSTRAINT uniq_bank_role_name UNIQUE (bank_id, role_name)
);

CREATE TABLE Employee(
bank_id BIGINT NOT NULL,
employee_id BIGINT GENERATED ALWAYS AS IDENTITY,
branch_id BIGINT NOT NULL,
role_id VARCHAR(30) NOT NULL,
salary DECIMAL(12,2) NOT NULL CHECK (salary >= 0),
is_active BOOLEAN NOT NULL DEFAULT TRUE,
PRIMARY KEY(bank_id, employee_id), 
FOREIGN KEY(bank_id, branch_id) REFERENCES branch(bank_id, branch_id), 
FOREIGN KEY(bank_id, role_id) REFERENCES role(bank_id, role_id)
);

CREATE TABLE Party (
    bank_id VARCHAR(10) NOT NULL,
    party_id VARCHAR(15) NOT NULL,
    type VARCHAR(15) NOT NULL CHECK (type IN ('individual', 'organization')),
    PRIMARY KEY (bank_id, party_id),
    FOREIGN KEY (bank_id) REFERENCES Bank(bank_id) ON DELETE CASCADE
);
CREATE TABLE Individual (
    bank_id VARCHAR(10) NOT NULL,
    party_id VARCHAR(15) NOT NULL,
    name VARCHAR(100) NOT NULL,
    surname VARCHAR(100) NOT NULL, 
    middle_name VARCHAR(100) NULL,
    dob DATE NOT NULL,
    national_id VARCHAR(20) NOT NULL,
    gender VARCHAR(5) NOT NULL CHECK(gender IN('male', 'female', 'intersex')),
    SSN VARCHAR(9) NULL,
    nationality VARCHAR(100) NOT NULL,
    registeration_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    occupation VARCHAR(10) NULL,
    martial_status VARCHAR(15) NOT NULL CHECK (martial_status IN ('married', 'not married', 'divorced', 'widowed', 'seperated')),
    disability BOOLEAN NOT NULL DEFAULT FALSE,
    disability_type VARCHAR(100) NULL,
    disability_disc VARCHAR(150) NULL,
    annual_income VARCHAR(100) NOT NULL,
    employment_status VARCHAR(100) NOT NULL CHECK(employment_status IN('employed', 'unemployed'),
    country_of_residence VARCHAR(15) NOT NULL,
    city_of_residence VARCHAR(15) NOT NULL,
    district_of_residence VARCHAR(15) NOT NULL,
    
    PRIMARY KEY (bank_id, party_id),
    FOREIGN KEY (bank_id, party_id) REFERENCES Party(bank_id, party_id) ON DELETE CASCADE,
    CONSTRAINT uniq_bank_national_id UNIQUE (bank_id, national_id)
);
