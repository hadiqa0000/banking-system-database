CREATE TABLE Country (
    country_code CHAR(2) PRIMARY KEY,
    country_name VARCHAR(100) NOT NULL UNIQUE
);

INSERT INTO Country VALUES
('US','United States'), ('GB','United Kingdom'), ('TR','Turkey'),
('DE','Germany'), ('FR','France'), ('JP','Japan'), ('CN','China'),
('CA','Canada'), ('AU','Australia'), ('IN','India');

CREATE TABLE Gender (
    gender_name VARCHAR(50) PRIMARY KEY
);

INSERT INTO Gender VALUES
('male'), ('female'), ('intersex'), ('non-binary'), ('unspecified'), ('prefer not to say');

CREATE TABLE Currency (
    currency_code CHAR(3) PRIMARY KEY,
    currency_name VARCHAR(50) NOT NULL,
    currency_symbol VARCHAR(5)
);

INSERT INTO Currency VALUES
('USD','US Dollar','$'), ('EUR','Euro','€'), ('GBP','Pound Sterling','£'),
('TRY','Turkish Lira','₺'), ('JPY','Japanese Yen','¥'), ('CAD','Canadian Dollar','$'),
('AUD','Australian Dollar','$'), ('CHF','Swiss Franc','CHF');

CREATE TABLE CardNetwork (
    network_name VARCHAR(20) PRIMARY KEY
);

INSERT INTO CardNetwork VALUES ('visa'), ('mastercard'), ('amex'), ('discover'), ('unionpay');

CREATE TABLE LoanType (
    loan_type_name VARCHAR(40) PRIMARY KEY
);

INSERT INTO LoanType VALUES 
('personal loan'), ('mortgage loan'), ('auto loan'), ('student loan'), ('business loan'),
('credit card loan'), ('term loan'), ('working capital loan'), ('business_line_of_credit'), ('equipment_financing_loan');

CREATE TABLE AccountType (
    account_type_name VARCHAR(30) PRIMARY KEY
);

INSERT INTO AccountType VALUES ('checking'), ('savings'), ('business'), ('student'), ('money market');

CREATE TABLE PaymentMethod (
    payment_method_name VARCHAR(20) PRIMARY KEY
);

INSERT INTO PaymentMethod VALUES ('cash'), ('bank transfer'), ('debit account'), ('cheque');

CREATE TABLE PaymentFrequency (
    frequency_name VARCHAR(20) PRIMARY KEY
);

INSERT INTO PaymentFrequency VALUES ('weekly'), ('bi-weekly'), ('monthly'), ('quarterly'), ('semi-annual'), ('annual');

CREATE TABLE RiskLevel (
    risk_level_name VARCHAR(10) PRIMARY KEY
);

INSERT INTO RiskLevel VALUES ('low'), ('medium'), ('high');

CREATE TABLE TransactionType (
    transaction_type_name VARCHAR(30) PRIMARY KEY
);

INSERT INTO TransactionType VALUES 
('transfer_internal'), ('transfer_external'), ('deposit_cash'), ('withdrawal_cash'),
('fee_charge'), ('interest_credit'), ('interest_debit'), ('loan_disbursement'), ('card_purchase');

CREATE TABLE TransactionStatus (
    status_name VARCHAR(20) PRIMARY KEY
);

INSERT INTO TransactionStatus VALUES ('pending'), ('authorized'), ('completed'), ('failed'), ('reversed'), ('cancelled'), ('held_compliance');

CREATE TABLE CardStatus (
    status_name VARCHAR(25) PRIMARY KEY
);

INSERT INTO CardStatus VALUES ('pending_activation'), ('active'), ('frozen'), ('blocked'), ('expired'), ('cancelled'), ('stolen'), ('lost');

CREATE TABLE ATMStatus (
    status_name VARCHAR(20) PRIMARY KEY
);

INSERT INTO ATMStatus VALUES ('active'), ('out_of_service'), ('maintenance');

CREATE TABLE LockerSize (
    size_name VARCHAR(10) PRIMARY KEY
);

INSERT INTO LockerSize VALUES ('small'), ('medium'), ('large');

CREATE TABLE OrganizationType (
    organization_type_name VARCHAR(40) PRIMARY KEY
);

INSERT INTO OrganizationType VALUES ('sole proprietorship'), ('partnership'), ('private limited'), ('public limited'), ('government'), ('non-profit'), ('bank'), ('corporation');

CREATE TABLE AccountStatus (
    status_name VARCHAR(20) PRIMARY KEY
);

INSERT INTO AccountStatus VALUES ('active'), ('frozen'), ('closed'), ('blacklisted');

CREATE TABLE BankStatus (
    status_name VARCHAR(20) PRIMARY KEY
);

INSERT INTO BankStatus VALUES ('active'), ('suspended'), ('closed');

CREATE TABLE AuditActorType (
    actor_type VARCHAR(20) PRIMARY KEY,
    description VARCHAR(100) NOT NULL
);

INSERT INTO AuditActorType VALUES ('employee', 'Bank employee'), ('system', 'Automated internal system'), ('api', 'External API client'), ('scheduler', 'Scheduled background job');

CREATE TABLE AuditEntityType (
    entity_type VARCHAR(30) PRIMARY KEY,
    description VARCHAR(100)
);

INSERT INTO AuditEntityType VALUES 
('Bank','Bank'), ('Branch','Branch'), ('Employee','Employee'), ('Role','Role'), ('Party','Party'),
('Individual','Individual'), ('Organization','Organization'), ('Account','Account'), ('AccountOwnership','Account Ownership'),
('Transaction','Transaction'), ('JournalEntry','Journal Entry'), ('JournalLine','Journal Line'), ('LoanApplication','Loan Application'),
('CreditAssessment','Credit Assessment'), ('Loan','Loan'), ('LoanPayment','Loan Payment'), ('CardProduct','Card Product'),
('Card','Card'), ('CardApplication','Card Application'), ('ATM','ATM'), ('ATMTransaction','ATM Transaction'), ('Locker','Locker');

CREATE TABLE AuditAction (
    action_name VARCHAR(20) PRIMARY KEY,
    description VARCHAR(100)
);

INSERT INTO AuditAction VALUES ('INSERT','Row inserted'), ('UPDATE','Row updated'), ('DELETE','Row deleted'), ('LOGIN','User login'), ('LOGOUT','User logout'), ('APPROVE','Approval action'), ('REJECT','Rejection action');

CREATE TABLE EmploymentStatus (
    employment_status VARCHAR(20) PRIMARY KEY,
    description VARCHAR(100)
);

INSERT INTO EmploymentStatus VALUES 
('active', 'Currently employed'), ('on_leave', 'Temporarily on leave'), 
('suspended', 'Employment temporarily suspended'), ('terminated', 'Employment terminated');

CREATE TABLE AuditSource (
    source_name VARCHAR(20) PRIMARY KEY
);
INSERT INTO AuditSource VALUES ('web'), ('mobile'), ('atm'), ('system_core');

CREATE TABLE LockerAccessRole (
    role_name VARCHAR(20) PRIMARY KEY,
    description VARCHAR(100)
);

INSERT INTO LockerAccessRole VALUES 
('primary', 'Main leaseholder responsible for billing and ultimate access control'),
('co-renter', 'Joint leaseholder with full access rights to the physical locker'),
('authorized_visitor', 'Allowed physical access under supervision, cannot alter lease terms');

CREATE TABLE BorrowerRole (
    role_name VARCHAR(20) PRIMARY KEY,
    description VARCHAR(100)
);

INSERT INTO BorrowerRole VALUES 
('primary', 'Main borrower whose income is primarily used for underwriting'),
('co-borrower', 'Joint borrower equally responsible for monthly payments'),
('guarantor', 'Provides a payment guarantee; only legally liable upon default of primaries');

CREATE TABLE Bank (
    bank_id BIGINT GENERATED ALWAYS AS IDENTITY,
    legal_name VARCHAR(100) NOT NULL UNIQUE,
    bic VARCHAR(11) NOT NULL UNIQUE CHECK (LENGTH(bic) IN (8, 11)),
    routing_no VARCHAR(9) NULL CHECK (LENGTH(routing_no) = 9),
    country_code CHAR(2) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    bank_status VARCHAR(20) NOT NULL,
    headquarters_city VARCHAR(100) NOT NULL,
    headquarters_address VARCHAR(255) NOT NULL,
    license_number VARCHAR(50) NOT NULL,
    PRIMARY KEY (bank_id),
    FOREIGN KEY (country_code) REFERENCES Country(country_code),
    FOREIGN KEY (bank_status) REFERENCES BankStatus(status_name)
);

CREATE TABLE Branch (
    bank_id BIGINT NOT NULL,
    branch_id BIGINT GENERATED ALWAYS AS IDENTITY,
    name VARCHAR(100) NOT NULL,
    region VARCHAR(50) NOT NULL,
    branch_address VARCHAR(255) NOT NULL, 
    country_code CHAR(2) NOT NULL,
    PRIMARY KEY (bank_id, branch_id), 
    FOREIGN KEY (bank_id) REFERENCES Bank(bank_id) ON DELETE CASCADE, 
    CONSTRAINT uniq_bank_branch_name UNIQUE (bank_id, name),
    FOREIGN KEY (country_code) REFERENCES Country(country_code)
);

CREATE TABLE Role (
    bank_id BIGINT NOT NULL,
    role_id BIGINT GENERATED ALWAYS AS IDENTITY, 
    role_name VARCHAR(50) NOT NULL,
    PRIMARY KEY (bank_id, role_id),
    FOREIGN KEY (bank_id) REFERENCES Bank(bank_id) ON DELETE CASCADE,
    CONSTRAINT uniq_bank_role_name UNIQUE (bank_id, role_name)
);

CREATE TABLE Employee (
    bank_id BIGINT NOT NULL,
    employee_id BIGINT GENERATED ALWAYS AS IDENTITY,
    branch_id BIGINT NOT NULL,
    employee_gender VARCHAR(50) NOT NULL,
    role_id BIGINT NOT NULL,
    manager_id BIGINT NULL, 
    employee_number VARCHAR(30) NOT NULL,
    employee_work_email VARCHAR(255) NOT NULL,
    employee_phone VARCHAR(30) NULL,
    employee_salary DECIMAL(12, 2) NOT NULL CHECK (employee_salary >= 0), -- Fixed variable reference
    employee_hire_date DATE NOT NULL DEFAULT CURRENT_DATE,
    employee_termination_date DATE NULL,
    employment_status VARCHAR(20) NOT NULL DEFAULT 'active',
    employee_is_active BOOLEAN NOT NULL DEFAULT TRUE,
    PRIMARY KEY (bank_id, employee_id), 
    FOREIGN KEY (bank_id, branch_id) REFERENCES Branch(bank_id, branch_id), 
    FOREIGN KEY (bank_id, role_id) REFERENCES Role(bank_id, role_id),
    FOREIGN KEY (bank_id, manager_id) REFERENCES Employee(bank_id, employee_id) ON DELETE SET NULL,
    CONSTRAINT uniq_bank_employee_number UNIQUE (bank_id, employee_number),
    CONSTRAINT uniq_bank_employee_email UNIQUE (bank_id, employee_work_email),
    CONSTRAINT chk_termination_after_hire CHECK (employee_termination_date IS NULL OR employee_termination_date >= employee_hire_date),
    FOREIGN KEY (employment_status) REFERENCES EmploymentStatus(employment_status),
    FOREIGN KEY (employee_gender) REFERENCES Gender(gender_name)
);

CREATE TABLE Party (
    bank_id BIGINT NOT NULL,
    party_id BIGINT GENERATED ALWAYS AS IDENTITY,
    party_type VARCHAR(15) NOT NULL CHECK (party_type IN ('individual', 'organization')), 
    PRIMARY KEY (bank_id, party_id),
    FOREIGN KEY (bank_id) REFERENCES Bank(bank_id) ON DELETE CASCADE
);

CREATE TABLE Individual (
    bank_id BIGINT NOT NULL,
    party_id BIGINT NOT NULL,
    name VARCHAR(100) NOT NULL,
    surname VARCHAR(100) NOT NULL, 
    middle_name VARCHAR(100) NULL,
    dob DATE NOT NULL,
    national_id VARCHAR(20) NOT NULL,
    individual_gender VARCHAR(10) NOT NULL,
    SSN VARCHAR(9) NULL,
    nationality VARCHAR(65) NOT NULL,
    registration_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP, 
    occupation VARCHAR(100) NULL, 
    marital_status VARCHAR(15) NOT NULL CHECK (marital_status IN ('married', 'single', 'divorced', 'widowed', 'separated')),
    disability BOOLEAN NOT NULL DEFAULT FALSE,
    disability_type VARCHAR(100) NULL,
    disability_desc VARCHAR(150) NULL,
    annual_income DECIMAL(15, 2) NOT NULL CHECK (annual_income >= 0), 
    employment_status VARCHAR(100) NOT NULL CHECK (employment_status IN ('employed', 'unemployed', 'self_employed', 'retired')),
    country_of_residence CHAR(2) NOT NULL, 
    city_of_residence VARCHAR(100) NOT NULL,
    district_of_residence VARCHAR(100) NOT NULL,
    customer_status VARCHAR(15) NOT NULL CHECK (customer_status IN ('active', 'inactive', 'blacklisted')),
    deceased_flag BOOLEAN NOT NULL DEFAULT FALSE,
    PRIMARY KEY (bank_id, party_id),
    FOREIGN KEY (bank_id, party_id) REFERENCES Party(bank_id, party_id) ON DELETE CASCADE,
    CONSTRAINT uniq_bank_national_id UNIQUE (bank_id, national_id),
    FOREIGN KEY (country_of_residence) REFERENCES Country(country_code),
    FOREIGN KEY (individual_gender) REFERENCES Gender(gender_name)
);

CREATE TABLE Organization (
    bank_id BIGINT NOT NULL,
    party_id BIGINT NOT NULL,
    legal_name VARCHAR(200) NOT NULL,
    trading_name VARCHAR(200) NULL,
    registration_number VARCHAR(50) NOT NULL,
    tax_id VARCHAR(50) NOT NULL,
    organization_type VARCHAR(40) NOT NULL,
    industry VARCHAR(100) NULL,
    incorporation_date DATE NOT NULL,
    email VARCHAR(255) NULL,
    phone_number VARCHAR(30) NULL,
    website VARCHAR(255) NULL,
    annual_revenue DECIMAL(18,2) NULL CHECK (annual_revenue >= 0),
    employee_count INT NULL CHECK (employee_count >= 0),
    PRIMARY KEY (bank_id, party_id),
    FOREIGN KEY (bank_id, party_id) REFERENCES Party(bank_id, party_id) ON DELETE CASCADE,
    CONSTRAINT uniq_bank_registration UNIQUE (bank_id, registration_number),
    CONSTRAINT uniq_bank_tax_id UNIQUE (bank_id, tax_id),
    FOREIGN KEY (organization_type) REFERENCES OrganizationType(organization_type_name)
);

CREATE TABLE Account (
    bank_id BIGINT NOT NULL,
    account_id BIGINT GENERATED ALWAYS AS IDENTITY,
    branch_id BIGINT NOT NULL,
    currency_code CHAR(3) NOT NULL,
    account_number VARCHAR(34) NOT NULL,
    current_balance DECIMAL(18,2) NOT NULL DEFAULT 0.00,
    available_balance DECIMAL(18,2) NOT NULL DEFAULT 0.00,
    account_status VARCHAR(20) NOT NULL,
    account_type VARCHAR(30) NOT NULL,
    opened_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    closed_at TIMESTAMP NULL,
    last_activity_at TIMESTAMP NULL,
    overdraft_limit DECIMAL(18, 2) DEFAULT 0 CHECK (overdraft_limit >= 0),
    interest_rate DECIMAL(5, 2) NULL CHECK (interest_rate >= 0),
    minimum_balance DECIMAL(18, 2) NULL DEFAULT 0 CHECK (minimum_balance >= 0),
    PRIMARY KEY (bank_id, account_id),
    FOREIGN KEY (bank_id, branch_id) REFERENCES Branch(bank_id, branch_id),
    CONSTRAINT uniq_bank_account_number UNIQUE (bank_id, account_number),
    FOREIGN KEY (currency_code) REFERENCES Currency(currency_code),
    FOREIGN KEY (account_type) REFERENCES AccountType(account_type_name),
    FOREIGN KEY (account_status) REFERENCES AccountStatus(status_name)
);

CREATE TABLE Account_ownership (
    bank_id BIGINT NOT NULL,
    account_id BIGINT NOT NULL,
    party_id BIGINT NOT NULL,
    role VARCHAR(15) NOT NULL DEFAULT 'primary' CHECK (role IN ('primary', 'joint', 'signatory')),
    ownership_pct DECIMAL(5, 2) NOT NULL DEFAULT 100.00 CHECK (ownership_pct BETWEEN 0 AND 100),
    ownership_start_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    ownership_end_date TIMESTAMP NULL,
    ownership_status VARCHAR(15) CHECK (ownership_status IN ('active', 'inactive', 'revoked')),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (bank_id, account_id, party_id),
    FOREIGN KEY (bank_id, account_id) REFERENCES Account(bank_id, account_id) ON DELETE CASCADE,
    FOREIGN KEY (bank_id, party_id) REFERENCES Party(bank_id, party_id) ON DELETE CASCADE
);

CREATE TABLE JournalEntry (
    bank_id BIGINT NOT NULL,
    journal_id BIGINT GENERATED ALWAYS AS IDENTITY,
    entry_timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    reference_type VARCHAR(20) NOT NULL,
    reference_id BIGINT NOT NULL,
    description VARCHAR(255) NOT NULL,
    posting_status VARCHAR(15) NOT NULL CHECK (posting_status IN ('draft', 'posted', 'reversed')),
    posted_at TIMESTAMP NULL,
    posted_by_employee_id BIGINT NULL,
    source_system VARCHAR(30) NOT NULL,
    reversal_of_journal_id BIGINT NULL,
    batch_id BIGINT NULL,
    currency_code CHAR(3) NOT NULL,
    PRIMARY KEY (bank_id, journal_id),
    FOREIGN KEY (bank_id) REFERENCES Bank(bank_id) ON DELETE CASCADE,
    FOREIGN KEY (bank_id, posted_by_employee_id) REFERENCES Employee(bank_id, employee_id),
    FOREIGN KEY (currency_code) REFERENCES Currency(currency_code)
);

CREATE TABLE Bank_Transaction (
    bank_id BIGINT NOT NULL,
    transaction_id BIGINT GENERATED ALWAYS AS IDENTITY,
    journal_id BIGINT NULL,
    reversal_of_transaction_id BIGINT NULL,
    from_account_id BIGINT NULL, 
    to_account_id BIGINT NULL,
    initiated_by_party_id BIGINT NULL,
    initiated_by_employee_id BIGINT NULL,
    authorized_by_employee_id BIGINT NULL, 
    amount DECIMAL(15, 2) NOT NULL CHECK (amount > 0),
    currency_code CHAR(3) NOT NULL,
    exchange_rate DECIMAL(18, 8) NOT NULL DEFAULT 1.00000000,
    converted_amount DECIMAL(18, 8) NOT NULL,
    fee_amount DECIMAL(15, 2) NOT NULL DEFAULT 0.00 CHECK (fee_amount >= 0),
    transaction_type VARCHAR(30) NOT NULL,
    transaction_status VARCHAR(20) NOT NULL DEFAULT 'pending', 
    channel VARCHAR(15) NOT NULL CHECK (channel IN ('branch', 'atm', 'online_banking', 'mobile_app', 'pos_terminal', 'open_api', 'batch_system')),
    authorization_code VARCHAR(20) NULL,
    response_code CHAR(4) NULL, 
    idempotency_key UUID NOT NULL,
    mfa_verified BOOLEAN NOT NULL DEFAULT FALSE,
    aml_risk_score DECIMAL(5, 2) NULL CHECK (aml_risk_score BETWEEN 0 AND 100),
    fraud_flagged BOOLEAN NOT NULL DEFAULT FALSE,
    compliance_hold_reason VARCHAR(255) NULL,
    value_date DATE NOT NULL, 
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    authorized_at TIMESTAMP NULL,
    completed_at TIMESTAMP NULL,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    transaction_description VARCHAR(255) NULL,
    payment_reference VARCHAR(100) NULL,
    custom_metadata JSONB NULL,
    PRIMARY KEY (bank_id, transaction_id),
    FOREIGN KEY (bank_id) REFERENCES Bank(bank_id) ON DELETE CASCADE,
    FOREIGN KEY (bank_id, from_account_id) REFERENCES Account(bank_id, account_id),
    FOREIGN KEY (bank_id, to_account_id) REFERENCES Account(bank_id, account_id),
    FOREIGN KEY (bank_id, initiated_by_party_id) REFERENCES Party(bank_id, party_id),
    FOREIGN KEY (bank_id, initiated_by_employee_id) REFERENCES Employee(bank_id, employee_id),
    FOREIGN KEY (bank_id, authorized_by_employee_id) REFERENCES Employee(bank_id, employee_id),
    FOREIGN KEY (bank_id, reversal_of_transaction_id) REFERENCES Bank_Transaction(bank_id, transaction_id) ON DELETE SET NULL,
    CONSTRAINT uniq_bank_idempotency UNIQUE (bank_id, idempotency_key),
    CONSTRAINT chk_at_least_one_account CHECK (from_account_id IS NOT NULL OR to_account_id IS NOT NULL),
    CONSTRAINT chk_exclusive_initiator CHECK (
        (initiated_by_party_id IS NULL AND initiated_by_employee_id IS NULL) OR 
        (initiated_by_party_id IS NOT NULL AND initiated_by_employee_id IS NULL) OR 
        (initiated_by_party_id IS NULL AND initiated_by_employee_id IS NOT NULL)),
    CONSTRAINT chk_cannot_reverse_self CHECK (reversal_of_transaction_id IS NULL OR reversal_of_transaction_id <> transaction_id),
    CONSTRAINT chk_account_directionality CHECK (
        from_account_id IS NULL OR 
        to_account_id IS NULL OR 
        from_account_id <> to_account_id),
    FOREIGN KEY (transaction_type) REFERENCES TransactionType(transaction_type_name),
    FOREIGN KEY (transaction_status) REFERENCES TransactionStatus(status_name),
    FOREIGN KEY (bank_id, journal_id) REFERENCES JournalEntry(bank_id, journal_id) ON DELETE SET NULL,
    FOREIGN KEY (currency_code) REFERENCES Currency(currency_code)
);

CREATE TABLE JournalLine (
    bank_id BIGINT NOT NULL,
    journal_id BIGINT NOT NULL,
    line_id BIGINT GENERATED ALWAYS AS IDENTITY,
    account_id BIGINT NOT NULL,
    debit DECIMAL(15, 2) NOT NULL DEFAULT 0.00,
    credit DECIMAL(15, 2) NOT NULL DEFAULT 0.00,
    description VARCHAR(255) NULL,
    line_number BIGINT NOT NULL,
    currency_code CHAR(3) NOT NULL,
    exchange_rate DECIMAL(18, 8) NULL DEFAULT 1.00000000,
    PRIMARY KEY (bank_id, journal_id, line_id),
    FOREIGN KEY (bank_id, journal_id) REFERENCES JournalEntry(bank_id, journal_id) ON DELETE CASCADE,
    FOREIGN KEY (bank_id, account_id) REFERENCES Account(bank_id, account_id),
    CONSTRAINT chk_debit CHECK (debit >= 0),
    CONSTRAINT chk_credit CHECK (credit >= 0),
    CONSTRAINT chk_debit_and_credit CHECK ((debit > 0 AND credit = 0) OR (credit > 0 AND debit = 0)),
    FOREIGN KEY (currency_code) REFERENCES Currency(currency_code)
);

CREATE TABLE LoanApplication (
    bank_id BIGINT NOT NULL,
    application_id BIGINT GENERATED ALWAYS AS IDENTITY,
    requested_amount DECIMAL(15, 2) NOT NULL CHECK (requested_amount > 0),
    loan_application_status VARCHAR(15) NOT NULL DEFAULT 'pending' CHECK (loan_application_status IN ('pending', 'approved', 'rejected', 'cancelled')),
    application_sent_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    loan_type_name VARCHAR(40) NOT NULL,
    requested_term_months SMALLINT NOT NULL CHECK (requested_term_months > 0),
    purpose_of_loan VARCHAR(250) NOT NULL,
    requested_interest_rate DECIMAL(5, 2) NULL CHECK (requested_interest_rate > 0),
    assigned_employee_id BIGINT NULL, 
    decision_at TIMESTAMP NULL,
    rejection_reason VARCHAR(255) NULL,
    approved_amount DECIMAL(15, 2) NULL CHECK (approved_amount >= 0),
    approved_term_month SMALLINT NULL CHECK (approved_term_month > 0),
    approved_interest_rate DECIMAL(5, 2) NULL CHECK (approved_interest_rate >= 0),
    PRIMARY KEY (bank_id, application_id),
    FOREIGN KEY (bank_id, assigned_employee_id) REFERENCES Employee(bank_id, employee_id), 
    FOREIGN KEY (loan_type_name) REFERENCES LoanType(loan_type_name)
);

CREATE TABLE CreditAssessment (
    bank_id BIGINT NOT NULL,
    assessment_id BIGINT GENERATED ALWAYS AS IDENTITY,
    application_id BIGINT NOT NULL,
    employee_id BIGINT NOT NULL,
    score INT NOT NULL,
    risk_level VARCHAR(10) NOT NULL,
    assessment_method VARCHAR(15) NOT NULL CHECK (assessment_method IN ('manual', 'automated', 'hybrid')),
    recommendation VARCHAR(15) NOT NULL CHECK (recommendation IN ('approve', 'reject', 'manual_review')),
    assessment_version VARCHAR(20) NOT NULL,
    debt_to_income_ratio DECIMAL(5, 2) NULL CHECK (debt_to_income_ratio >= 0),
    annual_income_snapshot DECIMAL(15, 2) NULL CHECK (annual_income_snapshot >= 0),
    monthly_expenses_snapshot DECIMAL(15, 2) NULL CHECK (monthly_expenses_snapshot >= 0),
    comments TEXT NULL,
    assessed_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP NULL,
    PRIMARY KEY (bank_id, assessment_id),
    FOREIGN KEY (bank_id, application_id) REFERENCES LoanApplication(bank_id, application_id),
    FOREIGN KEY (bank_id, employee_id) REFERENCES Employee(bank_id, employee_id),
    FOREIGN KEY (risk_level) REFERENCES RiskLevel(risk_level_name)
);

CREATE TABLE Loan (
    bank_id BIGINT NOT NULL,
    loan_id BIGINT GENERATED ALWAYS AS IDENTITY,
    application_id BIGINT NOT NULL,
    account_id BIGINT NOT NULL,
    principal DECIMAL(15, 2) NOT NULL CHECK (principal > 0),
    interest_rate DECIMAL(5, 4) NOT NULL CHECK (interest_rate >= 0),
    disbursed_at TIMESTAMP NULL,
    loan_status VARCHAR(15) NOT NULL DEFAULT 'active' CHECK (loan_status IN ('active', 'performing', 'delinquent', 'defaulted', 'charged_off', 'closed')),
    maturity_date DATE NOT NULL,
    next_payment_due_date DATE NOT NULL,
    payment_frequency VARCHAR(20) NOT NULL, 
    installment_amount DECIMAL(15, 2) NOT NULL CHECK (installment_amount >= 0),
    currency_code CHAR(3) NOT NULL,
    late_fee_rate DECIMAL(5, 4) NOT NULL CHECK (late_fee_rate >= 0),
    grace_period_days SMALLINT NULL DEFAULT 0 CHECK (grace_period_days >= 0),
    closed_at DATE NULL,
    closure_reason VARCHAR(40) NULL CHECK (closure_reason IN ('paid in full', 'early closure', 'refinancing', 'one-time settlement', 'default and charge-off', 'sent to collections', 'fraud or policy violation')),
    PRIMARY KEY (bank_id, loan_id),
    FOREIGN KEY (bank_id, application_id) REFERENCES LoanApplication(bank_id, application_id),
    FOREIGN KEY (bank_id, account_id) REFERENCES Account(bank_id, account_id),
    CONSTRAINT uniq_bank_application UNIQUE (bank_id, application_id),
    FOREIGN KEY (currency_code) REFERENCES Currency(currency_code),
    FOREIGN KEY (payment_frequency) REFERENCES PaymentFrequency(frequency_name)
);

CREATE TABLE LoanPayment (
    bank_id BIGINT NOT NULL,
    payment_id BIGINT GENERATED ALWAYS AS IDENTITY,
    loan_id BIGINT NOT NULL,
    journal_id BIGINT NOT NULL,
    total_amount_paid DECIMAL(15, 2) NOT NULL,
    principal_component DECIMAL(15, 2) NOT NULL,
    interest_component DECIMAL(15, 2) NOT NULL,
    payment_status VARCHAR(20) NOT NULL DEFAULT 'pending' CHECK (payment_status IN ('pending', 'completed', 'failed', 'reversed')),
    payment_method VARCHAR(20) NOT NULL, 
    payment_channel VARCHAR(20) CHECK (payment_channel IN ('branch', 'atm', 'online', 'mobile', 'api')),
    installment_number SMALLINT NOT NULL,
    remaining_balance_after_payment DECIMAL(15, 2) NOT NULL,
    late_fee_component DECIMAL(15, 2) NULL DEFAULT 0.00,
    penalty_interest_component DECIMAL(15, 2) NULL DEFAULT 0.00,
    payment_reference VARCHAR(50) NULL,
    paid_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (bank_id, payment_id),
    FOREIGN KEY (bank_id, loan_id) REFERENCES Loan(bank_id, loan_id),
    FOREIGN KEY (bank_id, journal_id) REFERENCES JournalEntry(bank_id, journal_id) ON DELETE CASCADE,
    CONSTRAINT uniq_bank_payment_journal UNIQUE (bank_id, journal_id),
    CONSTRAINT uniq_bank_payment_reference UNIQUE (bank_id, payment_reference),
    CONSTRAINT chk_principal_component CHECK (principal_component >= 0),
    CONSTRAINT chk_interest_component CHECK (interest_component >= 0),
    CONSTRAINT chk_late_fee CHECK (late_fee_component >= 0),
    CONSTRAINT chk_penalty_interest CHECK (penalty_interest_component >= 0),
    CONSTRAINT chk_remaining_balance CHECK (remaining_balance_after_payment >= 0),
    CONSTRAINT chk_installment_number CHECK (installment_number > 0),
    FOREIGN KEY (payment_method) REFERENCES PaymentMethod(payment_method_name),
    CONSTRAINT chk_total_amount CHECK (total_amount_paid = principal_component + interest_component + COALESCE(late_fee_component, 0) + COALESCE(penalty_interest_component, 0))
);

CREATE TABLE CardProduct (
    bank_id BIGINT NOT NULL,
    card_product_id BIGINT GENERATED ALWAYS AS IDENTITY,
    product_name VARCHAR(100) NOT NULL,
    card_type VARCHAR(15) NOT NULL CHECK (card_type IN ('debit', 'credit', 'prepaid', 'charge')),
    card_segment VARCHAR(20) NOT NULL CHECK (card_segment IN ('consumer', 'business', 'corporate', 'private_banking')),
    card_network VARCHAR(20) NOT NULL,
    supports_contactless BOOLEAN NOT NULL DEFAULT TRUE,
    daily_atm_withdrawal_limit DECIMAL(15, 2) NULL DEFAULT 0 CHECK (daily_atm_withdrawal_limit >= 0),
    daily_purchase_limit DECIMAL(15, 2) NOT NULL CHECK (daily_purchase_limit >= 0),
    min_age SMALLINT NOT NULL CHECK (min_age >= 0),
    min_cred_score SMALLINT NULL CHECK (min_cred_score BETWEEN 300 AND 850),
    annual_fee DECIMAL(15, 2) NOT NULL DEFAULT 0.00 CHECK (annual_fee >= 0), 
    PRIMARY KEY (bank_id, card_product_id),
    FOREIGN KEY (bank_id) REFERENCES Bank(bank_id) ON DELETE CASCADE,
    FOREIGN KEY (card_network) REFERENCES CardNetwork(network_name)
);

CREATE TABLE Card (
    bank_id BIGINT NOT NULL,
    card_id BIGINT GENERATED ALWAYS AS IDENTITY,
    card_product_id BIGINT NOT NULL,
    account_id BIGINT NOT NULL,
    card_number VARCHAR(19) NOT NULL,
    card_token_id UUID NOT NULL UNIQUE,
    card_expiry_date DATE NOT NULL,
    card_status VARCHAR(20) NOT NULL,
    card_issued_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    crd_activated_at TIMESTAMP NULL,
    cardholder_name VARCHAR(100) NOT NULL,
    card_last_used_at TIMESTAMP NULL,
    card_pin_retry_count SMALLINT DEFAULT 0 CHECK (card_pin_retry_count BETWEEN 0 AND 3), 
    card_pin_last_changed_at TIMESTAMP NULL,             
    card_replacement_reason VARCHAR(20) NULL CHECK (card_replacement_reason IN ('expired', 'lost', 'stolen', 'damaged')), 
    PRIMARY KEY (bank_id, card_id),
    FOREIGN KEY (bank_id, account_id) REFERENCES Account(bank_id, account_id) ON DELETE CASCADE,
    FOREIGN KEY (bank_id, card_product_id) REFERENCES CardProduct(bank_id, card_product_id),
    CONSTRAINT uniq_bank_card_number UNIQUE (bank_id, card_number),
    FOREIGN KEY (card_status) REFERENCES CardStatus(status_name)
);

CREATE TABLE CardApplication (
    bank_id BIGINT NOT NULL,
    account_id BIGINT NOT NULL,
    card_application_id BIGINT GENERATED ALWAYS AS IDENTITY, 
    card_applicant_party_id BIGINT NOT NULL,
    card_product_id BIGINT NOT NULL, 
    card_application_status VARCHAR(20) NOT NULL CHECK (card_application_status IN ('pending', 'approved', 'rejected', 'cancelled')), 
    card_submitted_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    card_reviewed_at TIMESTAMP NULL,
    card_reviewed_by_employee_id BIGINT NULL,
    card_rejection_reason VARCHAR(500) NULL,
    approved_card_id BIGINT NULL,
    PRIMARY KEY (bank_id, card_application_id), 
    FOREIGN KEY (bank_id, card_applicant_party_id) REFERENCES Party(bank_id, party_id),
    FOREIGN KEY (bank_id, card_product_id) REFERENCES CardProduct(bank_id, card_product_id),
    FOREIGN KEY (bank_id, approved_card_id) REFERENCES Card(bank_id, card_id),
    FOREIGN KEY (bank_id, account_id) REFERENCES Account(bank_id, account_id)
);

CREATE TABLE ATM (
    bank_id BIGINT NOT NULL,
    atm_id BIGINT GENERATED ALWAYS AS IDENTITY,
    branch_id BIGINT NOT NULL,
    atm_terminal_id BIGINT NOT NULL,
    atm_status VARCHAR(15) NOT NULL DEFAULT 'active',
    atm_location_address VARCHAR(255) NOT NULL,
    atm_installed_at TIMESTAMP NOT NULL,
    atm_last_maintenance_at TIMESTAMP NOT NULL,
    atm_next_maintenance_due DATE NOT NULL,
    atm_cash_capacity DECIMAL(15, 2) NOT NULL CHECK (atm_cash_capacity >= 0), 
    atm_current_cash_balance DECIMAL(15, 2) NOT NULL CHECK (atm_current_cash_balance >= 0), 
    atm_supports_cash_deposit BOOLEAN NOT NULL DEFAULT FALSE,
    atm_supports_contactless BOOLEAN NOT NULL DEFAULT FALSE,
    atm_supports_cardless BOOLEAN NOT NULL DEFAULT FALSE,
    atm_supports_statement_printing BOOLEAN NOT NULL DEFAULT TRUE,
    atm_supports_cash_recycling BOOLEAN NOT NULL DEFAULT FALSE,
    PRIMARY KEY (bank_id, atm_id),
    FOREIGN KEY (bank_id, branch_id) REFERENCES Branch(bank_id, branch_id),
    CONSTRAINT uniq_bank_terminal UNIQUE (bank_id, atm_terminal_id),
    FOREIGN KEY (atm_status) REFERENCES ATMStatus(status_name) -- Completed truncated line
);



CREATE TABLE LoanApplicationApplicant (
    bank_id BIGINT NOT NULL,
    application_id BIGINT NOT NULL,
    party_id BIGINT NOT NULL,
    applicant_role VARCHAR(20) NOT NULL DEFAULT 'primary', 
    credit_score_snapshot INT NULL,                       
    declared_monthly_income DECIMAL(15, 2) NOT NULL CHECK (declared_monthly_income >= 0),
    PRIMARY KEY (bank_id, application_id, party_id),
    FOREIGN KEY (bank_id, application_id) REFERENCES LoanApplication(bank_id, application_id) ON DELETE CASCADE,
    FOREIGN KEY (bank_id, party_id) REFERENCES Party(bank_id, party_id) ON DELETE CASCADE,
    FOREIGN KEY (applicant_role) REFERENCES BorrowerRole(role_name)
);

CREATE TABLE LoanBorrower (
    bank_id BIGINT NOT NULL,
    loan_id BIGINT NOT NULL,
    party_id BIGINT NOT NULL,
    borrower_role VARCHAR(20) NOT NULL DEFAULT 'primary', 
    liability_pct DECIMAL(5, 2) NOT NULL DEFAULT 100.00 CHECK (liability_pct BETWEEN 0 AND 100), 
    is_signed_agreement BOOLEAN NOT NULL DEFAULT TRUE,     
    PRIMARY KEY (bank_id, loan_id, party_id),
    FOREIGN KEY (bank_id, loan_id) REFERENCES Loan(bank_id, loan_id) ON DELETE CASCADE,
    FOREIGN KEY (bank_id, party_id) REFERENCES Party(bank_id, party_id) ON DELETE CASCADE,
    FOREIGN KEY (borrower_role) REFERENCES BorrowerRole(role_name)
);
