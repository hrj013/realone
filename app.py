import streamlit as st

from carbon import calculate_transport_carbon


# -------------------------
# 페이지 설정
# -------------------------

st.set_page_config(
    page_title="Carbon Quest",
    page_icon="🌱",
    layout="centered",
)


# -------------------------
# 제목
# -------------------------

st.title("🌱 Carbon Quest")

st.write(
    "오늘의 생활을 기록하고 "
    "탄소를 조금씩 줄여보세요!"
)


st.divider()


# -------------------------
# 이동 기록
# -------------------------

st.header("🚗 오늘의 이동")


car_minutes = st.slider(
    "🚗 자동차",
    min_value=0,
    max_value=180,
    value=30,
    step=5,
)

bus_minutes = st.slider(
    "🚌 버스",
    min_value=0,
    max_value=180,
    value=20,
    step=5,
)

subway_minutes = st.slider(
    "🚇 지하철",
    min_value=0,
    max_value=180,
    value=30,
    step=5,
)


st.divider()


# -------------------------
# 탄소 계산
# -------------------------

carbon = calculate_transport_carbon(
    car_minutes,
    bus_minutes,
    subway_minutes,
)


st.header("🌍 오늘의 예상 탄소")


st.metric(
    label="탄소배출량",
    value=f"{carbon:.2f} kg CO₂e",
)


# -------------------------
# 상세 정보
# -------------------------

with st.expander("🔎 계산 과정 보기"):

    st.write(f"🚗 자동차: {car_minutes}분")
    st.write(f"🚌 버스: {bus_minutes}분")
    st.write(f"🚇 지하철: {subway_minutes}분")

    st.write(
        f"총 예상 배출량: "
        f"**{carbon:.2f} kg CO₂e**"
    )
