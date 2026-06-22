## Fact: fact_transactions (20,000 rows)
Column	Type	Description	Constraint
transaction_id	STRING	Unique transaction id (UUID)	PK, unique
date_key	INT	FK → dim_date	Not null, valid ref
customer_key	INT	FK → dim_customer	Not null, valid ref
account_key	INT	FK → dim_account	Not null, valid ref
branch_key	INT	FK → dim_branch	Not null, valid ref
product_key	INT	FK → dim_product	Not null, valid ref
transaction_type_key	INT	FK → dim_transaction_type	Not null, valid ref
currency_key	INT	FK → dim_currency	Not null, valid ref
amount	DECIMAL(12,2)	Transaction amount (~Normal dist.)	> 0
fee	DECIMAL(8,2)	Fee charged (~Normal dist.)	≥ 0
balance_after	DECIMAL(14,2)	Account balance post‑txn	—
is_flagged	BOOLEAN	Anomaly flag (amount outlier)	—
created_ts	TIMESTAMP	Event timestamp	Not null

## Dimensions
dim_date (~730 rows) — date_key INT PK, full_date DATE, day, month, month_name, quarter, year, day_of_week, is_weekend BOOLEAN.

dim_customer (2,000) — customer_key INT PK, customer_id, first_name, last_name, email, segment (Retail/Premier/Private), credit_score INT (~Normal μ=680 σ=60), join_date, country.

dim_account (3,000) — account_key INT PK, account_id, customer_key INT FK, account_type (Checking/Savings/Credit), open_date, status (Active/Dormant/Closed).

dim_branch (50) — branch_key INT PK, branch_id, branch_name, city, region, manager.

dim_product (8) — product_key INT PK, product_name, category (Deposit/Loan/Card/Investment), risk_level.

dim_transaction_type (6) — transaction_type_key INT PK, type_name (Deposit/Withdrawal/Transfer/Payment/Fee/Refund), direction (Credit/Debit).

dim_currency (5) — currency_key INT PK, currency_code (USD/EUR/GBP/SGD/PHP), currency_name, usd_rate.