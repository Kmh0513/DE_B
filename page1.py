from matplotlib import font_manager, rc
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import requests
from datetime import datetime

font_path = 'NanumGothic-Regular.ttf'
font_manager.fontManager.addfont(font_path)
rc('font', family='NanumGothic')

# FastAPI URL
API_URL = "http://127.0.0.1:8000"

# GET 최신 생산 데이터
def get_production_data():
    response = requests.get(f"{API_URL}/productions/")
    if response.status_code == 200:
        return pd.DataFrame(response.json())
    else:
        st.error("백엔드에서 데이터를 가져오는 데 실패했습니다.")
        return pd.DataFrame()

def get_inventories_data():
    response = requests.get(f"{API_URL}/inventories/")
    if response.status_code == 200:
        return pd.DataFrame(response.json())
    else:
        st.error("백엔드에서 데이터를 가져오는 데 실패했습니다.")
        return pd.DataFrame()

def get_plan_list():
    response = requests.get(f"{API_URL}/plans/all")
    if response.status_code == 200:
        return pd.DataFrame(response.json())
    else:
        st.error("전체 생산 계획 리스트를 가져오는 데 실패했습니다.")
        return pd.DataFrame()

# GET 전체 생산 계획
def get_all_plans(year: int, month: int):
    response = requests.get(f"{API_URL}/plans/?year={year}&month={month}")
    if response.status_code == 200:
        data = response.json()
        if isinstance(data, dict):
            data = [data]  # 단일 객체를 리스트로 변환
        return pd.DataFrame(data)
    else:
        st.error("생산 계획을 가져오는 데 실패했습니다.")
        return pd.DataFrame()

# POST 생산 계획 저장
def create_production_plan(data):
    response = requests.post(f"{API_URL}/plans/", json=data)
    if response.status_code == 200:
        st.success("생산 계획이 성공적으로 저장되었습니다!")
    else:
        st.error("생산 계획 저장에 실패했습니다.")

def page1_view():
    st.title("생산 계획 관리")
    tab = st.sidebar.selectbox("생산 계획 관리", ["생산 계획 조회", "생산 계획 등록/수정"])

    # 1. 생산 계획 조회 페이지
    if tab == "생산 계획 조회":
        # 생산 데이터
        st.subheader("생산 계획")
        df_plans_list = get_plan_list()
        if not df_plans_list.empty:
            st.dataframe(df_plans_list, use_container_width=True)
        else:
            st.warning("생산 계획이 없습니다.")

        # 월별 생산 계획 및 실적 조회
        st.subheader("월별 생산 계획 및 실적")
        year = st.selectbox("년도 선택", options=list(range(2014, 2100)), index=10)
        month = st.selectbox("월 선택", options=list(range(1, 13)))
        
        df_plans = get_all_plans(year, month)
        if not df_plans.empty:
            columns_to_display = [
                "year", "month", "total_plan_quantity", "total_business_plan", "total_production_quantity",
                "total_business_actual", "production_achievement_rate", "business_achievement_rate",
            ]

            # 데이터 가공
            st.write("계획 및 실적 데이터")
            df_display = df_plans[columns_to_display]
            st.table(df_display)
            
            # 그래프
            st.subheader(f"{month}월 달성률 차트")

            # 사업 달성률과 나머지 비율 계산
            business_achievement_rate = df_plans["business_achievement_rate"].values[0]
            production_achievement_rate = df_plans["production_achievement_rate"].values[0]
             
            fig, ax = plt.subplots(figsize=(6, 4))

# 막대그래프에 데이터 추가
            categories = ['사업 달성률', '생산 달성률']
            values = [business_achievement_rate, production_achievement_rate]

            ax.bar(categories, values, color=['#ff9999', '#66b3ff'])

            # 그래프에 텍스트와 제목 추가
            ax.set_ylim(0, 100)  # y축 범위 0~100
            ax.set_ylabel('달성률 (%)')
            ax.set_title('사업 및 생산 달성률')

            # 스트림릿에 그래프 출력
            st.pyplot(fig)
        else:
            st.warning("계획 데이터가 없습니다.")

    # 2. 생산 계획 등록/수정 페이지
    elif tab == "생산 계획 등록/수정":
        st.subheader("생산 계획 등록/수정")

        new_item_name = st.text_input("품명 입력")
        col1, col2 = st.columns([1, 1])
        with col1:
            new_year = st.selectbox("년도 선택", options=list(range(2014, 2100)), index=10)
        with col2:
            new_month = st.selectbox("월 선택", options=list(range(1, 13)))
        new_plan_quantity = st.number_input("계획 수량", min_value=0)

        if st.button("저장"):
            new_data = {
                "year": new_year,
                "month": new_month,
                "item_name": new_item_name,
                "plan_quantity": new_plan_quantity
            }
            create_production_plan(new_data)
        st.subheader("생산 데이터")
        df_production = get_production_data()
        if not df_production.empty:
            st.write(df_production)
        else:
            st.warning("생산 데이터가 없습니다.")

        st.subheader("재고 데이터")
        df_inventories = get_inventories_data()
        if not df_inventories.empty:
            st.write(df_inventories)
        else:
            st.warning("생산 데이터가 없습니다.")
if __name__ == "__main__":
    page1_view()
