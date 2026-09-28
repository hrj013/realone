import os
import streamlit as st

from carbon import calculate_transport_carbon


# =========================================================
# 기본 설정
# =========================================================

st.set_page_config(
    page_title="CARBON RIDER",
    page_icon="🏍️",
    layout="centered"
)


# =========================================================
# 게임 상태
# =========================================================

if "xp" not in st.session_state:
    st.session_state.xp = 0

if "coins" not in st.session_state:
    st.session_state.coins = 0

if "previous_carbon" not in st.session_state:
    st.session_state.previous_carbon = None

if "player_x" not in st.session_state:
    st.session_state.player_x = 0

if "player_y" not in st.session_state:
    st.session_state.player_y = 2

if "energy" not in st.session_state:
    st.session_state.energy = 0


# =========================================================
# CSS
# =========================================================

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
    font-size: 36px;
    font-weight: bold;
    letter-spacing: 5px;
}

.game-subtitle {
    text-align: center;
    color: #777788;
    font-family: monospace;
}

.map {
    background-color: #171724;

    border: 4px solid white;

    padding: 15px;

    font-family: monospace;

    font-size: 28px;

    line-height: 1.5;

    text-align: center;

    box-shadow:
        6px 6px 0px #000000;

    margin-top: 20px;

    margin-bottom: 20px;
}

.dialogue {
    background-color: #08080d;

    border: 3px solid white;

    padding: 18px;

    font-family: monospace;

    line-height: 1.7;
}

.energy {
    color: #6cff8a;

    font-weight: bold;

}

</style>
""", unsafe_allow_html=True)


# =========================================================
# 제목
# =========================================================

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


# =========================================================
# 맵
# =========================================================

MAP_WIDTH = 7
MAP_HEIGHT = 5


# 맵 생성

game_map = []

for y in range(MAP_HEIGHT):

    row = []

    for x in range(MAP_WIDTH):

        # 플레이어
        if (
            x == st.session_state.player_x
            and y == st.session_state.player_y
        ):

            row.append("🏍️")

        # 목적지
        elif x == 6 and y == 2:

            row.append("🏁")

        # 나무
        elif (x + y) % 5 == 0:

            row.append("🌲")

        # 길
        else:

            row.append("▫️")

    game_map.append(row)


# 맵 출력

map_text = ""

for row in game_map:

    map_text += " ".join(row)
    map_text += "<br>"


st.markdown(
    f"""
    <div class="map">
        {map_text}
    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# 상태
# =========================================================

col1, col2, col3 = st.columns(3)


with col1:

    st.metric(
        "LEVEL",
        "01"
    )


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


# =========================================================
# 에너지
# =========================================================

st.subheader("⚡ RIDER ENERGY")

st.progress(
    min(st.session_state.energy / 10, 1.0)
)

st.write(
    f"Energy: {st.session_state.energy} / 10"
)


# =========================================================
# 탄소 계산
# =========================================================

st.divider()

st.header("🌱 TODAY'S JOURNEY")


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


# =========================================================
# 탄소 계산
# =========================================================

carbon = calculate_transport_carbon(
    car_minutes,
    bus_minutes,
    subway_minutes
)


st.metric(
    "TODAY'S CARBON",
    f"{carbon:.2f} kg CO₂e"
)


# =========================================================
# 여정 완료
# =========================================================

if st.button(
    "🌱 COMPLETE JOURNEY",
    use_container_width=True
):

    if st.session_state.previous_carbon is None:

        st.session_state.previous_carbon = carbon

        st.session_state.xp += 10

        st.session_state.coins += 10

        st.session_state.energy += 3

        st.success(
            "첫 번째 여정 완료!\n\n"
            "⚡ +3 ENERGY\n"
            "⭐ +10 EXP\n"
            "🪙 +10 COIN"
        )

    else:

        previous = st.session_state.previous_carbon

        reduction = previous - carbon


        if reduction > 0:

            energy = max(
                1,
                int(reduction * 5)
            )

            xp = max(
                10,
                int(reduction * 40)
            )

            coins = max(
                5,
                int(reduction * 20)
            )


            st.session_state.energy += energy

            st.session_state.xp += xp

            st.session_state.coins += coins

            st.session_state.previous_carbon = carbon


            st.success(
                f"🌱 CARBON REDUCED!\n\n"
                f"{reduction:.2f} kg 감소\n\n"
                f"⚡ +{energy} ENERGY\n"
                f"⭐ +{xp} EXP\n"
                f"🪙 +{coins} COIN"
            )

        else:

            st.session_state.previous_carbon = carbon

            st.info(
                "탄소 배출량이 줄지 않았습니다."
            )


# =========================================================
# 이동 버튼
# =========================================================

st.divider()

st.header("🏍️ RIDE")


# 위

if st.button(
    "⬆️",
    use_container_width=True
):

    if st.session_state.energy > 0:

        if st.session_state.player_y > 0:

            st.session_state.player_y -= 1

            st.session_state.energy -= 1

            st.rerun()


# 좌우

col1, col2, col3 = st.columns(3)


with col1:

    if st.button(
        "⬅️",
        use_container_width=True
    ):

        if st.session_state.energy > 0:

            if st.session_state.player_x > 0:

                st.session_state.player_x -= 1

                st.session_state.energy -= 1

                st.rerun()


with col2:

    if st.button(
        "⏺️",
        use_container_width=True
    ):

        st.rerun()


with col3:

    if st.button(
        "➡️",
        use_container_width=True
    ):

        if st.session_state.energy > 0:

            if st.session_state.player_x < MAP_WIDTH - 1:

                st.session_state.player_x += 1

                st.session_state.energy -= 1

                st.rerun()


# 아래

if st.button(
    "⬇️",
    use_container_width=True
):

    if st.session_state.energy > 0:

        if st.session_state.player_y < MAP_HEIGHT - 1:

            st.session_state.player_y += 1

            st.session_state.energy -= 1

            st.rerun()


# =========================================================
# 목적지 도착
# =========================================================

if (
    st.session_state.player_x == 6
    and st.session_state.player_y == 2
):

    st.balloons()

    st.success(
        "🏁 DESTINATION REACHED!\n\n"
        "🌱 GREEN JOURNEY COMPLETE!\n\n"
        "+50 EXP\n"
        "+100 COIN"
    )

    st.session_state.xp += 50

    st.session_state.coins += 100
