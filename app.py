import streamlit as st
import yfinance as yf

st.title("Trade-Nexus Risk Analyzer")
st.write("金融データ分析ダッシュボード")

st.subheader("USD/JPY(ドル円)過去1か月のデータ")
ticker = yf.Ticker("JPY=X")
data = ticker.history(period="1mo")
st.write(data)

st.subheader("USD/JPY 終値の推移")
st.line_chart(data['Close'])