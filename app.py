import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd 
from datetime import datetime

# 1. App 設定
st.set_page_config(page_title="辦桌訂單系統", page_icon="🏮")
st.title("🏮 辦桌訂單管理系統")
st.subheader("醫工級精準記帳與備料同步")

# 2. 建立 Google Sheets 連線
url = "https://docs.google.com/spreadsheets/d/1QWAnwlDuyqRpWesfEFGm0Du6G6CrFcSCuFt6sNw-1dw/edit#gid=0"

# 建立連線，設定 ttl=0 代表不使用緩存，確保每次都讀到最新資料
conn = st.connection("gsheets", type=GSheetsConnection)

# 3. 整合式輸入表單
with st.form("main_order_form"):
    st.write("### 📝 新增訂單資料")
    customer = st.text_input("客戶姓名")
    tables = st.number_input("預訂桌數", min_value=1, value=10)
    price = st.number_input("每桌單價 (元)", min_value=0, value=12000)
    
    # 提交按鈕
    submitted = st.form_submit_button("送出訂單並計算備料")

# 4. 按下按鈕後的邏輯處理
if submitted:
    # A. 計算邏輯
    total_amount = tables * price
    pork_needed = tables * 1.5  
    shrimp_needed = tables * 12 
    
    # B. 顯示即時結果
    st.success(f"✅ 訂單已產出：{customer}")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("總金額", f"${total_amount:,}")
    with col2:
        st.metric("豬肉需求", f"{pork_needed} 斤")
    with col3:
        st.metric("蝦子需求", f"{shrimp_needed} 隻")

    # C. 同步至 Google Sheets
    try:
        # 準備新資料
        new_order = pd.DataFrame([{
            "客戶姓名": customer,
            "預訂桌數": tables,
            "每桌單價": price,
            "總金額": total_amount,
            "豬肉需求": pork_needed,
            "訂單時間": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }])

        # 讀取現有資料 (如果表單是空的，會回傳空 DataFrame)
        existing_data = conn.read(spreadsheet=url)
        
        # 合併資料
        updated_data = pd.concat([existing_data, new_order], ignore_index=True)

        # 更新回雲端
        conn.update(spreadsheet=url, data=updated_data)
        st.balloons() # 成功後的慶祝動畫
        st.info("💡 資料已同步至 Google Sheet，家人可即時查看。")
    except Exception as e:
        st.error(f"同步失敗，請檢查 Google Sheet 權限設定。錯誤訊息: {e}")

# 5. (選用) 顯示目前已存檔的訂單
if st.checkbox("查看雲端現有訂單"):
    data = conn.read(spreadsheet=url)
    st.dataframe(data)
