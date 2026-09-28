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

# -------------------------
# 게임 데이터
# -------------------------

if "xp" not in st.session_state:
    st.session_state.xp = 0

if "coins" not in st.session_state:
    st.session_state.coins = 0

if "previous_carbon" not in st.session_state:
    st.session_state.previous_carbon = None

if st.button("🌱 오늘 기록 저장"):

    if st.session_state.previous_carbon is None:

        st.session_state.previous_carbon = carbon

        st.session_state.xp += 10
        st.session_state.coins += 10

        st.success(
            "🎉 첫 기록 완료!\n\n"
            "+10 XP\n"
            "+10 🪙"
        )

    else:

        previous = st.session_state.previous_carbon

        reduction = previous - carbon

        if reduction > 0:

            xp = 30
            coins = 20

            st.session_state.xp += xp
            st.session_state.coins += coins

            st.balloons()

            st.success(
                f"🌱 탄소를 "
                f"{reduction:.2f} kg 줄였어요!\n\n"
                f"⭐ +{xp} XP\n"
                f"🪙 +{coins}"
            )

        else:

            st.info(
                "오늘도 기록 완료! "
                "내일 조금 더 줄여볼까요? 🌱"
            )

        st.session_state.previous_carbon = carbon

ITEMS = {
    "🌱 작은 화분": 20,
    "🌳 나무": 50,
    "🛋️ 소파": 100,
    "🖼️ 그림": 150,
}


st.divider()

st.header("🎮 나의 상태")

col1, col2 = st.columns(2)

with col1:
    st.metric("⭐ XP", st.session_state.xp)

with col2:
    st.metric("🪙 코인", st.session_state.coins)


st.header("🛒 아이템 상점")

for item, price in ITEMS.items():

    if st.button(f"{item} — {price} 🪙"):

        if st.session_state.coins >= price:

            st.session_state.coins -= price

            st.success(
                f"{item}을 구매했습니다!"
            )

        else:

            st.warning(
                "🪙 코인이 부족해요!"
            )
