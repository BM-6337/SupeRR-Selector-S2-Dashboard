import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="SupeRR Selector 2 - Differential Picks", layout="wide", page_icon="🏏")
st.markdown('''<style>
.stApp {background-color: #0f172a;}
h1, h2, h3, p, div {color: #f8fafc;}
.metric-card {background: #1e293b; padding: 20px; border-radius: 10px; border: 1px solid #3d4a60; text-align: center; border-top: 4px solid #38bdf8;}
.highlight {color: #38bdf8; font-weight: bold;}
</style>''', unsafe_allow_html=True)

@st.cache_data
def load_data():
    bat_stats = pd.read_csv('bat_stats_2.csv')
    bowl_stats = pd.read_csv('bowl_stats_2.csv')
    return bat_stats.head(50), bowl_stats.head(50)

bat_stats, bowl_stats = load_data()

st.title("🏏 SupeRR Selector: The 'Hidden Gems' Dashboard")
st.markdown("### Powered by the Differential Clutch Model")

pages = ["Overview", "Batters (Differential)", "Bowlers (Differential)", "Methodology"]
selected_page = st.sidebar.radio("Navigation", pages)

if selected_page == "Overview":
    st.header("Draft Strategy: Asymmetric Value")
    col1, col2 = st.columns(2)
    col1.markdown(f"<div class='metric-card'><h3>Top Differential Batter</h3><h2>{bat_stats.iloc[0]['striker_name']}</h2><p>Clutch Rating: {bat_stats.iloc[0]['Pressure_Rating']:.2f}</p></div>", unsafe_allow_html=True)
    col2.markdown(f"<div class='metric-card'><h3>Top Differential Bowler</h3><h2>{bowl_stats.iloc[0]['bowler_name']}</h2><p>Clutch Rating: {bowl_stats.iloc[0]['Pressure_Rating']:.2f}</p></div>", unsafe_allow_html=True)

elif selected_page == "Batters (Differential)":
    st.header("Top Batters (High Pressure Spike + High Consistency)")
    st.dataframe(bat_stats[['striker_name', 'Pressure_Rating', 'sr_base', 'sr_pres', 'sr_std']].head(15).round(2), use_container_width=True)
    fig = px.bar(bat_stats.head(10), x='striker_name', y='Pressure_Rating', title='Clutch Rating - Top 10 Batters', template='plotly_dark', color_discrete_sequence=['#38bdf8'])
    st.plotly_chart(fig, use_container_width=True)

elif selected_page == "Bowlers (Differential)":
    st.header("Top Bowlers (Pressure Lockdown + High Consistency)")
    st.dataframe(bowl_stats[['bowler_name', 'Pressure_Rating', 'econ_base', 'econ_pres', 'econ_std']].head(15).round(2), use_container_width=True)
    fig = px.bar(bowl_stats.head(10), x='bowler_name', y='Pressure_Rating', title='Clutch Rating - Top 10 Bowlers', template='plotly_dark', color_discrete_sequence=['#fb7185'])
    st.plotly_chart(fig, use_container_width=True)

elif selected_page == "Methodology":
    st.header("The 'Wow' Factor Methodology")
    st.markdown('''
    - **Extreme Pressure Only:** 19th/20th overs, RRR > 12, or 4 wickets down in the Powerplay.
    - **The Consistency Penalty:** Averages lie. We mathematically penalize players with high match-to-match variance.
    - **The Clutch Multiplier:** A 1.5x multiplier is applied to the player's *Differential* (their pressure stats minus their base stats). We want players who spike when the heat is on.
    ''')
