import streamlit as st
import yfinance as yf

st.title("Trade-Nexus Risk Analyzer")
st.write("金融データ分析ダッシュボード")

st.subheader("USD/JPY(ドル円)過去1か月のデータ")
tickers = {'ドル円': 'JPY=X', 'ユーロ円': 'EURJPY=X', '日経平均': '^N225'}
name = st.selectbox("分析対象を選択してください：", list(tickers.keys()))
periods = {'1か月': '1mo', '半年': '6mo', '1年': '1y'}
p_name = st.selectbox("期間を選択してください：", list(periods.keys()))
data = yf.Ticker(tickers[name]).history(period=periods[p_name])

# data = yf.Ticker(tickers[name]).history(period="1mo")

st.subheader(f"{name} のデータと推移")
st.write(data)
st.line_chart(data['Close'])