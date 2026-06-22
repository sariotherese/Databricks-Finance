from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from faker import Faker


SEED = 42
FACT_ROWS = 20_000


def clipped_normal(
    rng: np.random.Generator,
    mean: float,
    std_dev: float,
    size: int,
    min_value: float,
    max_value: float,
) -> np.ndarray:
    values = rng.normal(loc=mean, scale=std_dev, size=size)
    return np.clip(values, min_value, max_value)


def build_dim_date() -> pd.DataFrame:
    dates = pd.date_range(start="2025-01-01", end="2026-12-31", freq="D")
    df = pd.DataFrame({"full_date": dates})
    df.insert(0, "date_key", np.arange(1, len(df) + 1, dtype=np.int32))
    df["day"] = df["full_date"].dt.day
    df["month"] = df["full_date"].dt.month
    df["month_name"] = df["full_date"].dt.month_name()
    df["quarter"] = df["full_date"].dt.quarter
    df["year"] = df["full_date"].dt.year
    df["day_of_week"] = df["full_date"].dt.day_name()
    df["is_weekend"] = df["full_date"].dt.dayofweek >= 5
    return df


def build_dim_customer(fake: Faker, rng: np.random.Generator, count: int = 1_500) -> pd.DataFrame:
    first_names = [fake.first_name() for _ in range(count)]
    last_names = [fake.last_name() for _ in range(count)]
    cities = [fake.city() for _ in range(count)]
    emails = [f"{f.lower()}.{l.lower()}{i + 1}@examplebank.com" for i, (f, l) in enumerate(zip(first_names, last_names))]

    df = pd.DataFrame(
        {
            "customer_key": np.arange(1, count + 1, dtype=np.int32),
            "first_name": first_names,
            "last_name": last_names,
            "email": emails,
            "city": cities,
            "segment": rng.choice(["Mass", "Affluent", "Private"], size=count, p=[0.65, 0.3, 0.05]),
            "join_date": pd.to_datetime(rng.choice(pd.date_range("2018-01-01", "2026-06-30"), size=count)),
        }
    )
    return df


def build_dim_branch(fake: Faker, count: int = 120) -> pd.DataFrame:
    branch_names = [f"{fake.city()} Branch" for _ in range(count)]
    branch_cities = [fake.city() for _ in range(count)]
    return pd.DataFrame(
        {
            "branch_key": np.arange(1, count + 1, dtype=np.int32),
            "branch_name": branch_names,
            "city": branch_cities,
            "region": np.random.choice(["North", "South", "East", "West", "Central"], size=count),
        }
    )


def build_dim_product() -> pd.DataFrame:
    products = [
        ("CHK_STD", "Checking Standard", "Checking"),
        ("CHK_PRM", "Checking Premium", "Checking"),
        ("SVG_STD", "Savings Standard", "Savings"),
        ("SVG_HY", "Savings High Yield", "Savings"),
        ("CRD_CL", "Credit Card Classic", "Cards"),
        ("CRD_PL", "Credit Card Platinum", "Cards"),
        ("LN_PER", "Personal Loan", "Lending"),
        ("LN_AUTO", "Auto Loan", "Lending"),
        ("MRT_FIX", "Mortgage Fixed", "Mortgage"),
        ("MRT_VAR", "Mortgage Variable", "Mortgage"),
    ]
    df = pd.DataFrame(products, columns=["product_code", "product_name", "product_category"])
    df.insert(0, "product_key", np.arange(1, len(df) + 1, dtype=np.int32))
    return df


def build_dim_transaction_type() -> pd.DataFrame:
    tx_types = [
        "Deposit",
        "Withdrawal",
        "Card Purchase",
        "Card Refund",
        "Transfer In",
        "Transfer Out",
        "Loan Payment",
        "Fee",
    ]
    df = pd.DataFrame({"transaction_type": tx_types})
    df.insert(0, "transaction_type_key", np.arange(1, len(df) + 1, dtype=np.int32))
    return df


def build_dim_currency() -> pd.DataFrame:
    currencies = [
        ("USD", "US Dollar"),
        ("EUR", "Euro"),
        ("GBP", "British Pound"),
        ("CAD", "Canadian Dollar"),
        ("AUD", "Australian Dollar"),
        ("JPY", "Japanese Yen"),
    ]
    df = pd.DataFrame(currencies, columns=["currency_code", "currency_name"])
    df.insert(0, "currency_key", np.arange(1, len(df) + 1, dtype=np.int32))
    return df


def build_dim_account(
    rng: np.random.Generator,
    customer_count: int,
    product_count: int,
    branch_count: int,
    currency_count: int,
    count: int = 3_000,
) -> pd.DataFrame:
    opened_dates = pd.to_datetime(rng.choice(pd.date_range("2019-01-01", "2026-12-31"), size=count))
    account_numbers = [f"AC{10000000 + i}" for i in range(count)]

    return pd.DataFrame(
        {
            "account_key": np.arange(1, count + 1, dtype=np.int32),
            "account_number": account_numbers,
            "customer_key": rng.integers(1, customer_count + 1, size=count),
            "product_key": rng.integers(1, product_count + 1, size=count),
            "branch_key": rng.integers(1, branch_count + 1, size=count),
            "currency_key": rng.integers(1, currency_count + 1, size=count),
            "opened_date": opened_dates,
            "status": rng.choice(["Active", "Dormant", "Closed"], size=count, p=[0.86, 0.1, 0.04]),
        }
    )


def build_fact_transactions(
    rng: np.random.Generator,
    dim_sizes: dict[str, int],
    count: int = FACT_ROWS,
) -> pd.DataFrame:
    amount = clipped_normal(rng, mean=250.0, std_dev=120.0, size=count, min_value=1.0, max_value=20_000.0)
    fee = clipped_normal(rng, mean=3.5, std_dev=1.2, size=count, min_value=0.01, max_value=250.0)
    credit_score = clipped_normal(rng, mean=680.0, std_dev=90.0, size=count, min_value=300.0, max_value=850.0)

    fact = pd.DataFrame(
        {
            "transaction_id": np.arange(1, count + 1, dtype=np.int64),
            "date_key": rng.integers(1, dim_sizes["date"] + 1, size=count),
            "customer_key": rng.integers(1, dim_sizes["customer"] + 1, size=count),
            "account_key": rng.integers(1, dim_sizes["account"] + 1, size=count),
            "branch_key": rng.integers(1, dim_sizes["branch"] + 1, size=count),
            "product_key": rng.integers(1, dim_sizes["product"] + 1, size=count),
            "transaction_type_key": rng.integers(1, dim_sizes["transaction_type"] + 1, size=count),
            "currency_key": rng.integers(1, dim_sizes["currency"] + 1, size=count),
            "amount": np.round(amount, 2),
            "fee": np.round(fee, 2),
            "credit_score": np.round(credit_score).astype(np.int32),
        }
    )
    return fact


def main() -> None:
    rng = np.random.default_rng(SEED)
    np.random.seed(SEED)
    Faker.seed(SEED)
    fake = Faker()
    fake.seed_instance(SEED)

    dim_date = build_dim_date()
    dim_customer = build_dim_customer(fake, rng)
    dim_branch = build_dim_branch(fake)
    dim_product = build_dim_product()
    dim_transaction_type = build_dim_transaction_type()
    dim_currency = build_dim_currency()
    dim_account = build_dim_account(
        rng=rng,
        customer_count=len(dim_customer),
        product_count=len(dim_product),
        branch_count=len(dim_branch),
        currency_count=len(dim_currency),
    )

    fact_transactions = build_fact_transactions(
        rng,
        dim_sizes={
            "date": len(dim_date),
            "customer": len(dim_customer),
            "account": len(dim_account),
            "branch": len(dim_branch),
            "product": len(dim_product),
            "transaction_type": len(dim_transaction_type),
            "currency": len(dim_currency),
        },
        count=FACT_ROWS,
    )

    project_root = Path(__file__).resolve().parents[2]
    output_dir = project_root / "data"
    output_dir.mkdir(parents=True, exist_ok=True)

    tables = {
        "dim_date": dim_date,
        "dim_customer": dim_customer,
        "dim_account": dim_account,
        "dim_branch": dim_branch,
        "dim_product": dim_product,
        "dim_transaction_type": dim_transaction_type,
        "dim_currency": dim_currency,
        "fact_transactions": fact_transactions,
    }

    for table_name, table_df in tables.items():
        table_df.to_csv(output_dir / f"{table_name}.csv", index=False)

    print(f"Generated {len(tables)} tables in: {output_dir}")
    print(f"fact_transactions rows: {len(fact_transactions)}")


if __name__ == "__main__":
    main()