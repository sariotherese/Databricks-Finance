# Copilot prompt:
# Generate a synthetic retail-banking dataset for a Databricks star schema.
# Requirements:
#   - 7 dimension tables: dim_date, dim_customer, dim_account, dim_branch,
#     dim_product, dim_transaction_type, dim_currency
#   - 1 fact table: fact_transactions with exactly 20,000 rows
#   - Surrogate integer keys (1..N) as primary keys in every dimension
#   - Enforce referential integrity: every FK in fact_transactions must be
#     sampled ONLY from existing dimension surrogate keys
#   - Numeric measures (amount, fee, credit_score) follow a NORMAL distribution
#     using numpy.random.normal, clipped to valid positive ranges
#   - Use Faker for names/emails/cities; seed everything for reproducibility
#   - Write each table to data/<table>.csv