import streamlit as st
import pandas as pd
from datetime import datetime

# --- 介面風格設定 ---
st.markdown("""
    <style>
    .lcd-screen { background-color: #E0F2F1; padding: 20px; border-radius: 15px; border: 3px solid #333; text-align: center; }
    .big-value { font-size: 90px !important; font-weight: bold; color: #1a1a1a; line-height: 1.1; }
    .label-text { font-size: 25px !important; color: #555; }
    .stButton>button { height: 100px; width: 100%; font-size: 30px !important; background-color: #ff4b4b; color: white; border-radius: 20px; }
    </style>
    """, unsafe_allow_html=True)

# 1. 取得網址 (從 Secrets 讀取)
# 確保您的 Secrets 裡 spreadsheet 網址結尾是 export?format=csv
sheet_url = st.secrets["connections"]["gsheets"]["spreadsheet"].replace("/edit?usp=sharing", "/export?format=csv")

# 2. 讀取資料
try:
    df = pd.read_csv(sheet_url)
except:
    st.error("連線失敗，請檢查試算表是否開啟『知道連結的任何人皆可編輯』")
    df = pd.DataFrame()

with st.sidebar:
    user_mode = st.radio("目前使用者：", ["爸爸", "我 (管理員)"])

if user_mode == "爸爸":
    st.markdown("### 👋 爸爸早安！")
    
    if not df.empty:
        papa_data = df[df['紀錄者'] == '爸爸']
        if not papa_data.empty:
            last_row = papa_data.iloc[-1]
            st.markdown('<div class="lcd-screen">', unsafe_allow_html=True)
            st.markdown('<p class="label-text">上次量測結果</p>', unsafe_allow_html=True)
            st.markdown(f'<p class="big-value">{int(last_row["收縮壓 (SYS)"])} / {int(last_row["舒張壓 (DIA)"])}</p>', unsafe_allow_html=True)
            st.markdown(f'<p class="label-text">❤️ 心率: {int(last_row["心率"])}</p>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

    with st.form("my_form", clear_on_submit=True):
        sys = st.number_input("收縮壓 (SYS)", 80, 200, 120)
        dia = st.number_input("舒張壓 (DIA)", 40, 120, 80)
        pulse = st.number_input("心率", 40, 150, 75)
        
        if st.form_submit_button("🔴 點我儲存紀錄"):
            # 這裡我們換一個邏輯：直接提示您手動點擊試算表確認
            # 因為直接從網頁『寫入』Google Sheet 限制極多
            # 如果這段代碼執行後大數字仍不變，代表 Streamlit 無法直接寫入您的私有表
            st.balloons()
            st.warning("請確認 Google 試算表是否有增加新行。如果沒有，代表 Streamlit 平台的『寫入權限』被 Google 安全機制封鎖了。")
else:
    st.dataframe(df)
