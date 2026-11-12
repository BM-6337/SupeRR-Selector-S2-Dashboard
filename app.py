import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- PAGE SETUP ---
st.set_page_config(page_title="SupeRR Selector 2 - Cyberpunk Edition", layout="wide", page_icon="⚡")

# --- CRAZY CUSTOM CSS ---
st.markdown('''
<style>
    /* Dark space background */
    .stApp {
        background-color: #050505;
        background-image: radial-gradient(circle at 50% 0%, #1a0b2e 0%, #050505 70%);
        color: #e0e0e0;
    }
    
    /* Animated Gradient Title */
    .title-glitch {
        font-size: 3.5rem;
        font-weight: 900;
        text-transform: uppercase;
        background: linear-gradient(to right, #ff00ff, #00ffff, #ff00ff);
        background-size: 200% auto;
        color: #fff;
        background-clip: text;
        text-fill-color: transparent;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: shine 3s linear infinite;
        text-align: center;
        margin-bottom: 0px;
    }
    @keyframes shine {
        to {
            background-position: 200% center;
        }
    }
    
    /* Neon glowing cards */
    .neon-card {
        background: rgba(20, 20, 20, 0.8);
        border: 1px solid #333;
        padding: 25px;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 0 15px rgba(0, 255, 255, 0.2);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        margin-bottom: 20px;
    }
    .neon-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 0 25px rgba(255, 0, 255, 0.6);
        border-color: #ff00ff;
    }
    .neon-card h3 {
        color: #00ffff;
        text-transform: uppercase;
        letter-spacing: 2px;
        font-size: 1.2rem;
        margin-bottom: 10px;
    }
    .neon-card h1 {
        color: #fff;
        font-size: 2.5rem;
        font-weight: bold;
        margin: 0;
        text-shadow: 0 0 10px rgba(255, 255, 255, 0.5);
    }
    .neon-card p {
        color: #ff00ff;
        font-size: 1.2rem;
        font-weight: bold;
        margin-top: 10px;
    }
    
    /* Subheaders */
    .sub-title {
        color: #00ffff;
        border-bottom: 2px solid #ff00ff;
        padding-bottom: 10px;
        margin-top: 30px;
        margin-bottom: 20px;
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
st.markdown('<div class="title-glitch">⚡ THE CLUTCH PROTOCOL ⚡</div>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center; color:#888; font-size:1.2rem; margin-bottom:40px;">Moneyball Engine v2.0 // Differential Match-Winners</p>', unsafe_allow_html=True)

# --- SIDEBAR ---
st.sidebar.markdown("<h2 style='color:#00ffff; text-align:center;'>SYSTEM MENU</h2>", unsafe_allow_html=True)
page = st.sidebar.radio("", ["🌌 The Arena", "🏏 Batting Hitlist", "🎯 Bowling Hitlist", "🔍 Player Spotlight"])

# --- PAGE 1: OVERVIEW ---
if page == "🌌 The Arena":
    st.markdown('<h2 class="sub-title">EXECUTIVE SUMMARY</h2>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    top_bat = bat_stats.iloc[0]
    top_bowl = bowl_stats.iloc[0]
    
    with col1:
        st.markdown(f'''
        <div class="neon-card" style="box-shadow: 0 0 20px rgba(0,255,255,0.4); border-color:#00ffff;">
            <h3>Top Differential Batter</h3>
            <h1>{top_bat['striker_name']}</h1>
            <p>Rating: {top_bat['Pressure_Rating']:.2f} 🚀</p>
        </div>
        ''', unsafe_allow_html=True)
        
    with col2:
        st.markdown(f'''
        <div class="neon-card" style="box-shadow: 0 0 20px rgba(255,0,255,0.4); border-color:#ff00ff;">
            <h3>Top Differential Bowler</h3>
            <h1>{top_bowl['bowler_name']}</h1>
            <p>Rating: {top_bowl['Pressure_Rating']:.2f} 🎯</p>
        </div>
        ''', unsafe_allow_html=True)
        
    with col3:
        st.markdown(f'''
        <div class="neon-card" style="box-shadow: 0 0 20px rgba(255,255,0,0.4); border-color:#ffff00;">
            <h3>Players Analyzed</h3>
            <h1>400+</h1>
            <p>Strict Variance Penalty Active ⚠️</p>
        </div>
        ''', unsafe_allow_html=True)
        
    st.markdown('<h2 class="sub-title">HOW IT WORKS</h2>', unsafe_allow_html=True)
    st.info("We isolated deliveries in the 19th/20th overs, chases requiring 12+ RPO, or 4-wicket collapses. Players are rewarded with a **1.5x Multiplier** on their differential (Pressure Stats minus Base Stats) and penalized for match-to-match variance.")

# --- PAGE 2: BATTING ---
elif page == "🏏 Batting Hitlist":
    st.markdown('<h2 class="sub-title">BATTING CLUTCH RANKINGS</h2>', unsafe_allow_html=True)
    
    fig = px.scatter(bat_stats.head(20), x='sr_base', y='sr_pres', size='Pressure_Rating', 
                     color='Pressure_Rating', hover_name='striker_name',
                     text='striker_name', color_continuous_scale='cool',
                     title="Base Strike Rate vs. Extreme Pressure Strike Rate (Size = Clutch Rating)")
    
    fig.update_traces(textposition='top center', marker=dict(line=dict(width=2, color='DarkSlateGrey')))
    fig.update_layout(template='plotly_dark', plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
    # Add a diagonal line for baseline (x=y)
    max_val = max(bat_stats['sr_base'].max(), bat_stats['sr_pres'].max())
    fig.add_shape(type="line", x0=100, y0=100, x1=max_val, y1=max_val, line=dict(color="gray", width=2, dash="dash"))
    
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(bat_stats[['striker_name', 'Pressure_Rating', 'sr_base', 'sr_pres', 'sr_std']].head(15).style.background_gradient(cmap='cool'), use_container_width=True)

# --- PAGE 3: BOWLING ---
elif page == "🎯 Bowling Hitlist":
    st.markdown('<h2 class="sub-title">BOWLING CLUTCH RANKINGS</h2>', unsafe_allow_html=True)
    
    fig = px.bar(bowl_stats.head(10), x='Pressure_Rating', y='bowler_name', orientation='h',
                 color='Pressure_Rating', color_continuous_scale='sunset',
                 title="Top 10 Ice-Cold Bowlers (Differential Rating)")
    fig.update_layout(template='plotly_dark', plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', yaxis={'categoryorder':'total ascending'})
    
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(bowl_stats[['bowler_name', 'Pressure_Rating', 'econ_base', 'econ_pres', 'econ_std']].head(15).style.background_gradient(cmap='sunset_r'), use_container_width=True)

# --- PAGE 4: PLAYER SPOTLIGHT ---
elif page == "🔍 Player Spotlight":
    st.markdown('<h2 class="sub-title">INDIVIDUAL PROFILE SCANS</h2>', unsafe_allow_html=True)
    
    player_type = st.radio("Select Category:", ["Batters", "Bowlers"], horizontal=True)
    
    if player_type == "Batters":
        player = st.selectbox("Select Batter", bat_stats['striker_name'].tolist())
        p_data = bat_stats[bat_stats['striker_name'] == player].iloc[0]
        
        col1, col2 = st.columns([1, 2])
        with col1:
            st.markdown(f'''
            <div class="neon-card" style="border-color:#00ffff;">
                <h3>{player}</h3>
                <h1 style="font-size:2rem; color:#00ffff;">Rank: #{bat_stats.index[bat_stats['striker_name'] == player][0] + 1}</h1>
                <p>Clutch Rating: {p_data['Pressure_Rating']:.2f}</p>
            </div>
            ''', unsafe_allow_html=True)
            
        with col2:
            # Radar Chart
            fig = go.Figure(data=go.Scatterpolar(
              r=[p_data['sr_base'], p_data['sr_pres'], p_data['avg_base'], p_data['avg_pres']],
              theta=['Base SR', 'Pressure SR', 'Base Avg', 'Pressure Avg'],
              fill='toself',
              line_color='#00ffff'
            ))
            fig.update_layout(
              polar=dict(radialaxis=dict(visible=True, range=[0, max(p_data['sr_pres'], 200)])),
              showlegend=False, template='plotly_dark', plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
              title=f"{player}: Base vs Extreme Pressure"
            )
            st.plotly_chart(fig, use_container_width=True)
            
    else:
        player = st.selectbox("Select Bowler", bowl_stats['bowler_name'].tolist())
        p_data = bowl_stats[bowl_stats['bowler_name'] == player].iloc[0]
        
        col1, col2 = st.columns([1, 2])
        with col1:
            st.markdown(f'''
            <div class="neon-card" style="border-color:#ff00ff;">
                <h3>{player}</h3>
                <h1 style="font-size:2rem; color:#ff00ff;">Rank: #{bowl_stats.index[bowl_stats['bowler_name'] == player][0] + 1}</h1>
                <p>Clutch Rating: {p_data['Pressure_Rating']:.2f}</p>
            </div>
            ''', unsafe_allow_html=True)
            
        with col2:
            # Gauge Chart for Economy
            fig = go.Figure(go.Indicator(
                mode = "gauge+number+delta",
                value = p_data['econ_pres'],
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': "Pressure Economy (Lower is Better)"},
                delta = {'reference': p_data['econ_base'], 'increasing': {'color': "red"}, 'decreasing':{'color':"green"}},
                gauge = {
                    'axis': {'range': [None, 15]},
                    'bar': {'color': "#ff00ff"},
                    'steps' : [
                        {'range': [0, 6], 'color': "rgba(0,255,0,0.3)"},
                        {'range': [6, 10], 'color': "rgba(255,255,0,0.3)"},
                        {'range': [10, 15], 'color': "rgba(255,0,0,0.3)"}],
                }
            ))
            fig.update_layout(template='plotly_dark', plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig, use_container_width=True)
