import streamlit as st
import yfinance as yf  # 追加

st.title("Trade Nexus Risk Analyzer")

# 1. ドル円のシンボルを定義
ticker = "JPY=X"

# 2. データをダウンロード (期間: 1ヶ月)
data = yf.download(ticker, period="1mo")

# 3. 終値(Close)だけを取り出してグラフ化
st.line_chart(data["Close"])