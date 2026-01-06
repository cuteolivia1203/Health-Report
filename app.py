import streamlit as st

# --- 介面風格設定 (模仿血壓計大螢幕) ---
st.markdown("""
    <style>
    .lcd-screen {
        background-color: #E0F2F1;
        padding: 30px;
        border-radius: 20px;
        border: 5px solid #333;
        text-align: center;
        font-family: 'Courier New', Courier, monospace;
    }
    .big-value { font-size: 100px !important; font-weight: bold; color: #1a1a1a; line-height: 1; }
    .label-text { font-size: 30px !important; color: #555; }
    .stButton>button { height: 80px; width: 100%; font-size: 25px !important; background-color: #ff4b4b; color: white; border-radius: 15px; }
    </style>
    """, unsafe_allow_html=True)

# --- 側邊欄隱私切換 ---
with st.sidebar:
    st.title("身分切換")
    user_mode = st.radio("目前使用者：", ["爸爸", "我 (管理員)"])

if user_mode == "爸爸":
    st.markdown("### 👋 爸爸早安！記得量血壓喔")
    
    # 模仿截圖的大數字顯示區
    st.markdown('<div class="lcd-screen">', unsafe_allow_html=True)
    st.markdown('<p class="label-text">SYS / DIA</p>', unsafe_allow_html=True)
    st.markdown('<p class="big-value">112 / 75</p>', unsafe_allow_html=True)
    st.markdown('<p class="label-text">❤️ 心率: 78</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.write("---")
    
    # 輸入區
    col1, col2 = st.columns(2)
    with col1:
        sys = st.number_input("高壓 (SYS)", 80, 200, 120, step=1)
    with col2:
        dia = st.number_input("低壓 (DIA)", 40, 120, 80, step=1)
    
    if st.button("🔴 點我儲存紀錄"):
        st.balloons()
        st.success("紀錄成功！數字很大，看得很清楚吧！")

else:
    st.title("我的管理後台")
    st.info("這裡之後可以串接 Google 試算表，讓您即時監測爸爸的狀況。")
    st.write("您的血壓紀錄區...")
    # 您自己的簡單輸入區...
