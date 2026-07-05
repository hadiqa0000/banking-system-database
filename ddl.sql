
CREATE TABLE Bank (
    bank_id BIGINT GENERATED ALWAYS AS IDENTITY,
    legal_name VARCHAR(100) NOT NULL UNIQUE,
    bic VARCHAR(11) NOT NULL UNIQUE CHECK (LENGTH(bic) IN (8, 11)),
    routing_no VARCHAR(9) NULL CHECK (LENGTH(routing_no) = 9),
    country_code CHAR(2) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) NOT NULL CHECK (status IN ('active', 'suspended', 'closed')),
    headquarters_city VARCHAR(100) NOT NULL,
    headquarters_address VARCHAR(255) NOT NULL,
    license_number VARCHAR(50) NOT NULL,
    PRIMARY KEY (bank_id)
);

CREATE TABLE Branch (
    bank_id BIGINT NOT NULL,
    branch_id BIGINT GENERATED ALWAYS AS IDENTITY,
    name VARCHAR(100) NOT NULL,
    region VARCHAR(50) NOT NULL,
    branch_addres VARCHAR(50) NOT NULL,
    country_code CHAR(2) NOT NULL,
    PRIMARY KEY (bank_id, branch_id), 
    FOREIGN KEY (bank_id) REFERENCES Bank(bank_id) ON DELETE CASCADE, 
    CONSTRAINT uniq_bank_branch_name UNIQUE (bank_id, name)
);

CREATE TABLE Role (
    bank_id BIGINT NOT NULL,
    role_id BIGINT NOT NULL,
    role_name VARCHAR(50) NOT NULL,
    PRIMARY KEY (bank_id, role_id),
    FOREIGN KEY (bank_id) REFERENCES Bank(bank_id) ON DELETE CASCADE,
    CONSTRAINT uniq_bank_role_name UNIQUE (bank_id, role_name)
);

CREATE TABLE Employee (
    bank_id BIGINT NOT NULL,
    employee_id BIGINT GENERATED ALWAYS AS IDENTITY,
    branch_id BIGINT NOT NULL,
    role_id BIGINT NOT NULL,
    salary DECIMAL(12, 2) NOT NULL CHECK (salary >= 0),
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    PRIMARY KEY (bank_id, employee_id), 
    FOREIGN KEY (bank_id, branch_id) REFERENCES Branch(bank_id, branch_id), 
    FOREIGN KEY (bank_id, role_id) REFERENCES Role(bank_id, role_id)
);

CREATE TABLE Party (
    bank_id BIGINT NOT NULL,
    party_id BIGINT NOT NULL,
    type VARCHAR(15) NOT NULL CHECK (type IN ('individual', 'organization')),
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
    gender VARCHAR(7) NOT NULL CHECK (gender IN ('male', 'female', 'intersex')),
    SSN VARCHAR(9) NULL,
    nationality VARCHAR(65) NOT NULL,
    registeration_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    occupation VARCHAR(10) NULL,
    martial_status VARCHAR(15) NOT NULL CHECK (martial_status IN ('married', 'not married', 'divorced', 'widowed', 'seperated')),
    disability BOOLEAN NOT NULL DEFAULT FALSE,
    disability_type VARCHAR(100) NULL,
    disability_disc VARCHAR(150) NULL,
    annual_income BIGINT NOT NULL,
    employment_status VARCHAR(100) NOT NULL CHECK (employment_status IN ('employed', 'unemployed')),
    country_of_residence VARCHAR(15) NOT NULL,
    city_of_residence VARCHAR(15) NOT NULL,
    district_of_residence VARCHAR(15) NOT NULL,
    customer_status VARCHAR(10) NOT NULL CHECK (customer_status IN ('Active', 'inactive', 'blacklisted')),
    deceased_flag BOOLEAN NOT NULL DEFAULT FALSE,
    PRIMARY KEY (bank_id, party_id),
    FOREIGN KEY (bank_id, party_id) REFERENCES Party(bank_id, party_id) ON DELETE CASCADE,
    CONSTRAINT uniq_bank_national_id UNIQUE (bank_id, national_id)
);

CREATE TABLE Organization (
    bank_id BIGINT NOT NULL,
    party_id BIGINT NOT NULL,
    legal_name VARCHAR(200) NOT NULL,
    trading_name VARCHAR(200) NULL,
    registration_number VARCHAR(50) NOT NULL,
    tax_id VARCHAR(50) NOT NULL,
    organization_type VARCHAR(30) NOT NULL CHECK (organization_type IN ('sole proprietorship','partnership', 'private limited','public limited','government','non-profit','bank','corporation')), 
    industry VARCHAR(100) NULL,
    incorporation_date DATE NOT NULL,

    email VARCHAR(255) NULL,

    phone_number VARCHAR(30) NULL,

    website VARCHAR(255) NULL,

    annual_revenue DECIMAL(18,2) NULL,

    employee_count INT NULL
        CHECK (employee_count >= 0),

    PRIMARY KEY (bank_id, party_id),

    FOREIGN KEY (bank_id, party_id)
        REFERENCES Party(bank_id, party_id)
        ON DELETE CASCADE,

    CONSTRAINT uniq_bank_registration
        UNIQUE(bank_id, registration_number),

    CONSTRAINT uniq_bank_tax_id
        UNIQUE(bank_id, tax_id)

);

CREATE TABLE Account (
    bank_id BIGINT NOT NULL,
    account_id BIGINT NOT NULL,
    branch_id BIGINT NOT NULL,
    account_number VARCHAR(34) NOT NULL,
    status VARCHAR(15) NOT NULL DEFAULT 'active' CHECK (status IN ('active', 'blacklisted', 'frozen', 'closed')),
    account_type VARCHAR(15) NOT NULL CHECK (account_type IN ('checking', 'savings', 'business', 'student', 'money market')),
    opened_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    currency_code CHAR(3) NOT NULL,
    closed_at TIMESTAMP NULL,
    last_activity_at TIMESTAMP NULL,
    overdraft_limit DECIMAL(18, 2) DEFAULT 0,
    interest_rate DECIMAL(5, 2) NULL,
    minimum_balance DECIMAL(18, 2) NULL,
    PRIMARY KEY (bank_id, account_id),
    FOREIGN KEY (bank_id, branch_id) REFERENCES Branch(bank_id, branch_id),
    CONSTRAINT uniq_bank_account_number UNIQUE (bank_id, account_number)
);

CREATE TABLE Account_ownership (
    bank_id BIGINT NOT NULL,
    account_id BIGINT NOT NULL,
    party_id BIGINT NOT NULL,
    role VARCHAR(15) NOT NULL DEFAULT 'primary' CHECK (role IN ('primary', 'joint', 'signatory')),
    ownershipt_pct DECIMAL(5, 2) NOT NULL DEFAULT 100.00,
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
    journal_id BIGINT NOT NULL,
    timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    reference_type VARCHAR(20) NOT NULL,
    reference_id BIGINT NOT NULL,
    description VARCHAR(255) NOT NULL,
    posting_status VARCHAR(15) NOT NULL CHECK (posting_status IN ('draft', 'posted', 'reversed')),
    posted_at TIMESTAMP NULL,
    posted_by_employee_id BIGINT NOT NULL,
    source_system VARCHAR(30) NOT NULL,
    reversal_of_journal_id BIGINT NULL,
    batch_id BIGINT NULL,
    currency_code CHAR(3) NULL,
    PRIMARY KEY (bank_id, journal_id),
    FOREIGN KEY (bank_id) REFERENCES Bank(bank_id) ON DELETE CASCADE
);

CREATE TABLE JournalLine (
    bank_id BIGINT NOT NULL,
    journal_id BIGINT NOT NULL,
    line_id BIGINT NOT NULL,
    account_id BIGINT NOT NULL,
    debit DECIMAL(15, 2) NOT NULL DEFAULT 0.00,
    credit DECIMAL(15, 2) NOT NULL DEFAULT 0.00,
    description VARCHAR(255) NULL,
    line_number BIGINT NOT NULL,
    currency_code CHAR(3) NOT NULL,
    exchange_rate DECIMAL(18, 8) NULL,
    PRIMARY KEY (bank_id, journal_id, line_id),
    FOREIGN KEY (bank_id, journal_id) REFERENCES JournalEntry(bank_id, journal_id) ON DELETE CASCADE,
    FOREIGN KEY (bank_id, account_id) REFERENCES Account(bank_id, account_id),
    CONSTRAINT CHK_DEBIT CHECK (debit >= 0),
    CONSTRAINT CHK_CREDIT CHECK (credit >= 0),
    CONSTRAINT CHK_DEBIT_AND_CREDIT CHECK ((debit > 0 AND credit = 0) OR (credit > 0 AND debit = 0))
);

CREATE TABLE LoanApplication (
    bank_id BIGINT NOT NULL,
    application_id BIGINT NOT NULL,
    applicant_party_id BIGINT NOT NULL,
    requested_amount DECIMAL(15, 2) NOT NULL,
    loan_application_status VARCHAR(15) NOT NULL DEFAULT 'pending' CHECK (loan_application_status IN ('pending', 'approved', 'rejected')),
    application_sent_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    loan_type VARCHAR(30) NOT NULL CHECK (loan_type IN ('personal loan', 'mortgage loan', 'auto loan', 'student loan', 'business loan', 'credit card loan', 'Term Loan', 'working capital loan', 'business_line_of_credit', 'equipment_financing_loan')),
    requested_term_months SMALLINT NOT NULL CHECK (requested_term_months <= 250),
    purpose_of_loan VARCHAR(250) NOT NULL,
    requested_interest_rate DECIMAL(5, 2) NULL CHECK (requested_interest_rate > 0),
    assigned_employee_id BIGINT NOT NULL,
    decision_at TIMESTAMP NULL,
    rejection_reason VARCHAR(15) NULL,
    approved_amount DECIMAL(15, 2) NULL,
    approved_term_month SMALLINT NULL CHECK (approved_term_month <= 250),
    approved_interest_rate DECIMAL(5, 2) NULL,
    PRIMARY KEY (bank_id, application_id),
    FOREIGN KEY (bank_id, applicant_party_id) REFERENCES Party(bank_id, party_id)
);

CREATE TABLE CreditAssessment (
    bank_id BIGINT NOT NULL,
    assessment_id BIGINT NOT NULL,
    application_id BIGINT NOT NULL,
    employee_id BIGINT NOT NULL,
    score INT NOT NULL,
    risk_level VARCHAR(10) NOT NULL CHECK (risk_level IN ('low', 'medium', 'high')),
    assessment_method VARCHAR(15) NOT NULL CHECK (assessment_method IN ('manual', 'automated', 'hybrid')),
    recommendation VARCHAR(15) NOT NULL CHECK (recommendation IN ('approve', 'reject', 'manual_review')),
    assessment_version VARCHAR(20) NOT NULL,
    debt_to_income_ratio DECIMAL(5, 2) NULL CHECK (debt_to_income_ratio IS NULL OR debt_to_income_ratio >= 0),
    annual_income_snapshot DECIMAL(15, 2) NULL CHECK (annual_income_snapshot IS NULL OR annual_income_snapshot >= 0),
    monthly_expenses_snapshot DECIMAL(15, 2) NULL CHECK (monthly_expenses_snapshot IS NULL OR monthly_expenses_snapshot >= 0),
    comments TEXT NULL,
    assessed_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP NULL,
    PRIMARY KEY (bank_id, assessment_id),
    FOREIGN KEY (bank_id, application_id) REFERENCES LoanApplication(bank_id, application_id),
    FOREIGN KEY (bank_id, employee_id) REFERENCES Employee(bank_id, employee_id)
);

CREATE TABLE Loan (
    bank_id BIGINT NOT NULL,
    loan_id BIGINT NOT NULL,
    application_id BIGINT NOT NULL,
    principal DECIMAL(15, 2) NOT NULL,
    interest_rate DECIMAL(5, 4) NOT NULL,
    disbursed_at TIMESTAMP NULL,
    loan_status VARCHAR(15) NOT NULL DEFAULT 'active' CHECK (loan_status IN ('active', 'performing', 'delinquent', 'Defaulted', 'Charged-Off', 'Closed')),
    maturity_date DATE NOT NULL,
    next_payment_due_date DATE NOT NULL,
    payment_frequency VARCHAR(20) NOT NULL DEFAULT 'monthly' CHECK (payment_frequency IN ('monthly', 'weekly', 'bi-weekly', 'quarterly', 'semi-annual', 'annual')),
    installment_amount DECIMAL(15, 2) NOT NULL,
    currency_code CHAR(3) NOT NULL,
    late_fee_rate DECIMAL(15, 2) NOT NULL,
    grace_period_days SMALLINT NULL DEFAULT 0,
    closed_at DATE NULL,
    closure_reason VARCHAR(40) NULL CHECK (closure_reason IN ('paid in full', 'early closure', 'refinancing', 'one-time settlement', 'default and charge-off', 'sent to collections', 'fraud or policy violation')),
    PRIMARY KEY (bank_id, loan_id),
    FOREIGN KEY (bank_id, application_id) REFERENCES LoanApplication(bank_id, application_id),
    CONSTRAINT uniq_bank_application UNIQUE (bank_id, application_id)
);

CREATE TABLE LoanPayment (
    bank_id BIGINT NOT NULL,
    payment_id BIGINT NOT NULL,
    loan_id BIGINT NOT NULL,
    journal_id BIGINT NOT NULL,
    total_amount_paid DECIMAL(15, 2) NOT NULL,
    principal_component DECIMAL(15, 2) NOT NULL,
    interest_component DECIMAL(15, 2) NOT NULL,
    payment_status VARCHAR(20) NOT NULL DEFAULT 'pending' CHECK (payment_status IN ('pending', 'completed', 'failed', 'reversed')),
    payment_method VARCHAR(20) NOT NULL CHECK (payment_method IN ('cash', 'bank transfer', 'debit account', 'cheque')),
    payment_channel VARCHAR(20) CHECK (payment_channel IN ('branch', 'atm', 'online', 'mobile', 'api')),
    installment_number SMALLINT NOT NULL,
    remaining_balance_after_payment DECIMAL(15, 2) NOT NULL,
    late_fee_component DECIMAL(15, 2) NULL,
    penalty_interest_component DECIMAL(15, 2) NULL,
    payment_reference VARCHAR(50) NULL,
    paid_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (bank_id, payment_id),
    FOREIGN KEY (bank_id, loan_id) REFERENCES Loan(bank_id, loan_id),
    FOREIGN KEY (bank_id, journal_id) REFERENCES JournalEntry(bank_id, journal_id) ON DELETE CASCADE,
    CONSTRAINT uniq_bank_payment_journal UNIQUE (bank_id, journal_id),
    CONSTRAINT uniq_bank_payment_reference UNIQUE (bank_id, payment_reference),
    CONSTRAINT chk_principal_component CHECK (principal_component >= 0),
    CONSTRAINT chk_interest_component CHECK (interest_component >= 0),
    CONSTRAINT chk_late_fee CHECK (late_fee_component IS NULL OR late_fee_component >= 0),
    CONSTRAINT chk_penalty_interest CHECK (penalty_interest_component IS NULL OR penalty_interest_component >= 0),
    CONSTRAINT chk_remaining_balance CHECK (remaining_balance_after_payment >= 0),
    CONSTRAINT chk_installment_number CHECK (installment_number > 0),
    CONSTRAINT chk_total_amount CHECK (
        total_amount_paid = principal_component + interest_component + COALESCE(late_fee_component, 0) + COALESCE(penalty_interest_component, 0)
    )
);

CREATE TABLE CardProduct (
    bank_id BIGINT NOT NULL,
    card_product_id BIGINT NOT NULL,
    product_name VARCHAR(100) NOT NULL,
    card_type VARCHAR(15) NOT NULL CHECK (card_type IN ('debit', 'credit', 'prepaid', 'charge')),
    card_segment VARCHAR(20) NOT NULL CHECK (card_segment IN ('consumer', 'business', 'corporate', 'private_banking')),
    card_network VARCHAR(20) CHECK (card_network IN ('visa', 'mastercard', 'amex', 'unionpay', 'discover')),
    supports_contactless BOOLEAN NOT NULL DEFAULT TRUE,
    daily_atm_withdrawal_limit DECIMAL(15, 2) NULL DEFAULT 0 CHECK (daily_atm_withdrawal_limit >= 0),
    daily_purchase_limit DECIMAL(15, 2) NOT NULL,
    min_age SMALLINT NOT NULL CHECK (min_age >= 0),
    min_cred_score SMALLINT NULL CHECK (min_cred_score IS NULL OR min_cred_score BETWEEN 300 AND 850),
    annual_fee DECIMAL(15, 2) NOT NULL DEFAULT 0.00,
    PRIMARY KEY (bank_id, card_product_id)
);

CREATE TABLE Card (
    bank_id BIGINT NOT NULL,
    card_id BIGINT NOT NULL,
    card_product_id BIGINT NOT NULL,
    account_id BIGINT NOT NULL,
    card_number VARCHAR(19) NOT NULL,
    expiry_date DATE NOT NULL,
    status VARCHAR(20) NOT NULL CHECK (status IN ('pending_activation', 'active', 'frozen', 'blocked', 'expired', 'cancelled', 'stolen', 'lost')),
    issued_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    activated_at TIMESTAMP NULL,
    cardholder_name VARCHAR(100) NOT NULL,
    last_used_at TIMESTAMP NULL,
    pin_retry_count SMALLINT DEFAULT 0 CHECK (pin_retry_count BETWEEN 0 AND 3),
    pin_last_changed_at TIMESTAMP NULL,               
    replacement_reason VARCHAR(20) CHECK (replacement_reason IN ('expired', 'lost', 'stolen', 'damaged')),
    PRIMARY KEY (bank_id, card_id),
    FOREIGN KEY (bank_id, account_id) REFERENCES Account(bank_id, account_id) ON DELETE CASCADE,
    FOREIGN KEY (bank_id, card_product_id) REFERENCES CardProduct(bank_id, card_product_id),
    CONSTRAINT uniq_bank_card_number UNIQUE (bank_id, card_number)
);

CREATE TABLE CardApplication (
    bank_id BIGINT NOT NULL,
    account_id BIGINT NOT NULL,
    application_id BIGINT NOT NULL, 
    applicant_party_id BIGINT NOT NULL,
    card_product_id BIGINT NOT NULL, 
    application_status VARCHAR(20) NOT NULL CHECK (application_status IN ('pending', 'approved', 'rejected', 'cancelled')),
    submitted_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    reviewed_at TIMESTAMP NULL,
    reviewed_by_employee_id BIGINT NULL,
    rejection_reason VARCHAR(500) NULL,
    approved_card_id BIGINT NULL,
    PRIMARY KEY (bank_id, application_id),
    FOREIGN KEY (bank_id, applicant_party_id) REFERENCES Party(bank_id, party_id),
    FOREIGN KEY (bank_id, card_product_id) REFERENCES CardProduct(bank_id, card_product_id),
    FOREIGN KEY (bank_id, reviewed_by_employee_id) REFERENCES Employee(bank_id, employee_id),
    FOREIGN KEY (bank_id, approved_card_id) REFERENCES Card(bank_id, card_id),
    FOREIGN KEY (bank_id, account_id) REFERENCES Account(bank_id, account_id)
);

CREATE TABLE ATM (
    bank_id BIGINT NOT NULL,
    atm_id BIGINT NOT NULL,
    branch_id BIGINT NOT NULL,
    terminal_id BIGINT NOT NULL,
    status VARCHAR(15) NOT NULL DEFAULT 'active' CHECK (status IN ('active', 'out_of_service', 'maintenance')),
    location_address VARCHAR(255) NOT NULL,
    installed_at TIMESTAMP NOT NULL,
    last_maintenance_at TIMESTAMP NOT NULL,
    next_maintenance_due DATE NOT NULL,
    cash_capacity DECIMAL(15, 2) NOT NULL CHECK (cash_capacity >= 0),
    current_cash_balance DECIMAL(15, 2) NOT NULL CHECK (current_cash_balance >= 0),
    supports_cash_deposit BOOLEAN NOT NULL DEFAULT FALSE,
    supports_contactless BOOLEAN NOT NULL DEFAULT FALSE,
    supports_cardless BOOLEAN NOT NULL DEFAULT FALSE,
    supports_statement_printing BOOLEAN NOT NULL DEFAULT TRUE,
    supports_cash_recycling BOOLEAN NOT NULL DEFAULT FALSE,
    PRIMARY KEY (bank_id, atm_id),
    FOREIGN KEY (bank_id, branch_id) REFERENCES Branch(bank_id, branch_id),
    CONSTRAINT uniq_bank_terminal UNIQUE (bank_id, terminal_id)
);

CREATE TABLE ATMTransaction (
    bank_id BIGINT NOT NULL,
    account_id BIGINT NOT NULL,
    transaction_id BIGINT NOT NULL,
    atm_id BIGINT NOT NULL,
    card_id BIGINT NOT NULL,
    journal_id BIGINT DEFAULT NULL,
    transaction_type VARCHAR(15) NOT NULL CHECK (transaction_type IN ('withdrawal', 'deposit', 'transfer', 'inquiry')),
    amount DECIMAL(15, 2) NOT NULL DEFAULT 0.00,
    response_code VARCHAR(4) NOT NULL DEFAULT '00',
    transaction_status VARCHAR(20) NOT NULL DEFAULT 'completed' CHECK (transaction_status IN ('pending', 'completed', 'failed', 'reversed', 'cancelled')),
    executed_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    destination_acc_id BIGINT NULL, 
    currency_code CHAR(3) NOT NULL,
    balance_after_transaction DECIMAL(15, 2) NULL,
    fee_amount DECIMAL(15, 2) NOT NULL DEFAULT 0,
    employee_id BIGINT NULL,
    receipt_printed BOOLEAN NOT NULL DEFAULT FALSE,
    authorization_status VARCHAR(15) CHECK (authorization_status IN ('approved', 'declined', 'timeout')),
    PRIMARY KEY (bank_id, transaction_id),
    FOREIGN KEY (bank_id, atm_id) REFERENCES ATM(bank_id, atm_id),
    FOREIGN KEY (bank_id, card_id) REFERENCES Card(bank_id, card_id) ON DELETE CASCADE,
    FOREIGN KEY (bank_id, account_id) REFERENCES Account(bank_id, account_id),
    FOREIGN KEY (bank_id, journal_id) REFERENCES JournalEntry(bank_id, journal_id) ON DELETE SET NULL,
    CONSTRAINT uniq_bank_atm_tx_journal UNIQUE (bank_id, journal_id)
);

CREATE TABLE Locker (
    bank_id BIGINT NOT NULL,
    locker_id BIGINT NOT NULL,
    branch_id BIGINT NOT NULL,
    renter_party_id BIGINT DEFAULT NULL,
    locker_number BIGINT NOT NULL,
    size_tier VARCHAR(10) NOT NULL DEFAULT 'small' CHECK (size_tier IN ('small', 'medium', 'large')),
    annual_fee DECIMAL(8, 2) NOT NULL,
    leased_from DATE NULL DEFAULT CURRENT_DATE,
    leased_until DATE DEFAULT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'available' CHECK (status IN ('available', 'leased', 'reserved', 'maintenance', 'retired')),
    security_deposit DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    keys_issued SMALLINT NOT NULL DEFAULT 2 CHECK (keys_issued >= 0),
    last_inspected_at DATE NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    notes VARCHAR(500),
    PRIMARY KEY (bank_id, locker_id),
    FOREIGN KEY (bank_id, branch_id) REFERENCES Branch(bank_id, branch_id),
    FOREIGN KEY (bank_id, renter_party_id) REFERENCES Party(bank_id, party_id) ON DELETE SET NULL,
    CONSTRAINT uniq_branch_locker_num UNIQUE (bank_id, branch_id, locker_number)
);


CREATE TABLE AuditLog (
    bank_id BIGINT NOT NULL,
    branch_id BIGINT NULL,
    audit_id BIGSERIAL, 
    actor_type VARCHAR(20) NOT NULL CHECK (actor_type IN ('employee', 'system', 'api', 'scheduler')),
    source VARCHAR(20) CHECK (source IN ('branch', 'atm', 'online', 'mobile', 'api', 'system')),
    actor_employee_id BIGINT DEFAULT NULL,
    action VARCHAR(10) NOT NULL CHECK (action IN ('INSERT', 'UPDATE', 'DELETE', 'LOGIN', 'LOGOUT', 'APPROVE', 'REJECT')),
    entity_type VARCHAR(30) NOT NULL CHECK (entity_type IN ('Account', 'Loan', 'Card', 'Customer', 'Branch', 'Employee', 'Transaction', 'ATM')),
    entity_id BIGINT NOT NULL,
    logged_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    before_state JSONB DEFAULT NULL, 
    after_state JSONB DEFAULT NULL,  
    error_message VARCHAR(500) NULL,
    session_id UUID NULL,
    reason VARCHAR(255) NULL,
    success BOOLEAN NOT NULL DEFAULT TRUE,
    PRIMARY KEY (bank_id, audit_id),
    FOREIGN KEY (bank_id) REFERENCES Bank(bank_id) ON DELETE CASCADE,
    FOREIGN KEY (bank_id, actor_employee_id) REFERENCES Employee(bank_id, employee_id) ON DELETE SET NULL,
    FOREIGN KEY (bank_id, branch_id) REFERENCES Branch(bank_id, branch_id)
);


CREATE INDEX idx_journal_timestamp ON JournalEntry (bank_id, timestamp);
CREATE INDEX idx_loan_app_status ON LoanApplication (bank_id, loan_application_status);
CREATE INDEX idx_account_opened ON Account (bank_id, opened_at);

CREATE INDEX idx_audit_timestamp ON AuditLog (bank_id, logged_at);
CREATE INDEX idx_audit_entity ON AuditLog (bank_id, entity_type, entity_id);
CREATE INDEX idx_audit_employee ON AuditLog (bank_id, actor_employee_id);
CREATE INDEX idx_audit_branch ON AuditLog (bank_id, branch_id);
