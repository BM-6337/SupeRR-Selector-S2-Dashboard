import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- PAGE SETUP ---
st.set_page_config(page_title="SupeRR Selector 2 - The Moneyball Engine", layout="wide", page_icon="🏏")

# --- PREMIUM ANALYTICS CSS ---
st.markdown('''
<style>
    /* Clean, premium dark mode */
    .stApp {
        background-color: #0d1117;
        color: #c9d1d9;
    }
    
    /* Elegant Title */
    .premium-title {
        font-family: 'Helvetica Neue', sans-serif;
        font-size: 3.2rem;
        font-weight: 300;
        letter-spacing: -1px;
        color: #f0f6fc;
        border-left: 6px solid #2f81f7;
        padding-left: 15px;
        margin-bottom: 5px;
    }
    .premium-subtitle {
        font-family: 'Helvetica Neue', sans-serif;
        font-size: 1.2rem;
        color: #8b949e;
        margin-bottom: 40px;
        padding-left: 21px;
    }
    
    /* Clean Metric Cards */
    .metric-card {
        background: #161b22;
        border: 1px solid #30363d;
        padding: 24px;
        border-radius: 8px;
        text-align: left;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    .metric-card:hover {
        transform: translateY(-2px);
        border-color: #2f81f7;
    }
    .metric-card h3 {
        color: #8b949e;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin-bottom: 12px;
        font-weight: 600;
    }
    .metric-card h1 {
        color: #f0f6fc;
        font-size: 2.4rem;
        font-weight: 700;
        margin: 0;
        line-height: 1.2;
    }
    .metric-card p {
        color: #2ea043;
        font-size: 1rem;
        margin-top: 8px;
        font-weight: 500;
    }
    
    /* Subheaders */
    .section-header {
        font-family: 'Helvetica Neue', sans-serif;
        color: #c9d1d9;
        font-size: 1.5rem;
        font-weight: 500;
        margin-top: 40px;
        margin-bottom: 20px;
        padding-bottom: 10px;
        border-bottom: 1px solid #30363d;
    }
</style>
''', unsafe_allow_html=True)

# --- DATA LOADING ---
@st.cache_data
def load_data():
    bat_stats = pd.read_csv('bat_stats_2.csv')
    bowl_stats = pd.read_csv('bowl_stats_2.csv')
    return bat_stats.head(50), bowl_stats.head(50)

bat_stats, bowl_stats = load_data()

# --- HEADER ---
st.markdown('<div class="premium-title">Asymmetric Value Engine</div>', unsafe_allow_html=True)
st.markdown('<div class="premium-subtitle">SupeRR Selector Season 2 | Differential Match-Winner Identification</div>', unsafe_allow_html=True)

# --- TABS ---
tab1, tab2, tab3, tab4 = st.tabs(["Overview", "Batting Differentials", "Bowling Differentials", "Player Profiles"])

# --- TAB 1: OVERVIEW ---
with tab1:
    st.markdown('<div class="section-header">Executive Summary</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    top_bat = bat_stats.iloc[0]
    top_bowl = bowl_stats.iloc[0]
    
    with col1:
        st.markdown(f'''
        <div class="metric-card">
            <h3>Highest Value Batter</h3>
            <h1>{top_bat['striker_name']}</h1>
            <p>+{top_bat['Pressure_Rating']:.2f} Differential Rating</p>
        </div>
        ''', unsafe_allow_html=True)
        
    with col2:
        st.markdown(f'''
        <div class="metric-card">
            <h3>Highest Value Bowler</h3>
            <h1>{top_bowl['bowler_name']}</h1>
            <p>+{top_bowl['Pressure_Rating']:.2f} Differential Rating</p>
        </div>
        ''', unsafe_allow_html=True)
        
    with col3:
        st.markdown(f'''
        <div class="metric-card">
            <h3>Data Pipeline</h3>
            <h1>400+</h1>
            <p style="color:#8b949e;">Players Processed & Verified</p>
        </div>
        ''', unsafe_allow_html=True)
        
    st.markdown('<div class="section-header">Methodology Overview</div>', unsafe_allow_html=True)
    st.info("This model ignores standard volume metrics. Instead, it measures 'Clutch Differential'—identifying players whose statistical output drastically improves during extreme match situations (Overs 19-20, RRR > 12, or top-order collapses), while mathematically penalizing match-to-match volatility.")

# --- TAB 2: BATTING ---
with tab2:
    st.markdown('<div class="section-header">Batting Clutch Rankings</div>', unsafe_allow_html=True)
    
    # Changed to Horizontal Bar Chart to match Bowling
    fig = px.bar(bat_stats.head(10), x='Pressure_Rating', y='striker_name', orientation='h',
                 color='Pressure_Rating', color_continuous_scale='Blues',
                 title="Top 10 High-Pressure Clutch Batters")
    fig.update_layout(template='plotly_dark', plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', yaxis={'categoryorder':'total ascending'})
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Extended dataframe to 50
    st.dataframe(bat_stats[['striker_name', 'Pressure_Rating', 'sr_base', 'sr_pres', 'sr_std']].head(50).round(2), use_container_width=True)

# --- TAB 3: BOWLING ---
with tab3:
    st.markdown('<div class="section-header">Bowling Clutch Rankings</div>', unsafe_allow_html=True)
    
    fig = px.bar(bowl_stats.head(10), x='Pressure_Rating', y='bowler_name', orientation='h',
                 color='Pressure_Rating', color_continuous_scale='Oranges',
                 title="Top 10 High-Pressure Lockdown Bowlers")
    fig.update_layout(template='plotly_dark', plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', yaxis={'categoryorder':'total ascending'})
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Extended dataframe to 50
    st.dataframe(bowl_stats[['bowler_name', 'Pressure_Rating', 'econ_base', 'econ_pres', 'econ_std']].head(50).round(2), use_container_width=True)

# --- TAB 4: PLAYER PROFILES ---
with tab4:
    st.markdown('<div class="section-header">Individual Player Scans</div>', unsafe_allow_html=True)
    
    player_type = st.radio("Select Role:", ["Batters", "Bowlers"], horizontal=True)
    
    if player_type == "Batters":
        player = st.selectbox("Select Batter", bat_stats['striker_name'].tolist())
        p_data = bat_stats[bat_stats['striker_name'] == player].iloc[0]
        
        col1, col2 = st.columns([1, 2])
        with col1:
            st.markdown(f'''
            <div class="metric-card" style="border-left: 4px solid #2f81f7;">
                <h3>{player}</h3>
                <h1 style="font-size:2rem; color:#f0f6fc;">Global Rank: #{bat_stats.index[bat_stats['striker_name'] == player][0] + 1}</h1>
                <p style="color:#2f81f7;">Clutch Rating: {p_data['Pressure_Rating']:.2f}</p>
            </div>
            ''', unsafe_allow_html=True)
            
        with col2:
            fig = go.Figure(data=go.Scatterpolar(
              r=[p_data['sr_base'], p_data['sr_pres'], p_data['avg_base'], p_data['avg_pres']],
              theta=['Base SR', 'Pressure SR', 'Base Avg', 'Pressure Avg'],
              fill='toself',
              line_color='#2f81f7',
              fillcolor='rgba(47, 129, 247, 0.2)'
            ))
            fig.update_layout(
              polar=dict(radialaxis=dict(visible=True, range=[0, max(p_data['sr_pres'], 200)], gridcolor='#30363d')),
              showlegend=False, template='plotly_dark', plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
              title=f"{player}: Base vs Extreme Pressure Output"
            )
            st.plotly_chart(fig, use_container_width=True)
            
    else:
        player = st.selectbox("Select Bowler", bowl_stats['bowler_name'].tolist())
        p_data = bowl_stats[bowl_stats['bowler_name'] == player].iloc[0]
        
        col1, col2 = st.columns([1, 2])
        with col1:
            st.markdown(f'''
            <div class="metric-card" style="border-left: 4px solid #d29922;">
                <h3>{player}</h3>
                <h1 style="font-size:2rem; color:#f0f6fc;">Global Rank: #{bowl_stats.index[bowl_stats['bowler_name'] == player][0] + 1}</h1>
                <p style="color:#d29922;">Clutch Rating: {p_data['Pressure_Rating']:.2f}</p>
            </div>
            ''', unsafe_allow_html=True)
            
        with col2:
            fig = go.Figure(go.Indicator(
                mode = "gauge+number+delta",
                value = p_data['econ_pres'],
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': "Pressure Economy (Lower is Better)", 'font': {'color': '#8b949e'}},
                delta = {'reference': p_data['econ_base'], 'increasing': {'color': "#f85149"}, 'decreasing':{'color':"#2ea043"}},
                gauge = {
                    'axis': {'range': [None, 15], 'tickcolor': "#8b949e"},
                    'bar': {'color': "#d29922"},
                    'bgcolor': "#161b22",
                    'borderwidth': 1,
                    'bordercolor': "#30363d",
                    'steps' : [
                        {'range': [0, 7], 'color': "rgba(46,160,67,0.1)"},
                        {'range': [7, 10], 'color': "rgba(210,153,34,0.1)"},
                        {'range': [10, 15], 'color': "rgba(248,81,73,0.1)"}],
                }
            ))
            fig.update_layout(template='plotly_dark', plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig, use_container_width=True)
