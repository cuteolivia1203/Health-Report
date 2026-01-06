import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# 介面風格
st.markdown("""
    <style>
    .lcd-screen { background-color: #E0F2F1; padding: 20px; border-radius: 15px; border: 3px solid #333; text-align: center; }
    .big-value { font-size: 90px !important; font-weight: bold; color: #1a1a1a; line-height: 1.1; }
    .label-text { font-size: 25px !important; color: #555; }
    .stButton>button { height: 100px; width: 100%; font-size: 30px !important; background-color: #ff4b4b; color: white; border-radius: 20px; }
    </style>
    """, unsafe_allow_html=True)

# 建立連線
conn = st.connection("gsheets", type=GSheetsConnection)

# 讀取資料 (強制不使用快取)
df = conn.read(worksheet="紀錄清單", ttl=0)

with st.sidebar:
    user_mode = st.radio("目前使用者：", ["爸爸", "我 (管理員)"])

if user_mode == "爸爸":
    st.markdown("### 👋 爸爸早安！記得量血壓喔")
    
    if not df.empty:
        papa_data = df[df['紀錄者'] == '爸爸']
        if not papa_data.empty:
            last_row = papa_data.iloc[-1]
            st.markdown('<div class="lcd-screen">', unsafe_allow_html=True)
            st.markdown('<p class="label-text">上次量測結果 (SYS/DIA)</p>', unsafe_allow_html=True)
            # 確保數字顯示正確
            sys_val = last_row["收縮壓 (SYS)"]
            dia_val = last_row["舒張壓 (DIA)"]
            st.markdown(f'<p class="big-value">{int(sys_val)} / {int(dia_val)}</p>', unsafe_allow_html=True)
            st.markdown(f'<p class="label-text">❤️ 心率: {int(last_row["心率"])}</p>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
    
    st.write("---")
    
    with st.form("input_form", clear_on_submit=True):
        st.write("#### 📝 輸入新紀錄")
        new_sys = st.number_input("收縮壓 (SYS)", 80, 200, 120)
        new_dia = st.number_input("舒張壓 (DIA)", 40, 120, 80)
        new_pulse = st.number_input("心率", 40, 150, 75)
        
        if st.form_submit_button("🔴 點我儲存紀錄"):
            new_entry = pd.DataFrame([{
                "紀錄時間": pd.Timestamp.now(tz='Asia/Taipei').strftime('%Y/%m/%d %H:%M'),
                "紀錄者": "爸爸",
                "類型 (血壓 / 血糖 / 吃藥)": "血壓",
                "收縮壓 (SYS)": new_sys,
                "舒張壓 (DIA)": new_dia,
                "心率": new_pulse,
                "血糖值": 0,
                "備註": "App輸入"
            }])
            
            # 執行更新
            updated_df = pd.concat([df, new_entry], ignore_index=True)
            conn.update(worksheet="紀錄清單", data=updated_df)
            st.cache_data.clear() # 強制清除快取
            st.balloons()
            st.success("存檔成功！請稍等頁面自動跳轉。")
            st.rerun() # 立即重新整理畫面

else:
    st.title("子女監控模式")
    st.dataframe(df)
