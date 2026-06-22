## Business Case

Scenario: FinFlow Bank wants a governed, near‑real‑time analytics platform on the Databricks Lakehouse. Raw transaction files land continuously from core‑banking systems. The bank needs to:

Ingest raw transactions reliably (schema drift, late files).
Cleanse and validate data (drop corrupt rows, enforce business rules).
Model data into a star schema for BI tools (Power BI / Databricks SQL).
Produce gold aggregates: daily revenue per branch, product profitability, customer spend behavior, and anomaly flags.