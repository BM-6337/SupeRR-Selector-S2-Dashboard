import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- PAGE SETUP ---
st.set_page_config(page_title="SupeRR Selector - The Pressure Index", layout="wide", page_icon="🏏")

st.markdown('''
<style>
    .stApp { background-color: #0d1117; color: #c9d1d9; }
    .premium-title { font-family: 'Helvetica Neue', sans-serif; font-size: 3rem; font-weight: 300; letter-spacing: -1px; color: #f0f6fc; border-left: 6px solid #2f81f7; padding-left: 15px; margin-bottom: 5px; text-transform: uppercase; }
    .premium-subtitle { font-family: 'Helvetica Neue', sans-serif; font-size: 1.2rem; color: #8b949e; margin-bottom: 40px; padding-left: 21px; text-transform: uppercase; letter-spacing: 2px;}
    .metric-card { background: #161b22; border: 1px solid #30363d; padding: 24px; border-radius: 8px; text-align: left; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); }
    .metric-card h3 { color: #8b949e; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 12px; font-weight: 600; }
    .metric-card h1 { color: #f0f6fc; font-size: 2.2rem; font-weight: 700; margin: 0; line-height: 1.2; }
    .metric-card p { color: #2ea043; font-size: 1rem; margin-top: 8px; font-weight: 500; }
</style>
''', unsafe_allow_html=True)

@st.cache_data
def load_data():
    bat_stats = pd.read_csv('DATA/processed data/bat_stats_final.csv')
    bowl_stats = pd.read_csv('DATA/processed data/bowl_stats_final.csv')
    return bat_stats, bowl_stats

bat_stats, bowl_stats = load_data()

st.markdown('<div class="premium-title">SUPERR SELECTOR<br>THE PRESSURE INDEX</div>', unsafe_allow_html=True)
st.markdown('<div class="premium-subtitle">IPL & T20I Cricket Analytics | 2022 onwards</div>', unsafe_allow_html=True)

tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "Executive Overview", "Batting Leaderboard", "Bowling Leaderboard", 
    "Player Profiles", "Player Comparison", "Pressure Situation Analysis", "Methodology"
])

with tab1:
    st.markdown('### Project Diagnostics')
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f'<div class="metric-card"><h3>Unique Batters</h3><h1>{len(bat_stats)}</h1><p>Validated</p></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="metric-card"><h3>Unique Bowlers</h3><h1>{len(bowl_stats)}</h1><p>Validated</p></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="metric-card"><h3>Top Batter</h3><h1>{bat_stats.iloc[0]["striker_name"]}</h1><p>Rating: {bat_stats.iloc[0]["Pressure_Rating"]:.2f}</p></div>', unsafe_allow_html=True)
    with col4:
        st.markdown(f'<div class="metric-card"><h3>Top Bowler</h3><h1>{bowl_stats.iloc[0]["bowler_name"]}</h1><p>Rating: {bowl_stats.iloc[0]["Pressure_Rating"]:.2f}</p></div>', unsafe_allow_html=True)

with tab2:
    st.markdown('### Top 10 Batters (Differential & Clutch Output)')
    display_cols = ['striker_name', 'Pressure_Rating', 'sr_base', 'sr_pres', 'avg_base', 'avg_pres', 'balls_pres', 'outs_pres', 'sr_std']
    st.dataframe(bat_stats[display_cols].head(10).round(2), use_container_width=True)

with tab3:
    st.markdown('### Top 10 Bowlers (Lockdown Efficiency)')
    display_cols = ['bowler_name', 'Pressure_Rating', 'econ_base', 'econ_pres', 'wickets_pres', 'balls_bowled_pres', 'sr_pres', 'econ_std', 'matches_played']
    st.dataframe(bowl_stats[display_cols].head(10).round(2), use_container_width=True)

with tab4:
    st.markdown('### Individual Player Intelligence')
    ptype = st.radio("Role:", ["Batting", "Bowling"], horizontal=True)
    
    if ptype == "Batting":
        player = st.selectbox("Search Batter", bat_stats['striker_name'].tolist())
        p_data = bat_stats[bat_stats['striker_name'] == player].iloc[0]
        col1, col2 = st.columns([1,2])
        with col1:
            st.metric("Pressure Rating", f"{p_data['Pressure_Rating']:.2f}")
            st.metric("Balls Faced (Pressure)", int(p_data['balls_pres']))
            st.metric("Dismissals (Pressure)", int(p_data['outs_pres']))
            st.metric("Consistency (Std Dev)", f"{p_data['sr_std']:.2f}")
        with col2:
            fig = go.Figure(data=[
                go.Bar(name='Baseline', x=['Strike Rate', 'Average'], y=[p_data['sr_base'], p_data['avg_base']], marker_color='#30363d'),
                go.Bar(name='Pressure', x=['Strike Rate', 'Average'], y=[p_data['sr_pres'], p_data['avg_pres']], marker_color='#2f81f7')
            ])
            fig.update_layout(barmode='group', template='plotly_dark', plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig, use_container_width=True)
    else:
        player = st.selectbox("Search Bowler", bowl_stats['bowler_name'].tolist())
        p_data = bowl_stats[bowl_stats['bowler_name'] == player].iloc[0]
        col1, col2 = st.columns([1,2])
        with col1:
            st.metric("Pressure Rating", f"{p_data['Pressure_Rating']:.2f}")
            st.metric("Balls Bowled (Pressure)", int(p_data['balls_bowled_pres']))
            st.metric("Wickets (Pressure)", int(p_data['wickets_pres']))
            st.metric("Consistency (Econ Std Dev)", f"{p_data['econ_std']:.2f}")
        with col2:
            fig = go.Figure(data=[
                go.Bar(name='Baseline', x=['Economy', 'Strike Rate'], y=[p_data['econ_base'], p_data['sr_base']], marker_color='#30363d'),
                go.Bar(name='Pressure', x=['Economy', 'Strike Rate'], y=[p_data['econ_pres'], p_data['sr_pres']], marker_color='#d29922')
            ])
            fig.update_layout(barmode='group', template='plotly_dark', plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig, use_container_width=True)

with tab5:
    st.markdown('### Head-to-Head Comparison')
    ctype = st.radio("Compare:", ["Batters", "Bowlers"], horizontal=True)
    if ctype == "Batters":
        players = st.multiselect("Select Batters", bat_stats['striker_name'].tolist(), default=bat_stats['striker_name'].head(2).tolist())
        if players:
            df_comp = bat_stats[bat_stats['striker_name'].isin(players)]
            fig = px.bar(df_comp, x='striker_name', y='Pressure_Rating', color='striker_name', template='plotly_dark')
            st.plotly_chart(fig, use_container_width=True)
    else:
        players = st.multiselect("Select Bowlers", bowl_stats['bowler_name'].tolist(), default=bowl_stats['bowler_name'].head(2).tolist())
        if players:
            df_comp = bowl_stats[bowl_stats['bowler_name'].isin(players)]
            fig = px.bar(df_comp, x='bowler_name', y='Pressure_Rating', color='bowler_name', template='plotly_dark')
            st.plotly_chart(fig, use_container_width=True)

with tab6:
    st.markdown('### Pressure Situation Analysis (Macro Trends)')
    # Show distribution of Z-Scores to avoid fabricating delivery-level charts without raw data loaded here
    fig1 = px.histogram(bat_stats, x='Pressure_Rating', title='Batting Pressure Rating Distribution', template='plotly_dark', color_discrete_sequence=['#2f81f7'])
    fig2 = px.histogram(bowl_stats, x='Pressure_Rating', title='Bowling Pressure Rating Distribution', template='plotly_dark', color_discrete_sequence=['#d29922'])
    col1, col2 = st.columns(2)
    col1.plotly_chart(fig1, use_container_width=True)
    col2.plotly_chart(fig2, use_container_width=True)

with tab7:
    st.markdown('''
    ### Analytical Methodology
    **Pressure Definitions:**
    * Chases requiring over 12.0 Runs Per Over.
    * Death Overs (Overs 19 & 20).
    * Top-Order Collapse (4+ Wickets lost within Powerplay).
    
    **Calculations:**
    * **Batting Model:** `Z(Pressure_Avg) + 1.5 * Z(Pressure_SR - Base_SR) + 0.5 * Z(Consistency)`
    * **Bowling Model:** `- [1.5 * Z(Pressure_Econ - Base_Econ) + Z(Pressure_SR)] + 0.5 * Z(Consistency)`
    * **Consistency:** Defined as the inverted standard deviation of match-by-match performance.
    * **Threshold Limits:** Filtered strictly to >100 balls (Batting) and >60 balls (Bowling) to resolve small-sample anomalies (e.g., S. Atal).
    ''')
