import streamlit as st
import yfinance as yf  # 追加

st.title("Trade Nexus Risk Analyzer")

# 1. ドル円のシンボルを定義
ticker = "JPY=X"

# 2. データをダウンロード (期間: 1ヶ月)
df = yf.download(ticker, period="1y")

# 【追加】データの「生の状態」を画面に出して確認する！
st.write("▼ 修正前のデータヘッダー：", df.head())

df.columns = df.columns.droplevel(1)

# 20日移動平均線(SMA)を計算
df['SMA_20'] = df['Close'].rolling(window=20).mean()

# 計算結果を画面に表示して確認
st.write("直近5日間のデータ：", df.tail(5))

# 3. 終値(Close)だけを取り出してグラフ化
st.line_chart(df[["Close", "SMA_20"]])