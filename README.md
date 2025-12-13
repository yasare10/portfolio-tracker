# portfolio-tracker
Read-only portfolio tracker for Sorare accounts, calculating purchases, sales, trades, rewards, and realised/unrealised P&amp;L.
Portfolio Tracker (Sorare MVP)


**Overview**

This project is a read-only portfolio tracker for Sorare accounts.
It connects to a Sorare user account via official APIs to analyse portfolio activity and calculate performance metrics, without making any changes to the account.

The initial MVP focuses exclusively on Sorare, with a design that supports future expansion to additional platforms and asset types.


**Objectives**

The primary goals of the MVP are to:

- Reconstruct the current Sorare portfolio from on-chain and platform data

- Normalise all historical account activity into structured transactions

- Calculate realised and unrealised profit & loss

- Track rewards, deposits, and withdrawals

- Produce clean, auditable outputs suitable for analysis and visualisation


**Features (MVP)**

**The MVP provides:**

- Account ingestion

- Read-only connection to a Sorare account

- Gallery and card ownership tracking

- Transaction tracking

- Purchases (auctions, instant buy)

- Sales

- Trades (with sunk-cost attribution)

- Rewards (cards with zero cost basis)

- Deposits and withdrawals

- Portfolio analytics

- Current holdings

- Cost basis per card

- Realised P&L

- Unrealised P&L (based on latest market value)

- Historical portfolio snapshots


**Non-Goals (Explicitly Out of Scope)**

To keep the MVP focused, the following are not included:

Trade execution or bidding

Account modification

Automated decision-making

Price prediction or modelling

Multi-platform aggregation


**Data Sources**
Sorare GraphQL API
User profile
Gallery ownership
Card lifecycle events
Market transactions
All access is strictly read-only.


**Tech Stack**
Language: Python
API: Sorare GraphQL
Data Processing: Pandas
Persistence (MVP): CSV / SQLite
Configuration: Environment variables
High-Level Architecture
Sorare API
   ↓
Data Ingestion
   ↓
Transaction Normalisation
   ↓
Portfolio State Reconstruction
   ↓
Metrics & P&L Calculations
   ↓
Structured Output (CSV / DataFrame)

**Repository Structure**
portfolio-tracker/
│
├── src/
│   ├── sorare/
│   │   ├── client.py        # GraphQL client and auth
│   │   ├── queries.py       # Sorare GraphQL queries
│   │   └── normaliser.py    # Convert API data to transactions
│   │
│   ├── portfolio/
│   │   ├── models.py        # Card, Player, Transaction models
│   │   ├── calculations.py # P&L and cost basis logic
│   │   └── metrics.py
│   │
│   └── main.py
│
├── tests/
│
├── .env.example
├── requirements.txt
├── README.md
└── LICENSE

**Installation**
git clone https://github.com/your-username/portfolio-tracker.git
cd portfolio-tracker
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

**Configuration**
Create a .env file using the example provided:
SORARE_API_KEY=your_api_key_here
SORARE_USER_SLUG=your_username

API keys are never committed to the repository.

**Usage**
**Run the MVP pipeline:**
python src/main.py


**Expected outputs include:**
Normalised transaction history
Current portfolio holdings
Realised and unrealised P&L summaries

**Roadmap**
**Planned future improvements:**

- Historical market price snapshots
- Web-based dashboard
- Multi-platform portfolio aggregation
- Tax-oriented reporting
- Automated data refresh

**Contributing**

This project is currently in MVP stage.
Contributions, suggestions, and issues are welcome.

**License**

MIT License
