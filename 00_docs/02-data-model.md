## Data model (Star Schema)

1 fact table + 7 dimension tables. All foreign keys in the fact table resolve to a valid surrogate key in a dimension (referential integrity enforced at generation time and re‑checked via DLT expectations).

                         ┌──────────────┐
                         │  dim_date    │
                         └──────┬───────┘
   ┌────────────┐               │              ┌──────────────────┐
   │dim_customer│──┐            │           ┌──│ dim_transaction  │
   └────────────┘  │            │           │  │     _type        │
   ┌────────────┐  │     ┌──────┴───────┐   │  └──────────────────┘
   │dim_account │──┼────►│    FACT      │◄──┤
   └────────────┘  │     │ transactions │   │  ┌──────────────────┐
   ┌────────────┐  │     └──────┬───────┘   └──│  dim_currency    │
   │ dim_branch │──┘            │              └──────────────────┘
   └────────────┘               │
                         ┌───────┴──────┐
                         │ dim_product  │
                         └──────────────┘

Foreign keys in fact_transactions: date_key, customer_key, account_key, branch_key, product_key, transaction_type_key, currency_key.