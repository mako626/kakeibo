import streamlit as st
import pandas as pd
from datetime import datetime

# ページ基本設定
st.set_page_config(page_title="シンプル家計簿", layout="centered")

st.title("📱 シンプル家計簿")

# データ保存用の初期化
if "expenses" not in st.session_state:
    st.session_state.expenses = pd.DataFrame(
        columns=["日付", "カテゴリ", "項目", "金額(円)", "メモ"]
    )

# 項目設定（ご希望のカテゴリ）
CATEGORIES = {
    "日々の支出": ["食事代", "その他"],
    "固定費": ["家賃", "電気", "ガス", "水道", "携帯"],
    "車関連": ["車の支払い（1台目）", "車の支払い（2台目）", "車の保険"],
    "カード払い": [f"カード払い {i}" for i in range(1, 7)],
    "投資・積立": ["投資積立", "その他投資枠"],
}

# --- 入力フォーム ---
st.subheader("＋ 支出・投資の入力")

with st.form("entry_form", clear_on_submit=True):
    date = st.date_input("日付", datetime.now())
    
    cat_group = st.selectbox("分類", list(CATEGORIES.keys()))
    item = st.selectbox("項目", CATEGORIES[cat_group])
    
    amount = st.number_input("金額 (円)", min_value=0, step=100)
    note = st.text_input("メモ (任意)", "")
    
    submitted = st.form_submit_button("保存する")
    
    if submitted and amount > 0:
        new_data = pd.DataFrame([{
            "日付": date,
            "カテゴリ": cat_group,
            "項目": item,
            "金額(円)": amount,
            "メモ": note
        }])
        st.session_state.expenses = pd.concat([st.session_state.expenses, new_data], ignore_index=True)
        st.success(f"保存しました: {item} - {amount:,}円")

# --- 集計・確認画面 ---
st.subheader("📊 今月の集計・内訳")

if not st.session_state.expenses.empty:
    df = st.session_state.expenses
    
    total_amount = df["金額(円)"].sum()
    st.metric("総支出・投資合計", f"{total_amount:,} 円")
    
    st.write("▼ カテゴリ別内訳")
    summary = df.groupby("カテゴリ")["金額(円)"].sum().reset_index()
    st.dataframe(summary, use_container_width=True)
    
    with st.expander("📝 入力履歴を見る"):
        st.dataframe(df.sort_values(by="日付", ascending=False), use_container_width=True)
else:
    st.info("まだデータがありません。上のフォームから入力してください。")
