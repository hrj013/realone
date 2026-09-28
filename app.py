import streamlit as st

from carbon import calculate_transport_carbon


# -----------------------------
# 기본 설정
# -----------------------------

st.set_page_config(
    page_title="CARBON RIDER",
    page_icon="🌱",
    layout="centered"
)


# -----------------------------
# 게임 데이터
# -----------------------------

if "xp" not in st.session_state:
    st.session_state.xp = 0

if "coins" not in st.session_state:
    st.session_state.coins = 0

if "previous_carbon" not in st.session_state:
    st.session_state.previous_carbon = None


# -----------------------------
# CSS
# -----------------------------

st.markdown("""
<style>

.stApp {
    background-color: #101018;
    color: white;
}

h1, h2, h3 {
    font-family: monospace;
}

.game-title {
    text-align: center;
    font-size: 38px;
    font-weight: bold;
    letter-spacing: 5px;
}

.game-subtitle {
    text-align: center;
    color: #777788;
    font-family: monospace;
}

.dialogue {
    background-color: #08080d;
    border: 3px solid white;
    padding: 20px;
    font-family: monospace;
    line-height: 1.8;
}

.speaker {
    color: #6cff8a;
    font-weight: bold;
}

</style>
""", unsafe_allow_html=True)


# -----------------------------
# 타이틀
# -----------------------------

st.markdown(
    '<div class="game-title">CARBON RIDER</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="game-subtitle">'
    'SEASON 01 — AUTUMN TRAIL'
    '</div>',
    unsafe_allow_html=True
)


st.write("")


# -----------------------------
# 캐릭터
# -----------------------------

st.image(
    "assets/rider.png",
    width=180
)


st.markdown(
    """
    <div class="dialogue">

    <div class="speaker">???</div>

    오늘도 길을 떠날 시간이야.<br>
    <br>
    네가 선택하는 이동이<br>
    이 세계의 내일을 바꾼다.

    </div>
    """,
    unsafe_allow_html=True
)


# -----------------------------
# 플레이어 정보
# -----------------------------

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("LEVEL", "01")

with col2:
    st.metric(
        "EXP",
        st.session_state.xp
    )

with col3:
    st.metric(
        "COIN",
        st.session_state.coins
    )


st.divider()


# -----------------------------
# 이동 입력
# -----------------------------

st.header("🚦 TODAY'S JOURNEY")


car_minutes = st.slider(
    "🚗 자동차",
    0,
    180,
    30,
    5
)


bus_minutes = st.slider(
    "🚌 버스",
    0,
    180,
    20,
    5
)


subway_minutes = st.slider(
    "🚇 지하철",
    0,
    180,
    30,
    5
)


walking_minutes = st.slider(
    "🚶 도보",
    0,
    180,
    20,
    5
)


# -----------------------------
# 탄소 계산
# -----------------------------

carbon = calculate_transport_carbon(
    car_minutes,
    bus_minutes,
    subway_minutes
)


# -----------------------------
# 결과
# -----------------------------

st.divider()

st.subheader("🌍 TODAY'S CARBON")

st.metric(
    "예상 배출량",
    f"{carbon:.2f} kg CO₂e"
)


# -----------------------------
# 기록
# -----------------------------

if st.button(
    "▶ JOURNEY COMPLETE",
    use_container_width=True
):

    if st.session_state.previous_carbon is None:

        st.session_state.previous_carbon = carbon

        st.session_state.xp += 10
        st.session_state.coins += 10

        st.success(
            "첫 번째 여정 완료!\n\n"
            "⭐ +10 EXP\n"
            "🪙 +10 COIN"
        )

    else:

        previous = st.session_state.previous_carbon

        reduction = previous - carbon

        if reduction > 0:

            xp = max(
                10,
                int(reduction * 40)
            )

            coins = max(
                10,
                int(reduction * 25)
            )

            st.session_state.xp += xp
            st.session_state.coins += coins

            st.session_state.previous_carbon = carbon

            st.success(
                f"🌱 탄소 감축 성공!\n\n"
                f"{reduction:.2f} kg 감소\n\n"
                f"⭐ +{xp} EXP\n"
                f"🪙 +{coins} COIN"
            )

        else:

            st.session_state.previous_carbon = carbon

            st.info(
                "오늘의 여정이 끝났습니다.\n\n"
                "내일은 조금 더 줄여볼까요?"
            )


# -----------------------------
# 다음 보상
# -----------------------------

st.divider()

st.header("🎁 NEXT VEHICLE")

if st.session_state.xp < 100:

    st.image(
        "assets/autumn_bike_locked.png",
        width=220
    )

    st.write("🔒 ???")

    st.progress(
        st.session_state.xp / 100
    )

    st.caption(
        f"{st.session_state.xp} / 100 EXP"
    )

else:

    st.image(
        "assets/autumn_bike.png",
        width=220
    )

    st.success(
        "🍂 AUTUMN BIKE UNLOCKED!"
    )
