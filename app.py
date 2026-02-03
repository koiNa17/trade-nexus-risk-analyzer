import streamlit as st
import yfinance as yf
import plotly.graph_objects as go

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

# --- Plotly (go) でプロ仕様のグラフを描く ---

# 1. 空っぽのキャンバス(fig)を用意
fig = go.Figure()

# 2. ローソク足 (Candlestick) を描く
fig.add_trace(go.Candlestick(
    x=df.index,
    open=df['Open'],
    high=df['High'],
    low=df['Low'],
    close=df['Close'],
    name="ローソク足"
))

# 3. 移動平均線 (SMA_20) の線を描き込む
fig.add_trace(go.Scatter(x=df.index, y=df['SMA_20'], name="20日SMA"))

# 4. 完成したグラフをStreamlitに貼り付ける
st.plotly_chart(fig)