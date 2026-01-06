import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# --- 介面風格設定 ---
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

# 讀取資料 (改為 Sheet1，並完全停用快取)
df = conn.read(worksheet="Sheet1", ttl=0)

with st.sidebar:
    user_mode = st.radio("目前使用者：", ["爸爸", "我 (管理員)"])

if user_mode == "爸爸":
    st.markdown("### 👋 爸爸早安！紀錄完會噴氣球喔")
    
    # 顯示最新紀錄
    if not df.empty:
        papa_data = df[df['紀錄者'] == '爸爸']
        if not papa_data.empty:
            last_row = papa_data.iloc[-1]
            st.markdown('<div class="lcd-screen">', unsafe_allow_html=True)
            st.markdown('<p class="label-text">上次量測結果 (SYS/DIA)</p>', unsafe_allow_html=True)
            st.markdown(f'<p class="big-value">{int(last_row["收縮壓 (SYS)"])} / {int(last_row["舒張壓 (DIA)"])}</p>', unsafe_allow_html=True)
            st.markdown(f'<p class="label-text">❤️ 心率: {int(last_row["心率"])}</p>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
    
    st.write("---")
    
    # 表單輸入
    with st.form("my_form", clear_on_submit=True):
        sys = st.number_input("收縮壓 (SYS)", 80, 200, 120)
        dia = st.number_input("舒張壓 (DIA)", 40, 120, 80)
        pulse = st.number_input("心率", 40, 150, 75)
        
        if st.form_submit_button("🔴 點我儲存紀錄"):
            # 建立新列 (欄位名稱必須與您的 image_feb79d.png 完全一致)
            new_row = pd.DataFrame([{
                "紀錄時間": pd.Timestamp.now(tz='Asia/Taipei').strftime('%Y/%m/%d %H:%M'),
                "紀錄者": "爸爸",
                "類型 (血壓 / 血糖 / 吃藥)": "血壓",
                "收縮壓 (SYS)": sys,
                "舒張壓 (DIA)": dia,
                "心率": pulse,
                "血糖值": 0,
                "備註": "App輸入"
            }])
            
            # 核心：合併舊資料與新資料，並整份推回 Sheet1
            updated_df = pd.concat([df, new_row], ignore_index=True)
            conn.update(worksheet="Sheet1", data=updated_df)
            
            st.balloons()
            st.success("存檔成功！正在同步到 Google 試算表...")
            st.rerun() # 強制重新整理以顯示最新數值

else:
    st.title("子女監控模式")
    st.write("您的紀錄區（爸爸看不到這裡）：")
    # 此處可增加您的個人紀錄代碼
    st.dataframe(df)
