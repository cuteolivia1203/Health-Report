import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# 1. 介面風格 (維持大字體)
st.markdown("""
    <style>
    .lcd-screen { background-color: #E0F2F1; padding: 20px; border-radius: 15px; border: 3px solid #333; text-align: center; }
    .big-value { font-size: 90px !important; font-weight: bold; color: #1a1a1a; line-height: 1.1; }
    .label-text { font-size: 25px !important; color: #555; }
    .stButton>button { height: 100px; width: 100%; font-size: 30px !important; background-color: #ff4b4b; color: white; border-radius: 20px; }
    </style>
    """, unsafe_allow_html=True)

# 2. 建立連線並「強制不使用快取」
conn = st.connection("gsheets", type=GSheetsConnection)

# 核心修正：使用 ttl=0 確保每次網頁重新整理都會抓取 Google Sheets 最新狀態
df = conn.read(worksheet="Sheet1", ttl=0)

with st.sidebar:
    user_mode = st.radio("目前使用者：", ["爸爸", "我 (管理員)"])

if user_mode == "爸爸":
    st.markdown("### 👋 爸爸早安！")
    
    if not df.empty:
        # 篩選最新的一筆資料
        last_row = df.iloc[-1]
        
        st.markdown('<div class="lcd-screen">', unsafe_allow_html=True)
        st.markdown('<p class="label-text">最新量測結果 (SYS/DIA)</p>', unsafe_allow_html=True)
        # 顯示最後一列的數值
        st.markdown(f'<p class="big-value">{int(last_row["收縮壓 (SYS)"])} / {int(last_row["舒張壓 (DIA)"])}</p>', unsafe_allow_html=True)
        st.markdown(f'<p class="label-text">❤️ 心率: {int(last_row["心率"])}</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.write("---")
    
    with st.form("input_form", clear_on_submit=True):
        st.write("#### 📝 存入新量測紀錄")
        sys = st.number_input("收縮壓 (SYS)", 80, 200, 120)
        dia = st.number_input("舒張壓 (DIA)", 40, 120, 80)
        hr = st.number_input("心率", 40, 150, 75)
        
        if st.form_submit_button("🔴 點我儲存紀錄"):
            new_data = pd.DataFrame([{
                "紀錄時間": pd.Timestamp.now(tz='Asia/Taipei').strftime('%Y/%m/%d %H:%M'),
                "紀錄者": "爸爸",
                "類型 (血壓 / 血糖 / 吃藥)": "血壓",
                "收縮壓 (SYS)": sys,
                "舒張壓 (DIA)": dia,
                "心率": hr,
                "血糖值": 0,
                "備註": "App輸入"
            }])
            
            # 合併並更新到 Google Sheets
            updated_df = pd.concat([df, new_data], ignore_index=True)
            conn.update(worksheet="Sheet1", data=updated_df)
            
            st.balloons()
            st.success("資料已儲存！大數字即將更新...")
            # 強制 App 重新跑一遍，大數字就會立刻抓到剛存進去的資料
            st.rerun()

else:
    st.title("子女監控")
    st.dataframe(df)
