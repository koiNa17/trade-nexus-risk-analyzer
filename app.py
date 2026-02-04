import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# --- 関数定義セクション ---
def calculate_rsi(data, window=14):
    """RSIを計算する関数"""
    delta = data['Close'].diff()  # 前日との差
    
    # 上昇幅と下落幅に分ける
    gain = (delta.where(delta > 0, 0)).fillna(0)
    loss = (-delta.where(delta < 0, 0)).fillna(0)
    
    # 指数平滑移動平均 (EMA) で計算
    avg_gain = gain.rolling(window=window).mean()
    avg_loss = loss.rolling(window=window).mean()
    
    # RS (相対強度) を計算
    rs = avg_gain / avg_loss
    
    # RSI (0〜100) に変換
    rsi = 100 - (100 / (1 + rs)) 
    
    return rsi

st.title("Trade Nexus Risk Analyzer")

# サイドバーに入力ボックスを作成 (初期値は "JPY=X")
ticker = st.sidebar.text_input("銘柄コードを入力：", "JPY=X")

st.write(f"現在表示中の銘柄： {ticker}") # 確認用に表示

# サイドバーで期間を選択 (ドロップダウンリストを作成)
period_days = st.sidebar.selectbox("期間を選択：", ['1mo', '3mo', '6mo', '1y', '5y', 'max'])

# 選択された期間(period_days)を使ってデータを取得
df = yf.download(ticker, period=period_days)

# 【追加】データの「生の状態」を画面に出して確認する！
st.write("▼ 修正前のデータヘッダー：", df.head())

df.columns = df.columns.droplevel(1)

# 最新のデータ(一番下の行)と、その前日のデータを取得
latest_close = df['Close'].iloc[-1]
prev_close = df['Close'].iloc[-2]

# 前日比を計算
delta = latest_close - prev_close

# 画面に見やすく表示 (st.metric)
# f"{数値:.2f}" は「小数第2位まで表示する」という整形テクニックです
st.metric(label="現在の終値", value=f"{latest_close:.2f} 円", delta=f"{delta:.2f} 円")

# 20日移動平均線(SMA)を計算
df['SMA_20'] = df['Close'].rolling(window=20).mean()

# 計算結果を画面に表示して確認
st.write("直近5日間のデータ：", df.tail(5))

# --- データ取得・加工セクションの末尾に追加 ---
# さっき作った関数でRSIを計算し、新しい列 'RSI' に入れる
df['RSI'] = calculate_rsi(df)

# 【確認用】 ちゃんと計算できたか、画面に数字を出してみる
current_rsi = df['RSI'].iloc[-1]
st.metric(label="現在のRSI(強弱感)", value=f"{current_rsi:.2f}")

# --- Plotly (go) でプロ仕様のグラフを描く ---
# 1. 空っぽのキャンバス(fig)を用意
# fig = go.Figure()

# 2段組みのグラフ領域を作成（上がメイン、下がRSI）
fig = make_subplots(
    rows=2, cols=1,
    shared_xaxes=True,
    vertical_spacing=0.05,
    row_heights=[0.7, 0.3]
)

# 2. ローソク足 (Candlestick) を描く
fig.add_trace(go.Candlestick(
    x=df.index,
    open=df['Open'],
    high=df['High'],
    low=df['Low'],
    close=df['Close'],
    name="OHLC"
), row=1, col=1)

# RSI (折れ線) を下段に追加
fig.add_trace(go.Scatter(
    x=df.index, y=df['RSI'], name='RSI',
    line=dict(color='purple', width=2),
    connectgaps=True
), row=2, col=1)

# 基準線 (70と30) を引く
fig.add_hline(y=70, line_dash="dot", row=2, col=1, line_color="red")
fig.add_hline(y=30, line_dash="dot", row=2, col=1, line_color="green")


# 3. 移動平均線 (SMA_20) の線を描き込む
fig.add_trace(go.Scatter(
    x=df.index, y=df['SMA_20'], name="20日SMA"
    ), row=1, col=1)

# --- レイアウトの調整 ---
fig.update_layout(
    height=800,  # 画面を少し縦長にして見やすくする
    showlegend=False, # 凡例が邪魔なら消す（お好みでTrueでも可）
    xaxis_rangeslider_visible=False  # <--- 【重要】元凶のスライダーを消す！
)


# 4. 完成したグラフをStreamlitに貼り付ける
st.plotly_chart(fig, use_container_width=True) # 幅を画面いっぱいに広げる