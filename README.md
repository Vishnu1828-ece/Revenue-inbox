A deterministic, rule-based sales manager dashboard built with Python and Streamlit to review call activity, automate conversation routing, handle duplicate imports (UPSERT logic), and manage manual overrides without relying on AI APIs.

## Features
- **Executive Dashboard Metrics:** Real-time totals for pipeline value, talk ratios, and risk flags.
- **Rule-Based Routing Engine:** Automatically categorizes calls (e.g., Pricing Pushback, Competitor Threats) using keyword matching and regex.
- **Deduplication & Updates:** Supports CSV imports that update existing records via unique call IDs.
- **Organized Exports:** Exports clean CSV data alongside a structured `manifest.json`.

## How to Run Locally
1. Clone or download this repository.
2. Install dependencies: `pip install -r requirements.txt`
3. Run the app: `streamlit run app.py`
