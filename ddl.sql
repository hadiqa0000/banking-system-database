CREATE TABLE Bank(
	bank_id BIGINT GENERATED ALWAYS AS IDENTITY,
	legal_name VARCHAR(100) NOT NULL UNIQUE,
	swift_code SMALLINT NOT NULL UNIQUE CHECK(LENGTH(swift_code) =15),
	routing_no SMALLINT NULL CHECK(LENGTH(routing_no)=9),
	country VARCHAR(50) NOT NULL,
	created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	
);

CREATE TABLE Branch(
	bank_id BIGINT NOT NULL,
	branch_id BIGINT GENERATED ALWAYS AS IDENTITY,
	name VARCHAR(100) NOT NULL,
	region VARCHAR(50) NOT NULL,
	branch_addres VARCHAR(50) NOT NULL,
	
PRIMARY KEY (bank_id, branch_id), FOREIGN KEY(bank_id) REFERENCES Bank(bank_id) ON DELETE CASCADE, CONSTRAINT uniq_bank_branch_name UNIQUE(bank_id,name)
);

CREATE TABLE Role (
    bank_id BIGINT NOT NULL,
    role_id SMALLINT NOT NULL,
    role_name VARCHAR(50) NOT NULL,
    PRIMARY KEY (bank_id, role_id),
    FOREIGN KEY (bank_id) REFERENCES Bank(bank_id) ON DELETE CASCADE,
    CONSTRAINT uniq_bank_role_name UNIQUE (bank_id, role_name)
);

CREATE TABLE Employee(
bank_id BIGINT NOT NULL,
employee_id SMALLINT GENERATED ALWAYS AS IDENTITY,
branch_id SMALLINT NOT NULL,
role_id SMALLINT NOT NULL,
salary DECIMAL(12,2) NOT NULL CHECK (salary >= 0),
is_active BOOLEAN NOT NULL DEFAULT TRUE,
PRIMARY KEY(bank_id, employee_id), 
FOREIGN KEY(bank_id, branch_id) REFERENCES branch(bank_id, branch_id), 
FOREIGN KEY(bank_id, role_id) REFERENCES role(bank_id, role_id)
);

CREATE TABLE Party (
    bank_id BIGINT NOT NULL,
    party_id SMALLINT NOT NULL,
    type VARCHAR(15) NOT NULL CHECK (type IN ('individual', 'organization')),
    PRIMARY KEY (bank_id, party_id),
    FOREIGN KEY (bank_id) REFERENCES Bank(bank_id) ON DELETE CASCADE
);
CREATE TABLE Individual (
    bank_id BIGINT NOT NULL,
    party_id SMALLINT NOT NULL,
    name VARCHAR(100) NOT NULL,
    surname VARCHAR(100) NOT NULL, 
    middle_name VARCHAR(100) NULL,
    dob DATE NOT NULL,
    national_id VARCHAR(20) NOT NULL,
    gender VARCHAR(7) NOT NULL CHECK(gender IN('male', 'female', 'intersex')),
    SSN VARCHAR(9) NULL,
    nationality VARCHAR(65) NOT NULL,
    registeration_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    occupation VARCHAR(10) NULL,
    martial_status VARCHAR(15) NOT NULL CHECK (martial_status IN ('married', 'not married', 'divorced', 'widowed', 'seperated')),
    disability BOOLEAN NOT NULL DEFAULT FALSE,
    disability_type VARCHAR(100) NULL,
    disability_disc VARCHAR(150) NULL,
    annual_income BIGINT NOT NULL,
    employment_status VARCHAR(100) NOT NULL CHECK(employment_status IN('employed', 'unemployed')),
    country_of_residence VARCHAR(15) NOT NULL,
    city_of_residence VARCHAR(15) NOT NULL,
    district_of_residence VARCHAR(15) NOT NULL,
    customer_status VARCHAR(10) NOT NULL CHECK(customer_status IN('Active', 'inactive', 'blacklisted')),
    deceased_flag BOOLEAN NOT NULL DEFAULT FALSE,
    
    PRIMARY KEY (bank_id, party_id),
    FOREIGN KEY (bank_id, party_id) REFERENCES Party(bank_id, party_id) ON DELETE CASCADE,
    CONSTRAINT uniq_bank_national_id UNIQUE (bank_id, national_id)
);

CREATE TABLE Account(
bank_id BIGINT NOT NULL,
account_id BIGINT NOT NULL,
Branch_id SMALLINT NOT NULL,
account_number VARCHAR(34) NOT NULL,
status VARCHAR(15) NOT NULL DEFAULT 'active' CHECK(status IN('active', 'blacklisted', 'frozen', 'closed')),
account_type VARCHAR(10) NOT NULL CHECK(account_type IN('checking','savings','business','student', 'money market', )),
opened_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
currency_code CHAR(3) NOT NULL,
closed_at TIMESTAMP NULL,
last_activity_at TIMESTAMP,
overdraft_limit DECIMAL(18,2) DEFAULT 0,
Interest_rate DECIMAL(5,2) NULL,
minimum_balance DECIMAL(18,2),
PRIMARY KEY(bank_id, account_id),
FOREIGN KEY(bank_id, branch_id) REFERENCES Branch(bank_id,branch_id),
CONSTRAINT uniq_bank_account_number UNIQUE(bank_id,account_id)

);

CREATE TABLE Account_ownership(
bank_id BIGINT NOT NULL,
account_id VARCHAR(15) NOT NULL,
party_id VARCHAR(15) NOT NULL,
role VARCHAR(15) NOT NULL DEFAULT 'primary' CHECK (role IN('primary', 'joint', 'signatory')),
ownershipt_pct DECIMAL(5,2) NOT NULL DEFAULT 100.00
ownership_start_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
ownership_end_date TIMESTAMP NULL,
ownership_status VARCHAR(15) CHECK (ownership_status IN ('active','inactive','revoked')),
created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
PRIMARY KEY(bank_id,account_id, party_id),
FOREIGN KEY (bank_id,account_id) REFERENCES Account(bank_id,account_id) ON DELETE CASCADE, 
);
FOREIGN KEY(bank_id,party_id) REFERENCES party(bank_id, party_id) ON DELETE CASCADE
);

CREATE TABLE LoanApplication(
bank_id BIGINT NOT NULL,
application_id VARCHAR(20) NOT NULL,
applicant_party_id VARCHAR(15) NOT NULL,
requested_amount DECIMAL(15,2) NOT NULL,
loan_application_status VARCHAR(15) NOT NULL DEFAULT 'Pending' CHECK(loan_application_status IN('pending', 'approved', 'rejected')),
application_sent_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
loan_type VARCHAR(15) NOT NULL CHECK (loan_type IN('personal loan', 'mortgage loan', 'auto loan', 'student loan', 'business loan','credit card loan', 'Term Loan', 'working capital loan', 'business_line_of_credit', 'equipment_financing_loan' ),
requested_term_months SMALLINT NOT NULL CHECK (requested_term_months <=250),
purpose_of_loan VARCHAR(250) NOT NULL,
requested_interest_rate DECIMAL(5,2) NULL CHECK(requested_interest_rate !<0 && !=0),
assigned_employee_id VARCHAR(30) NOT NULL,
decision_at TIMESTAMP  NULL,
rejection_reason VARCHAR(15) NULL,
approved_amount DECIMAL(15,2) NULL,
approved_term_month SMALLINT NULL CHECK(approved_term_month<=250),
approved_interest_rate DECIMAL(5,2) NULL,
PRIMARY KEY(bank_id,application_id),
FOREIGN KEY(bank_id, applicant_party_id) REFERENCES party(bank_id, party_id)
);



