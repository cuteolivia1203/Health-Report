import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# --- 介面風格設定 (模仿血壓計大螢幕) ---
st.markdown("""
    <style>
    .lcd-screen { background-color: #E0F2F1; padding: 20px; border-radius: 15px; border: 3px solid #333; text-align: center; }
    .big-value { font-size: 90px !important; font-weight: bold; color: #1a1a1a; line-height: 1; }
    .label-text { font-size: 25px !important; color: #555; }
    .stButton>button { height: 100px; width: 100%; font-size: 30px !important; background-color: #ff4b4b; color: white; border-radius: 20px; }
    </style>
    """, unsafe_allow_html=True)

# 建立與 Google 試算表的連線
conn = st.connection("gsheets", type=GSheetsConnection)

# 讀取現有資料 (worksheet 指向您的分頁名稱)
df = conn.read(worksheet="紀錄清單", ttl="0s")

# 側邊欄切換
with st.sidebar:
    st.title("身分切換")
    user_mode = st.sidebar.radio("目前使用者：", ["爸爸", "我 (管理員)"])

if user_mode == "爸爸":
    st.markdown("### 👋 爸爸早安！記得量血壓喔")
    
    # 1. 顯示最新一筆紀錄 (從您指定的欄位讀取)
    if not df.empty:
        # 過濾出紀錄者為爸爸的最新資料
        papa_data = df[df['紀錄者'] == '爸爸']
        if not papa_data.empty:
            last_row = papa_data.iloc[-1]
            st.markdown('<div class="lcd-screen">', unsafe_allow_html=True)
            st.markdown('<p class="label-text">上次量測結果 (SYS/DIA)</p>', unsafe_allow_html=True)
            st.markdown(f'<p class="big-value">{int(last_row["收縮壓 (SYS)"])} / {int(last_row["舒張壓 (DIA)"])}</p>', unsafe_allow_html=True)
            st.markdown(f'<p class="label-text">❤️ 心率: {int(last_row["心率"])}</p>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
    
    st.write("---")
    
    # 2. 資料輸入區 (對應您截圖的欄位)
    with st.form("input_form"):
        st.write("#### 📝 輸入新紀錄")
        sys = st.number_input("收縮壓 (SYS)", 80, 200, 120)
        dia = st.number_input("舒張壓 (DIA)", 40, 120, 80)
        pulse = st.number_input("心率", 40, 150, 75)
        note = st.selectbox("備註", ["無", "吃藥了", "剛運動完", "剛睡醒"])
        
        submit = st.form_submit_button("🔴 點我儲存紀錄")
        
        if submit:
            # 建立符合您試算表欄位的新資料
            new_entry = pd.DataFrame([{
                "紀錄時間": pd.Timestamp.now().strftime('%Y/%m/%d %H:%M'),
                "紀錄者": "爸爸",
                "類型 (血壓 / 血糖 / 吃藥)": "血壓",
                "收縮壓 (SYS)": sys,
                "舒張壓 (DIA)": dia,
                "心率": pulse,
                "血糖值": 0,
                "備註": note
            }])
            
            # 將新資料推送到 Google 試算表
            updated_df = pd.concat([df, new_entry], ignore_index=True)
            conn.update(worksheet="紀錄清單", data=updated_df)
            
            st.balloons()
            st.success("存檔成功！資料已同步到雲端。")
            st.info("提示：畫面將在存檔後自動更新。")

else:
    st.title("子女監控模式")
    st.write("這是「紀錄清單」的完整內容：")
    st.dataframe(df)
