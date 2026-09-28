import os
import streamlit as st

from carbon import calculate_transport_carbon


# =========================================================
# 기본 설정
# =========================================================

st.set_page_config(
    page_title="CARBON RIDER",
    page_icon="🌱",
    layout="centered"
)


# =========================================================
# 게임 데이터
# =========================================================

if "xp" not in st.session_state:
    st.session_state.xp = 0

if "coins" not in st.session_state:
    st.session_state.coins = 0

if "previous_carbon" not in st.session_state:
    st.session_state.previous_carbon = None


# =========================================================
# 이미지 경로
# =========================================================

RIDER_IMAGE = "assets/rider.png"

LOCKED_BIKE_IMAGE = "assets/autumn_bike_locked.png"

BIKE_IMAGE = "assets/autumn_bike.png"


# =========================================================
# CSS
# =========================================================

st.markdown(
    """
    <style>

    /* =========================================
       전체 화면
       ========================================= */

    .stApp {
        background-color: #101018;
        color: white;
    }


    /* =========================================
       기본 글꼴
       ========================================= */

    h1,
    h2,
    h3,
    p,
    div,
    span {
        font-family: monospace;
    }


    /* =========================================
       제목
       ========================================= */

    .game-title {
        text-align: center;

        font-size: 38px;

        font-weight: bold;

        letter-spacing: 5px;

        color: white;

        margin-top: 10px;
    }


    .game-subtitle {
        text-align: center;

        color: #777788;

        font-family: monospace;

        font-size: 13px;

        letter-spacing: 2px;
    }


    /* =========================================
       캐릭터 이름
       ========================================= */

    .character-name {
        text-align: center;

        color: white;

        font-size: 18px;

        font-weight: bold;

        letter-spacing: 3px;

        margin-top: 5px;

        margin-bottom: 20px;
    }


    /* =========================================
       대화창
       ========================================= */

    .dialogue {
        background-color: #08080d;

        border: 3px solid white;

        padding: 20px;

        font-family: monospace;

        line-height: 1.8;

        margin-top: 15px;

        margin-bottom: 20px;

        box-shadow: 5px 5px 0px #000000;
    }


    .speaker {
        color: #6cff8a;

        font-weight: bold;

        margin-bottom: 10px;
    }


    /* =========================================
       시즌
       ========================================= */

    .season {
        text-align: center;

        color: #ffcf5c;

        font-size: 18px;

        font-weight: bold;

        letter-spacing: 2px;

        margin-top: 15px;

        margin-bottom: 5px;
    }


    .season-info {
        text-align: center;

        color: #777788;

        font-size: 12px;

        margin-bottom: 20px;
    }


    /* =========================================
       탄소량
       ========================================= */

    .carbon-box {
        background-color: #08080d;

        border: 3px solid #6cff8a;

        padding: 20px;

        text-align: center;

        margin-top: 15px;

        margin-bottom: 20px;
    }


    .carbon-label {
        color: #777788;

        font-size: 12px;

        letter-spacing: 2px;
    }


    .carbon-number {
        color: #6cff8a;

        font-size: 40px;

        font-weight: bold;

        margin: 5px;
    }


    /* =========================================
       버튼
       ========================================= */

    .stButton > button {

        background-color: #151522;

        color: white;

        border: 2px solid white;

        border-radius: 0px;

        font-family: monospace;

        font-weight: bold;

        min-height: 45px;

    }


    .stButton > button:hover {

        background-color: white;

        color: #101018;

    }


    /* =========================================
       구분선
       ========================================= */

    hr {
        border-color: #333344;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# 타이틀
# =========================================================

st.markdown(
    '<div class="game-title">CARBON RIDER</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="game-subtitle">'
    'A JOURNEY TO A LOWER-CARBON WORLD'
    '</div>',
    unsafe_allow_html=True
)


# =========================================================
# 시즌
# =========================================================

st.markdown(
    '<div class="season">'
    '🍂 SEASON 01 — AUTUMN TRAIL'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="season-info">'
    'SEASON 01'
    '</div>',
    unsafe_allow_html=True
)


# =========================================================
# 캐릭터
# =========================================================

if os.path.exists(RIDER_IMAGE):

    st.image(
        RIDER_IMAGE,
        width=180
    )

else:

    st.markdown(
        """
        <div style="
            text-align:center;
            font-size:80px;
            padding:20px;
        ">
            🏍️
        </div>
        """,
        unsafe_allow_html=True
    )


st.markdown(
    '<div class="character-name">'
    'LEAF RIDER'
    '</div>',
    unsafe_allow_html=True
)


# =========================================================
# 대화창
# =========================================================

st.markdown(
    """
    <div class="dialogue">

        <div class="speaker">
            ???
        </div>

        오늘도 길을 떠날 시간이야.<br>
        <br>
        네가 선택하는 이동이<br>
        이 세계의 내일을 바꾼다.

    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# 플레이어 정보
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


st.divider()


# =========================================================
# 오늘의 이동
# =========================================================

st.header("🚦 TODAY'S JOURNEY")

st.caption(
    "오늘 하루 동안 이용한 교통수단의 시간을 입력하세요."
)


# 자동차

car_minutes = st.slider(
    "🚗 자동차",
    min_value=0,
    max_value=180,
    value=30,
    step=5,
    format="%d분"
)


# 버스

bus_minutes = st.slider(
    "🚌 버스",
    min_value=0,
    max_value=180,
    value=20,
    step=5,
    format="%d분"
)


# 지하철

subway_minutes = st.slider(
    "🚇 지하철",
    min_value=0,
    max_value=180,
    value=30,
    step=5,
    format="%d분"
)


# 도보

walking_minutes = st.slider(
    "🚶 도보",
    min_value=0,
    max_value=180,
    value=20,
    step=5,
    format="%d분"
)


# =========================================================
# 탄소 계산
# =========================================================

carbon = calculate_transport_carbon(
    car_minutes,
    bus_minutes,
    subway_minutes
)


# =========================================================
# 탄소 결과
# =========================================================

st.divider()


st.markdown(
    """
    <div class="carbon-box">

        <div class="carbon-label">
            TODAY'S CARBON
        </div>

    """,
    unsafe_allow_html=True
)


st.markdown(
    f"""
        <div class="carbon-number">
            {carbon:.2f}
        </div>

        <div class="carbon-label">
            kg CO₂e
        </div>

    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# 여정 완료
# =========================================================

if st.button(
    "▶ JOURNEY COMPLETE",
    use_container_width=True
):

    # -----------------------------------------------------
    # 첫 번째 기록
    # -----------------------------------------------------

    if st.session_state.previous_carbon is None:

        st.session_state.previous_carbon = carbon

        st.session_state.xp += 10

        st.session_state.coins += 10

        st.success(
            "첫 번째 여정 완료!\n\n"
            "⭐ +10 EXP\n"
            "🪙 +10 COIN"
        )


    # -----------------------------------------------------
    # 이전 기록과 비교
    # -----------------------------------------------------

    else:

        previous = st.session_state.previous_carbon

        reduction = previous - carbon


        # -------------------------------------------------
        # 탄소 감축
        # -------------------------------------------------

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


            st.balloons()


            st.success(
                f"🌱 탄소 감축 성공!\n\n"
                f"이전보다 {reduction:.2f} kg 감소했습니다.\n\n"
                f"⭐ +{xp} EXP\n"
                f"🪙 +{coins} COIN"
            )


        # -------------------------------------------------
        # 탄소 증가 또는 동일
        # -------------------------------------------------

        else:

            st.session_state.previous_carbon = carbon

            st.info(
                "오늘의 여정이 끝났습니다.\n\n"
                "내일은 조금 더 줄여볼까요?"
            )


# =========================================================
# 다음 차량
# =========================================================

st.divider()

st.header("🎁 NEXT VEHICLE")


# =========================================================
# 차량 잠금 상태
# =========================================================

if st.session_state.xp < 100:

    # 이미지가 존재하면 표시
    if os.path.exists(LOCKED_BIKE_IMAGE):

        st.image(
            LOCKED_BIKE_IMAGE,
            width=220
        )

    # 이미지가 없으면 임시 이모지
    else:

        st.markdown(
            """
            <div style="
                text-align:center;
                font-size:70px;
                padding:20px;
            ">
                🔒 🏍️
            </div>
            """,
            unsafe_allow_html=True
        )


    st.write(
        "🔒 ???"
    )


    # 경험치 진행도

    progress = min(
        st.session_state.xp / 100,
        1.0
    )


    st.progress(
        progress
    )


    st.caption(
        f"{st.session_state.xp} / 100 EXP"
    )


# =========================================================
# 차량 해금
# =========================================================

else:

    # 이미지가 존재하면 표시
    if os.path.exists(BIKE_IMAGE):

        st.image(
            BIKE_IMAGE,
            width=220
        )

    # 이미지가 없으면 임시 이모지
    else:

        st.markdown(
            """
            <div style="
                text-align:center;
                font-size:70px;
                padding:20px;
            ">
                🍂 🏍️
            </div>
            """,
            unsafe_allow_html=True
        )


    st.success(
        "🍂 AUTUMN BIKE UNLOCKED!"
    )
