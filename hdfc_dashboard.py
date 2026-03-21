import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px

st.set_page_config(
    page_title="HDFC Bank Pro Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Custom CSS with animations ─────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

* { font-family: 'Inter', sans-serif; }

.main { background: linear-gradient(135deg, #0a0a0a 0%, #0d1117 100%); }

.stApp { background: linear-gradient(135deg, #0a0a0a 0%, #0d1117 100%); }

.hero-header {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    border: 1px solid #e94560;
    border-radius: 16px;
    padding: 30px;
    margin-bottom: 20px;
    text-align: center;
    animation: fadeInDown 0.8s ease;
    box-shadow: 0 0 40px rgba(233, 69, 96, 0.3);
}

@keyframes fadeInDown {
    from { opacity: 0; transform: translateY(-30px); }
    to   { opacity: 1; transform: translateY(0); }
}

@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(30px); }
    to   { opacity: 1; transform: translateY(0); }
}

@keyframes pulse {
    0%   { box-shadow: 0 0 0 0 rgba(233, 69, 96, 0.4); }
    70%  { box-shadow: 0 0 0 10px rgba(233, 69, 96, 0); }
    100% { box-shadow: 0 0 0 0 rgba(233, 69, 96, 0); }
}

@keyframes glow {
    0%   { text-shadow: 0 0 10px #e94560; }
    50%  { text-shadow: 0 0 30px #e94560, 0 0 60px #e94560; }
    100% { text-shadow: 0 0 10px #e94560; }
}

@keyframes slideIn {
    from { opacity: 0; transform: translateX(-20px); }
    to   { opacity: 1; transform: translateX(0); }
}

.hero-title {
    font-size: 3rem;
    font-weight: 700;
    color: #ffffff;
    animation: glow 3s infinite;
    margin: 0;
}

.hero-subtitle {
    color: #e94560;
    font-size: 1.1rem;
    margin-top: 8px;
    animation: fadeInUp 1s ease;
}

.live-badge {
    display: inline-block;
    background: #e94560;
    color: white;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 600;
    animation: pulse 2s infinite;
    margin-left: 10px;
}

.kpi-card {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
    border: 1px solid #e94560;
    border-radius: 12px;
    padding: 20px;
    text-align: center;
    animation: fadeInUp 0.6s ease;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    margin-bottom: 10px;
}

.kpi-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 10px 30px rgba(233, 69, 96, 0.4);
}

.kpi-value {
    font-size: 1.8rem;
    font-weight: 700;
    color: #e94560;
    display: block;
}

.kpi-label {
    font-size: 0.8rem;
    color: #8b8b8b;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-top: 5px;
}

.kpi-change-positive { color: #00ff88; font-size: 0.9rem; }
.kpi-change-negative { color: #ff4444; font-size: 0.9rem; }

.section-header {
    background: linear-gradient(90deg, #e94560 0%, transparent 100%);
    padding: 10px 20px;
    border-radius: 8px;
    margin: 20px 0 15px 0;
    animation: slideIn 0.5s ease;
}

.section-title {
    color: white;
    font-size: 1.2rem;
    font-weight: 600;
    margin: 0;
}

.signal-bullish {
    background: linear-gradient(135deg, #0d2818, #1a4a2e);
    border: 1px solid #00ff88;
    border-radius: 8px;
    padding: 15px;
    text-align: center;
    animation: fadeInUp 0.5s ease;
}

.signal-bearish {
    background: linear-gradient(135deg, #2a0d0d, #4a1a1a);
    border: 1px solid #ff4444;
    border-radius: 8px;
    padding: 15px;
    text-align: center;
    animation: fadeInUp 0.5s ease;
}

.signal-neutral {
    background: linear-gradient(135deg, #1a1a0d, #2a2a1a);
    border: 1px solid #ffaa00;
    border-radius: 8px;
    padding: 15px;
    text-align: center;
    animation: fadeInUp 0.5s ease;
}

.pattern-card {
    background: #1a1a2e;
    border-left: 4px solid #e94560;
    border-radius: 8px;
    padding: 12px 16px;
    margin: 8px 0;
    animation: slideIn 0.5s ease;
    transition: all 0.3s ease;
}

.pattern-card:hover { background: #16213e; transform: translateX(5px); }

.stats-card {
    background: linear-gradient(135deg, #1a1a2e, #16213e);
    border: 1px solid #2a2a4a;
    border-radius: 10px;
    padding: 15px;
    animation: fadeInUp 0.7s ease;
}

.ticker-bar {
    background: #1a1a2e;
    border-top: 1px solid #e94560;
    border-bottom: 1px solid #e94560;
    padding: 8px 0;
    overflow: hidden;
    margin-bottom: 20px;
}

.footer {
    background: linear-gradient(135deg, #1a1a2e, #0d1117);
    border-top: 1px solid #e94560;
    border-radius: 12px;
    padding: 20px;
    text-align: center;
    margin-top: 30px;
    color: #8b8b8b;
    font-size: 0.85rem;
}
</style>
""", unsafe_allow_html=True)

# ── Sidebar ────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 15px; background: linear-gradient(135deg,#1a1a2e,#16213e);
    border-radius:12px; border:1px solid #e94560; margin-bottom:20px;'>
    <h2 style='color:#e94560; margin:0;'>⚙️ Control Panel</h2>
    <p style='color:#8b8b8b; font-size:0.8rem; margin:5px 0 0 0;'>HDFC Bank Analytics</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 📅 Date Range")
    start_date = st.date_input("Start Date", pd.to_datetime("2020-01-01"))
    end_date   = st.date_input("End Date",   pd.to_datetime("2025-03-21"))

    st.markdown("### 📊 Chart Settings")
    chart_type  = st.selectbox("Chart Type", ["Candlestick", "Line", "OHLC"])
    chart_theme = st.selectbox("Theme", ["Dark", "Midnight", "Forest"])

    st.markdown("### 📈 Indicators")
    show_sma    = st.checkbox("SMA (20/50/200)",    value=True)
    show_ema    = st.checkbox("EMA (20)",            value=True)
    show_bb     = st.checkbox("Bollinger Bands",     value=True)
    show_vwap   = st.checkbox("VWAP",                value=False)
    show_atr    = st.checkbox("ATR (Volatility)",    value=False)

    st.markdown("### 🕯️ Patterns")
    show_doji       = st.checkbox("Mark Doji",             value=True)
    show_hammer     = st.checkbox("Mark Hammer",           value=True)
    show_engulfing  = st.checkbox("Mark Engulfing",        value=True)

    st.markdown("### 🔢 Analysis Period")
    rsi_period  = st.slider("RSI Period",     7,  28, 14)
    bb_period   = st.slider("BB Period",      10, 50, 20)
    sma_fast    = st.slider("Fast SMA",       5,  50, 20)
    sma_slow    = st.slider("Slow SMA",       50, 200, 50)

    st.markdown("""
    <div style='background:#1a1a2e; border:1px solid #2a2a4a; border-radius:8px;
    padding:12px; margin-top:20px; font-size:0.75rem; color:#8b8b8b; text-align:center;'>
    📡 Data: NSE via Yahoo Finance<br>
    🔄 Auto-refresh on date change<br>
    📊 1294 trading days loaded
    </div>
    """, unsafe_allow_html=True)

# ── Load Data ──────────────────────────────────────────────────
@st.cache_data
def load_data(start, end, rsi_p, bb_p, sma_f, sma_s):
    df = pd.read_csv("hdfc_data.csv", index_col=0, parse_dates=True)
    df.index = pd.to_datetime(df.index)
    df = df[(df.index >= pd.Timestamp(start)) & (df.index <= pd.Timestamp(end))].copy()

    df[f'SMA_{sma_f}']  = df['Close'].rolling(sma_f).mean()
    df[f'SMA_{sma_s}']  = df['Close'].rolling(sma_s).mean()
    df['SMA_200']        = df['Close'].rolling(200).mean()
    df['EMA_20']         = df['Close'].ewm(span=20, adjust=False).mean()
    df['BB_Mid']         = df['Close'].rolling(bb_p).mean()
    df['BB_Std']         = df['Close'].rolling(bb_p).std()
    df['BB_Upper']       = df['BB_Mid'] + 2 * df['BB_Std']
    df['BB_Lower']       = df['BB_Mid'] - 2 * df['BB_Std']
    df['BB_Width']       = (df['BB_Upper'] - df['BB_Lower']) / df['BB_Mid'] * 100

    delta = df['Close'].diff()
    gain  = delta.where(delta > 0, 0).rolling(rsi_p).mean()
    loss  = -delta.where(delta < 0, 0).rolling(rsi_p).mean()
    df['RSI']            = 100 - (100 / (1 + gain / loss))

    ema12 = df['Close'].ewm(span=12, adjust=False).mean()
    ema26 = df['Close'].ewm(span=26, adjust=False).mean()
    df['MACD']           = ema12 - ema26
    df['MACD_Signal']    = df['MACD'].ewm(span=9, adjust=False).mean()
    df['MACD_Hist']      = df['MACD'] - df['MACD_Signal']

    df['Daily_Return']   = df['Close'].pct_change() * 100
    df['Volatility']     = df['Daily_Return'].rolling(20).std()
    df['VWAP']           = (df['Close'] * df['Volume']).cumsum() / df['Volume'].cumsum()

    tr1 = df['High'] - df['Low']
    tr2 = abs(df['High'] - df['Close'].shift())
    tr3 = abs(df['Low'] - df['Close'].shift())
    df['ATR']            = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1).rolling(14).mean()

    df['Body']           = abs(df['Close'] - df['Open'])
    df['Body_Range']     = df['High'] - df['Low']
    df['Upper_Shadow']   = df['High'] - df[['Close','Open']].max(axis=1)
    df['Lower_Shadow']   = df[['Close','Open']].min(axis=1) - df['Low']
    df['Doji']              = df['Body'] <= 0.1 * df['Body_Range']
    df['Hammer']            = (df['Lower_Shadow'] >= 2*df['Body']) & (df['Upper_Shadow'] <= 0.1*df['Body_Range']) & (df['Body'] > 0)
    df['Shooting_Star']     = (df['Upper_Shadow'] >= 2*df['Body']) & (df['Lower_Shadow'] <= 0.1*df['Body_Range']) & (df['Body'] > 0)
    df['Bullish_Engulfing'] = (df['Close']>df['Open']) & (df['Close'].shift(1)<df['Open'].shift(1)) & (df['Close']>df['Open'].shift(1)) & (df['Open']<df['Close'].shift(1))
    df['Bearish_Engulfing'] = (df['Close']<df['Open']) & (df['Close'].shift(1)>df['Open'].shift(1)) & (df['Close']<df['Open'].shift(1)) & (df['Open']>df['Close'].shift(1))
    df['Bullish'] = df['Close'] >= df['Open']

    df['Support']    = df['Low'].rolling(20).min()
    df['Resistance'] = df['High'].rolling(20).max()
    return df

df = load_data(start_date, end_date, rsi_period, bb_period, sma_fast, sma_slow)

if df.empty:
    st.error("No data found for the selected date range.")
    st.stop()

# ── Computed Stats ─────────────────────────────────────────────
current_price   = df['Close'].iloc[-1]
prev_price      = df['Close'].iloc[-2]
price_change    = current_price - prev_price
price_change_pct= (price_change / prev_price) * 100
current_rsi     = df['RSI'].iloc[-1]
current_macd    = df['MACD'].iloc[-1]
current_vol     = df['Volatility'].iloc[-1]
week52_high     = df['High'].tail(252).max()
week52_low      = df['Low'].tail(252).min()
avg_volume      = df['Volume'].mean()
total_return    = ((current_price / df['Close'].iloc[0]) - 1) * 100

# ── Hero Header ────────────────────────────────────────────────
st.markdown(f"""
<div class='hero-header'>
    <h1 class='hero-title'>📈 HDFC Bank <span style='color:#e94560;'>Pro</span> Dashboard
        <span class='live-badge'>● LIVE</span>
    </h1>
    <p class='hero-subtitle'>NSE: HDFCBANK &nbsp;|&nbsp; Real-time Price Action Analysis &nbsp;|&nbsp;
    {len(df)} Trading Days &nbsp;|&nbsp;
    {'🟢 +' if price_change >= 0 else '🔴 '}{price_change:.2f} ({price_change_pct:+.2f}%)</p>
</div>
""", unsafe_allow_html=True)

# ── KPI Cards ──────────────────────────────────────────────────
st.markdown("<div class='section-header'><p class='section-title'>📊 Key Performance Indicators</p></div>", unsafe_allow_html=True)

k1, k2, k3, k4, k5, k6, k7, k8 = st.columns(8)

kpis = [
    (k1, "Current Price",  f"₹{current_price:.2f}",    f"{'▲' if price_change>=0 else '▼'} {price_change_pct:+.2f}%", price_change>=0),
    (k2, "52W High",       f"₹{week52_high:.2f}",      f"{((current_price/week52_high)-1)*100:.1f}% from high", False),
    (k3, "52W Low",        f"₹{week52_low:.2f}",       f"{((current_price/week52_low)-1)*100:.1f}% from low", True),
    (k4, "RSI (14)",       f"{current_rsi:.1f}",        "Overbought" if current_rsi>70 else "Oversold" if current_rsi<30 else "Neutral", current_rsi<=70),
    (k5, "MACD",           f"{current_macd:.2f}",       "Bullish" if current_macd>0 else "Bearish", current_macd>0),
    (k6, "Volatility",     f"{current_vol:.2f}%",       "20-day std dev", True),
    (k7, "Avg Volume",     f"{avg_volume/1e6:.1f}M",    "Daily average", True),
    (k8, "Total Return",   f"{total_return:.1f}%",      f"Since {df.index[0].strftime('%b %Y')}", total_return>0),
]

for col, label, value, change, positive in kpis:
    color = "#00ff88" if positive else "#ff4444"
    col.markdown(f"""
    <div class='kpi-card'>
        <span class='kpi-value'>{value}</span>
        <div class='kpi-label'>{label}</div>
        <div style='color:{color}; font-size:0.75rem; margin-top:5px;'>{change}</div>
    </div>
    """, unsafe_allow_html=True)

# ── Trading Signals ────────────────────────────────────────────
st.markdown("<div class='section-header'><p class='section-title'>🚦 Trading Signals</p></div>", unsafe_allow_html=True)

s1, s2, s3, s4, s5 = st.columns(5)

rsi_signal   = "OVERBOUGHT 🔴" if current_rsi > 70 else "OVERSOLD 🟢" if current_rsi < 30 else "NEUTRAL 🟡"
rsi_class    = "signal-bearish" if current_rsi > 70 else "signal-bullish" if current_rsi < 30 else "signal-neutral"
macd_signal  = "BULLISH 🟢" if current_macd > 0 else "BEARISH 🔴"
macd_class   = "signal-bullish" if current_macd > 0 else "signal-bearish"
bb_pos       = (current_price - df['BB_Lower'].iloc[-1]) / (df['BB_Upper'].iloc[-1] - df['BB_Lower'].iloc[-1]) * 100
bb_signal    = "UPPER BAND 🔴" if bb_pos > 80 else "LOWER BAND 🟢" if bb_pos < 20 else "MID BAND 🟡"
bb_class     = "signal-bearish" if bb_pos > 80 else "signal-bullish" if bb_pos < 20 else "signal-neutral"
trend_signal = "UPTREND 🟢" if current_price > df['SMA_200'].iloc[-1] else "DOWNTREND 🔴"
trend_class  = "signal-bullish" if current_price > df['SMA_200'].iloc[-1] else "signal-bearish"
vol_signal   = "HIGH VOL 🔴" if current_vol > df['Volatility'].mean() * 1.5 else "LOW VOL 🟢"
vol_class    = "signal-bearish" if current_vol > df['Volatility'].mean() * 1.5 else "signal-bullish"

for col, title, signal, cls in [
    (s1, "RSI Signal",     rsi_signal,   rsi_class),
    (s2, "MACD Signal",    macd_signal,  macd_class),
    (s3, "BB Position",    bb_signal,    bb_class),
    (s4, "Trend (SMA200)", trend_signal, trend_class),
    (s5, "Volatility",     vol_signal,   vol_class),
]:
    col.markdown(f"""
    <div class='{cls}'>
        <div style='color:#8b8b8b; font-size:0.75rem; text-transform:uppercase;'>{title}</div>
        <div style='font-size:1rem; font-weight:700; margin-top:5px;'>{signal}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ── Main Price Chart ───────────────────────────────────────────
st.markdown("<div class='section-header'><p class='section-title'>💹 Advanced Price Chart</p></div>", unsafe_allow_html=True)

template = "plotly_dark"
fig = make_subplots(
    rows=4, cols=1,
    shared_xaxes=True,
    row_heights=[0.5, 0.18, 0.18, 0.14],
    vertical_spacing=0.02,
    subplot_titles=("Price Action", "Volume", "RSI", "MACD")
)

if chart_type == "Candlestick":
    fig.add_trace(go.Candlestick(
        x=df.index, open=df['Open'], high=df['High'],
        low=df['Low'], close=df['Close'], name='HDFC',
        increasing_line_color='#00ff88', decreasing_line_color='#ff4444'
    ), row=1, col=1)
elif chart_type == "OHLC":
    fig.add_trace(go.Ohlc(
        x=df.index, open=df['Open'], high=df['High'],
        low=df['Low'], close=df['Close'], name='HDFC'
    ), row=1, col=1)
else:
    fig.add_trace(go.Scatter(
        x=df.index, y=df['Close'], name='Close',
        line=dict(color='#e94560', width=2),
        fill='tozeroy', fillcolor='rgba(233,69,96,0.1)'
    ), row=1, col=1)

if show_sma:
    for col_name, color, name in [(f'SMA_{sma_fast}','#f7b731',f'SMA {sma_fast}'),
                                   (f'SMA_{sma_slow}','#20bf6b',f'SMA {sma_slow}'),
                                   ('SMA_200','#eb3b5a','SMA 200')]:
        if col_name in df.columns:
            fig.add_trace(go.Scatter(x=df.index, y=df[col_name], name=name,
                                     line=dict(color=color, width=1.2)), row=1, col=1)

if show_ema:
    fig.add_trace(go.Scatter(x=df.index, y=df['EMA_20'], name='EMA 20',
                             line=dict(color='#a55eea', width=1.2, dash='dot')), row=1, col=1)

if show_vwap:
    fig.add_trace(go.Scatter(x=df.index, y=df['VWAP'], name='VWAP',
                             line=dict(color='#45aaf2', width=1.2, dash='dash')), row=1, col=1)

if show_bb:
    fig.add_trace(go.Scatter(x=df.index, y=df['BB_Upper'], name='BB Upper',
                             line=dict(color='rgba(255,255,255,0.3)', width=0.8)), row=1, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=df['BB_Lower'], name='BB Lower',
                             line=dict(color='rgba(255,255,255,0.3)', width=0.8),
                             fill='tonexty', fillcolor='rgba(255,255,255,0.03)'), row=1, col=1)

if show_doji:
    doji_df = df[df['Doji']]
    fig.add_trace(go.Scatter(x=doji_df.index, y=doji_df['High']*1.01,
                             mode='markers', name='Doji',
                             marker=dict(symbol='circle', color='#fed330', size=8)), row=1, col=1)

if show_hammer:
    hammer_df = df[df['Hammer']]
    fig.add_trace(go.Scatter(x=hammer_df.index, y=hammer_df['Low']*0.99,
                             mode='markers', name='Hammer',
                             marker=dict(symbol='triangle-up', color='#20bf6b', size=10)), row=1, col=1)

if show_engulfing:
    bull_df = df[df['Bullish_Engulfing']]
    bear_df = df[df['Bearish_Engulfing']]
    fig.add_trace(go.Scatter(x=bull_df.index, y=bull_df['Low']*0.99,
                             mode='markers', name='Bull Engulf',
                             marker=dict(symbol='star', color='#20bf6b', size=12)), row=1, col=1)
    fig.add_trace(go.Scatter(x=bear_df.index, y=bear_df['High']*1.01,
                             mode='markers', name='Bear Engulf',
                             marker=dict(symbol='star', color='#eb3b5a', size=12)), row=1, col=1)

colors_vol = ['#20bf6b' if c >= o else '#eb3b5a' for c, o in zip(df['Close'], df['Open'])]
fig.add_trace(go.Bar(x=df.index, y=df['Volume'], name='Volume',
                     marker_color=colors_vol, opacity=0.7), row=2, col=1)

fig.add_trace(go.Scatter(x=df.index, y=df['RSI'], name='RSI',
                         line=dict(color='#f7b731', width=1.5)), row=3, col=1)
fig.add_hrect(y0=70, y1=100, fillcolor='rgba(235,59,90,0.1)', line_width=0, row=3, col=1)
fig.add_hrect(y0=0,  y1=30,  fillcolor='rgba(32,191,107,0.1)', line_width=0, row=3, col=1)
fig.add_hline(y=70, line_dash='dash', line_color='#eb3b5a', line_width=1, row=3, col=1)
fig.add_hline(y=30, line_dash='dash', line_color='#20bf6b', line_width=1, row=3, col=1)

fig.add_trace(go.Bar(x=df.index, y=df['MACD_Hist'], name='MACD Hist',
                     marker_color=['#20bf6b' if v >= 0 else '#eb3b5a' for v in df['MACD_Hist']],
                     opacity=0.7), row=4, col=1)
fig.add_trace(go.Scatter(x=df.index, y=df['MACD'],        name='MACD',
                         line=dict(color='#45aaf2', width=1.2)), row=4, col=1)
fig.add_trace(go.Scatter(x=df.index, y=df['MACD_Signal'], name='Signal',
                         line=dict(color='#eb3b5a', width=1.2)), row=4, col=1)

fig.update_layout(
    height=900,
    template=template,
    xaxis_rangeslider_visible=False,
    paper_bgcolor='#0d1117',
    plot_bgcolor='#0d1117',
    legend=dict(orientation='h', yanchor='bottom', y=1.01, bgcolor='rgba(0,0,0,0)'),
    font=dict(color='#8b8b8b'),
    margin=dict(l=0, r=0, t=30, b=0)
)
for i in range(1, 5):
    fig.update_xaxes(gridcolor='#1a1a2e', row=i, col=1)
    fig.update_yaxes(gridcolor='#1a1a2e', row=i, col=1)

st.plotly_chart(fig, use_container_width=True)

# ── Statistics + Returns ───────────────────────────────────────
st.markdown("<div class='section-header'><p class='section-title'>📐 Statistical Analysis</p></div>", unsafe_allow_html=True)

col_a, col_b, col_c = st.columns(3)

with col_a:
    st.markdown("**📊 Price Statistics**")
    stats = {
        "Mean Price":    f"₹{df['Close'].mean():.2f}",
        "Median Price":  f"₹{df['Close'].median():.2f}",
        "Std Deviation": f"₹{df['Close'].std():.2f}",
        "Skewness":      f"{df['Close'].skew():.3f}",
        "Kurtosis":      f"{df['Close'].kurt():.3f}",
        "Max Drawdown":  f"{((df['Close']/df['Close'].cummax())-1).min()*100:.2f}%",
    }
    for k, v in stats.items():
        st.markdown(f"""<div class='pattern-card'>
        <span style='color:#8b8b8b;font-size:0.8rem;'>{k}</span>
        <span style='color:#e94560;font-weight:700;float:right;'>{v}</span></div>""",
        unsafe_allow_html=True)

with col_b:
    st.markdown("**📈 Return Analysis**")
    returns = {
        "Total Return":    f"{total_return:.2f}%",
        "Best Day":        f"{df['Daily_Return'].max():.2f}%",
        "Worst Day":       f"{df['Daily_Return'].min():.2f}%",
        "Avg Daily Return":f"{df['Daily_Return'].mean():.3f}%",
        "Positive Days":   f"{(df['Daily_Return']>0).sum()} ({(df['Daily_Return']>0).mean()*100:.1f}%)",
        "Sharpe Ratio":    f"{(df['Daily_Return'].mean()/df['Daily_Return'].std()*np.sqrt(252)):.2f}",
    }
    for k, v in returns.items():
        st.markdown(f"""<div class='pattern-card'>
        <span style='color:#8b8b8b;font-size:0.8rem;'>{k}</span>
        <span style='color:#20bf6b;font-weight:700;float:right;'>{v}</span></div>""",
        unsafe_allow_html=True)

with col_c:
    st.markdown("**🕯️ Pattern Detection**")
    patterns = {
        "Doji":              int(df['Doji'].sum()),
        "Hammer":            int(df['Hammer'].sum()),
        "Shooting Star":     int(df['Shooting_Star'].sum()),
        "Bullish Engulfing": int(df['Bullish_Engulfing'].sum()),
        "Bearish Engulfing": int(df['Bearish_Engulfing'].sum()),
        "Bullish Days":      int(df['Bullish'].sum()),
    }
    for k, v in patterns.items():
        st.markdown(f"""<div class='pattern-card'>
        <span style='color:#8b8b8b;font-size:0.8rem;'>{k}</span>
        <span style='color:#f7b731;font-weight:700;float:right;'>{v}</span></div>""",
        unsafe_allow_html=True)

# ── Distribution Charts ────────────────────────────────────────
st.markdown("<div class='section-header'><p class='section-title'>📉 Distribution Analysis</p></div>", unsafe_allow_html=True)

d1, d2, d3 = st.columns(3)

with d1:
    fig_ret = px.histogram(df['Daily_Return'].dropna(), nbins=60,
                           title="Daily Returns Distribution",
                           color_discrete_sequence=['#e94560'])
    fig_ret.update_layout(template='plotly_dark', paper_bgcolor='#0d1117',
                          plot_bgcolor='#0d1117', height=300, showlegend=False)
    st.plotly_chart(fig_ret, use_container_width=True)

with d2:
    fig_vol = px.line(df, x=df.index, y='Volatility',
                      title="Rolling 20-day Volatility",
                      color_discrete_sequence=['#f7b731'])
    fig_vol.update_layout(template='plotly_dark', paper_bgcolor='#0d1117',
                          plot_bgcolor='#0d1117', height=300, showlegend=False)
    st.plotly_chart(fig_vol, use_container_width=True)

with d3:
    fig_bb = px.line(df, x=df.index, y='BB_Width',
                     title="Bollinger Band Width",
                     color_discrete_sequence=['#a55eea'])
    fig_bb.update_layout(template='plotly_dark', paper_bgcolor='#0d1117',
                         plot_bgcolor='#0d1117', height=300, showlegend=False)
    st.plotly_chart(fig_bb, use_container_width=True)

# ── ATR Chart ──────────────────────────────────────────────────
if show_atr:
    st.markdown("<div class='section-header'><p class='section-title'>📏 Average True Range (ATR)</p></div>", unsafe_allow_html=True)
    fig_atr = px.area(df, x=df.index, y='ATR', title="ATR - Volatility Measure",
                      color_discrete_sequence=['#45aaf2'])
    fig_atr.update_layout(template='plotly_dark', paper_bgcolor='#0d1117',
                          plot_bgcolor='#0d1117', height=250)
    st.plotly_chart(fig_atr, use_container_width=True)

# ── Monthly Returns Heatmap ────────────────────────────────────
st.markdown("<div class='section-header'><p class='section-title'>🗓️ Monthly Returns Heatmap</p></div>", unsafe_allow_html=True)

df['Month'] = df.index.month
df['Year']  = df.index.year
monthly = df.groupby(['Year','Month'])['Daily_Return'].sum().unstack()
monthly.columns = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'][:len(monthly.columns)]

fig_heat = px.imshow(monthly, color_continuous_scale='RdYlGn',
                     title="Monthly Returns Heatmap (%)",
                     aspect='auto')
fig_heat.update_layout(template='plotly_dark', paper_bgcolor='#0d1117',
                       plot_bgcolor='#0d1117', height=300)
st.plotly_chart(fig_heat, use_container_width=True)

# ── Volume Analysis ────────────────────────────────────────────
st.markdown("<div class='section-header'><p class='section-title'>📦 Volume Analysis</p></div>", unsafe_allow_html=True)

v1, v2 = st.columns(2)

with v1:
    df['Vol_MA20'] = df['Volume'].rolling(20).mean()
    fig_v = go.Figure()
    fig_v.add_trace(go.Bar(x=df.index, y=df['Volume'], name='Volume',
                           marker_color=colors_vol, opacity=0.6))
    fig_v.add_trace(go.Scatter(x=df.index, y=df['Vol_MA20'], name='Vol MA20',
                               line=dict(color='#f7b731', width=2)))
    fig_v.update_layout(template='plotly_dark', paper_bgcolor='#0d1117',
                        plot_bgcolor='#0d1117', height=300, title="Volume with Moving Average")
    st.plotly_chart(fig_v, use_container_width=True)

with v2:
    monthly_vol = df.groupby('Month')['Volume'].mean() / 1e6
    fig_mv = px.bar(x=monthly_vol.index, y=monthly_vol.values,
                    title="Average Monthly Volume (Millions)",
                    color=monthly_vol.values, color_continuous_scale='Reds')
    fig_mv.update_layout(template='plotly_dark', paper_bgcolor='#0d1117',
                         plot_bgcolor='#0d1117', height=300, showlegend=False)
    st.plotly_chart(fig_mv, use_container_width=True)

# ── Raw Data Table ─────────────────────────────────────────────
st.markdown("<div class='section-header'><p class='section-title'>📋 Raw Data Explorer</p></div>", unsafe_allow_html=True)

show_cols = st.multiselect("Select columns to display",
    options=['Open','High','Low','Close','Volume','RSI','MACD','BB_Upper','BB_Lower',
             'SMA_200','EMA_20','ATR','Volatility','Daily_Return','VWAP'],
    default=['Open','High','Low','Close','Volume','RSI','MACD'])

n_rows = st.slider("Number of rows to display", 10, 100, 30)
st.dataframe(df[show_cols].tail(n_rows).round(2).sort_index(ascending=False),
             use_container_width=True)

# ── Footer ─────────────────────────────────────────────────────
st.markdown("""
<div class='footer'>
    <p>📈 <strong style='color:#e94560;'>HDFC Bank Price Action Dashboard</strong> &nbsp;|&nbsp;
    Built with Python, Streamlit & Plotly &nbsp;|&nbsp;
    Data: NSE via Yahoo Finance &nbsp;|&nbsp;
    ⚠️ For educational purposes only — not financial advice</p>
</div>
""", unsafe_allow_html=True)
