import streamlit as st
import pandas as pd 

# 1. App 標題與介面設定
st.title("🏮 辦桌訂單管理系統")
st.subheader("醫工級精準記帳與備料")

# 2. 輸入區域：讓家人在手機上填寫
with st.form("order_form"):
    customer = st.text_input("客戶姓名")
    tables = st.number_input("預訂桌數", min_value=1, value=10)
    price = st.number_input("每桌單價 (元)", min_value=0, value=12000)
    submitted = st.form_submit_button("產生訂單報告")

# 3. 邏輯運算：自動化備料與財務計算
if submitted:
    total_amount = tables * price
    pork_needed = tables * 1.5  # 假設每桌 1.5 斤
    shrimp_needed = tables * 12 # 假設每桌 12 隻
    
    # 4. 顯示結果
    st.success(f"✅ 訂單已產出：{customer}")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("總金額", f"${total_amount:,}")
    with col2:
        st.metric("豬肉需求", f"{pork_needed} 斤")
    
    st.info(f"🦐 蝦子採購量：{shrimp_needed} 隻")
