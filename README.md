# Feature Engineered Transaction Risk Model


## 📌 Overview
This project builds **an audit‑focused transaction risk scoring engine** that ranks origin accounts based on their behavior in a large synthetic financial transactions dataset. The goal is to help internal audit and fraud teams **prioritize which accounts to review first**.

The pipeline:

* Aggregates raw transactions to the **account** level.
* Engineers **audit‑relevant features** such as volume, volatility, transaction‑type mix, and fraud rate.
* Computes an interpretable **risk score** and **high‑risk flag** for each origin account.
* Generates plots and tables to explain why accounts are labeled high risk.

---

📑 Table of Contents
Project Objectives

Project Structure

Data and Features

Risk Scoring Model

Analysis and Visualizations

Tools and Libraries

Possible Extensions

---

## 🎯 Project Objectives
* Transform raw transaction‑level data into account‑level risk indicators for internal audit.
* Design a transparent, explainable scoring model instead of a black‑box classifier.
* Handle large‑scale synthetic financial data using a reproducible Python pipeline.
* Provide notebooks and plots that communicate findings to non‑technical audit stakeholders.

---

📂 Project Structure
text
audit-risk-model/
├── data/
│   ├── raw/
│   │   └── transactions.csv
│   └── processed/
│       ├── origin_account_features.csv
│       └── origin_account_features_scored.csv
├── notebooks/
│   ├── 01_exploration.ipynb
│   └── 02_risk_scoring_model.ipynb
├── src/
│   ├── data_prep.py
│   ├── features.py
│   └── model.py
└── run_pipeline.py

* `data/raw/transactions.csv` – synthetic transaction‑level dataset.
* `data/processed/origin_account_features.csv` – origin‑account features after aggregation.
* `data/processed/origin_account_features_scored.csv` – features plus risk scores and flags.
* `01_exploration.ipynb` – quick EDA of the raw transactions.
* `02_risk_scoring_model.ipynb` – scoring logic, high‑risk flags, plots, and interpretation.
* `src/data_prep.py` – `load_transactions()` with optional sampling.
* `src/features.py` – `build_origin_account_features()` (groupby by origin account).
* `src/model.py` – `add_risk_score()` (scaling + weighted risk score).
* `run_pipeline.py` – orchestrates the full pipeline and prints top high‑risk accounts.

---

📊 Data and Features
The raw dataset simulates mobile money transactions with fields like `step`, `type`, `amount`, `nameOrig`, `nameDest`, balances, and fraud labels.

Key raw fields:

* `step` – simulated time step (hour index).
* `type` – transaction type (PAYMENT, TRANSFER, CASH_OUT, DEBIT, etc.).
* `amount` – transaction amount.
* `nameOrig` – origin account.
* `nameDest` – destination account.
* `oldbalanceOrg`, `newbalanceOrg`, `oldbalanceDest`, `newbalanceDest`.
* `isFraud`, `isFlaggedFraud` – fraud indicators.

Transactions are aggregated by `nameOrig` into origin‑account‑level features:

* `txn_count` – number of transactions.
* `total_amount` – total value sent.
* `avg_amount`, `std_amount`, `max_amount`, `min_amount`.
* `amount_volatility` – `std_amount` / `avg_amount`.
* `payment_ratio` – share of transactions that are PAYMENT.
* `transfer_ratio` – share of transactions that are TRANSFER.
* `cashout_ratio` – share of transactions that are CASH_OUT.
* `debit_ratio` – share of transactions that are DEBIT.
* `fraud_rate` – average of isFraud for the account.

These features are written to `origin_account_features.csv` and reused by both the pipeline and the analysis notebook.

---

## 🧠 Risk Scoring Model
The risk model is deliberately **simple and audit‑friendly**.

### Feature Scaling
Selected features are scaled to [0,1] using `MinMaxScaler`:

* `txn_count`
* `total_amount`
* `amount_volatility`
* `fraud_rate`

### Weighted Composite Score
A linear risk score is computed as a weighted sum:

* 0.2 × scaled `txn_count`
* 0.2 × scaled `total_amount`
* 0.3 × scaled `amount_volatility`
* 0.3 × scaled `fraud_rate`

This emphasizes accounts that:

* Move **a lot of money**,
* Have **volatile transaction patterns**, and
* Show **higher historical fraud rate**.

The resulting `risk_score` is stored in `origin_account_features_scored.csv`.

### High‑Risk Flag
To make the score actionable, the engine defines a **high‑risk flag**:

* Sort accounts by `risk_score` (descending).
* Label the **top 20%** as high risk with a binary `high_risk_flag` column.

This gives audit a clear list of accounts to prioritize for testing.

---

## 🔍 Analysis and Visualizations

`02_risk_scoring_model.ipynb` provides:

* **Summary statistics** of `risk_score`.
* A **histogram**: “Distribution of Audit Risk Scores by Origin Account.”
* Tables showing **example high‑risk accounts vs low‑risk accounts**, including:

* `txn_count`
* `total_amount`
* `amount_volatility`
* `fraud_rate`
* `risk_score`
* `high_risk_flag`

---

## 🛠 Tools and Libraries

* Python
* pandas, NumPy
* scikit‑learn (MinMaxScaler)
* Matplotlib
* Jupyter Notebook / Cursor

---

🚀 Possible Extensions
* Train a supervised model (e.g., logistic regression) to predict `isFraud` or `high_risk_flag`.
* Add **time‑window features** (recent spike in activity vs long‑term behavior).
* Build a **Streamlit or Dash app** for auditors to filter and investigate high‑risk accounts.
* Tune weights in the risk score with domain input from audit or credit risk teams.
