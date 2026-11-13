# SupeRR Selector 2: The 'Moneyball' Dashboard 🏏

This dashboard presents a data-driven "Differential" draft strategy for SupeRR Selector Season 2. It is designed to find asymmetric value by identifying hidden gems and clutch performers who drastically outperform their baselines under extreme pressure.

## Features
- **Differential Batters:** Ranks players based on their strike rate differential under extreme pressure, penalized for match-to-match variance.
- **Differential Bowlers:** Ranks bowlers based on their economy rate differential under extreme pressure, penalized for match-to-match variance.
- **Interactive Visualizations:** Dark-themed Plotly charts for easy analysis.

## Setup Instructions (Local)
1. Ensure you have Python installed.
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```

## Files in this Directory
- `app.py`: The main Streamlit dashboard application.
- `requirements.txt`: Python package dependencies.
- `README.md`: This file.
