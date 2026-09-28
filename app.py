import streamlit as st
from carbon import calculate_transport_carbon


# =========================================================
# 기본 설정
# =========================================================

st.set_page_config(
    page_title="CARBON RIDER",
    page_icon="🌱",
    layout="centered",
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

if "recorded" not in st.session_state:
    st.session_state.recorded = False


# =========================================================
# CSS
# =========================================================

st.markdown(
    """
    <style>

    /* 전체 배경 */
    .stApp {
        background-color: #111111;
        color: #eeeeee;
    }

    /* 기본 폰트 */
    html, body, [class*="css"] {
        font-family: monospace;
    }

    /* 제목 */
    .game-title {
        text-align: center;
        color: #ffffff;
        font-size: 42px;
        font-weight: 900;
        letter-spacing: 5px;
        margin-top: 10px;
        margin-bottom: 0px;
        text-shadow: 3px 3px 0px #333333;
    }

    .game-subtitle {
        text-align: center;
        color: #aaaaaa;
        font-size: 14px;
        margin-bottom: 25px;
    }

    /* 게임 화면 */
    .game-box {
        background-color: #1b1b1b;
        border: 3px solid #eeeeee;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 6px 6px 0px #000000;
    }

    /* 캐릭터 영역 */
    .character-box {
        background-color: #222222;
        border: 2px solid #555555;
        padding: 30px 10px;
        text-align: center;
        margin-bottom: 20px;
    }

    .character {
        font-size: 80px;
        line-height: 1;
    }

    .character-name {
        color: #ffffff;
        font-size: 18px;
        margin-top: 12px;
    }

    /* 대화창 */
    .dialogue {
        background-color: #0d0d0d;
        border: 2px solid #ffffff;
        padding: 18px;
        margin-top: 10px;
        margin-bottom: 20px;
        line-height: 1.7;
    }

    .speaker {
        color: #6cff6c;
        font-weight: bold;
    }

    /* 스탯 */
    .stat-box {
        background-color: #181818;
        border: 2px solid #444444;
        padding: 12px;
        text-align: center;
    }

    .stat-label {
        color: #888888;
        font-size: 12px;
    }

    .stat-value {
        color: #ffffff;
        font-size: 24px;
        font-weight: bold;
    }

    /* 탄소량 */
    .carbon-value {
        text-align: center;
        color: #6cff6c;
        font-size: 42px;
        font-weight: bold;
        margin: 10px 0px;
    }

    .carbon-label {
        text-align: center;
        color: #999999;
        font-size: 13px;
    }

    /* 시즌 */
    .season {
        color: #ffcc66;
        text-align: center;
        font-size: 18px;
        font-weight: bold;
        margin-bottom: 10px;
    }

    /* Streamlit 버튼 */
    .stButton > button {
        width: 100%;
        background-color: #222222;
        color: #ffffff;
        border: 2px solid #ffffff;
        border-radius: 0px;
        font-family: monospace;
        font-weight: bold;
    }

    .stButton > button:hover {
        background-color: #ffffff;
        color: #111111;
        border-color: #ffffff;
    }

    /* 슬라이더 */
    .stSlider {
        padding-top: 5px;
        padding-bottom: 10px;
    }

    /* 안내창 */
    .stAlert {
        border-radius: 0px;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# 타이틀
# =========================================================

st.markdown(
    '<div class="game-title">CARBON RIDER</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="game-subtitle">A JOURNEY TO A LOWER-CARBON WORLD</div>',
    unsafe_allow_html=True
)


# =========================================================
# 캐릭터
# =========================================================

st.markdown(
    """
    <div class="character-box">

        <div class="character">🏍️</div>

        <div class="character-name">
            LEAF RIDER
        </div>

    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# 대화창
# =========================================================

st.markdown(
    """
    <div class="dialogue">

        <div class="speaker">???</div>

        오늘도 길을 떠날 시간이야.<br>
        네가 선택하는 이동이<br>
        이 세계의 내일을 바꾼다.

    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# 시즌
# =========================================================

st.markdown(
    """
    <div class="season">
        🍂 SEASON 01 — AUTUMN TRAIL
    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# 플레이어 스탯
# =========================================================

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        f"""
        <div class="stat-box">
            <div class="stat-label">LEVEL</div>
            <div class="stat-value">1</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        f"""
        <div class="stat-box">
            <div class="stat-label">EXP</div>
            <div class="stat-value">{st.session_state.xp}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        f"""
        <div class="stat-box">
            <div class="stat-label">COIN</div>
            <div class="stat-value">{st.session_state.coins}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


st.write("")


# =========================================================
# 이동 기록
# =========================================================

st.markdown(
    """
    <div class="game-box">
        <h3>🚦 TODAY'S JOURNEY</h3>
    </div>
    """,
    unsafe_allow_html=True
)


car_minutes = st.slider(
    "🏍️ CAR",
    min_value=0,
    max_value=180,
    value=30,
    step=5,
    format="%d min",
)

bus_minutes = st.slider(
    "🚌 BUS",
    min_value=0,
    max_value=180,
    value=20,
    step=5,
    format="%d min",
)

subway_minutes = st.slider(
    "🚇 SUBWAY",
    min_value=0,
    max_value=180,
    value=30,
    step=5,
    format="%d min",
)

walking_minutes = st.slider(
    "🚶 WALK",
    min_value=0,
    max_value=180,
    value=20,
    step=5,
    format="%d min",
)


# =========================================================
# 탄소 계산
# =========================================================

carbon = calculate_transport_carbon(
    car_minutes,
    bus_minutes,
    subway_minutes,
)


# =========================================================
# 탄소 결과
# =========================================================

st.markdown(
    """
    <div class="game-box">

        <div class="carbon-label">
            TODAY'S ESTIMATED CARBON
        </div>

        <div class="carbon-value">
            %.2f kg
        </div>

        <div class="carbon-label">
            CO₂e
        </div>

    </div>
    """
    % carbon,
    unsafe_allow_html=True
)


# =========================================================
# 기록하기
# =========================================================

if st.button("▶ SAVE TODAY'S RECORD"):

    if st.session_state.previous_carbon is None:

        st.session_state.previous_carbon = carbon

        st.session_state.xp += 10
        st.session_state.coins += 10

        st.success(
            "FIRST JOURNEY COMPLETE\n\n"
            "+10 EXP\n"
            "+10 COIN"
        )

    else:

        previous = st.session_state.previous_carbon

        reduction = previous - carbon

        if reduction > 0:

            # 감축량에 따른 보상
            xp = max(10, int(reduction * 40))
            coins = max(10, int(reduction * 25))

            st.session_state.xp += xp
            st.session_state.coins += coins

            st.session_state.previous_carbon = carbon

            st.balloons()

            st.success(
                f"🌱 CARBON REDUCED!\n\n"
                f"{reduction:.2f} kg less than yesterday.\n\n"
                f"+{xp} EXP\n"
                f"+{coins} COIN"
            )

        else:

            st.session_state.previous_carbon = carbon

            st.info(
                "The journey continues...\n\n"
                "Try reducing your carbon footprint tomorrow."
            )


# =========================================================
# 현재 상태
# =========================================================

st.markdown("---")

st.markdown(
    f"""
    <div class="dialogue">

        <div class="speaker">SYSTEM</div>

        CURRENT EXP : {st.session_state.xp}<br>
        CURRENT COIN : {st.session_state.coins}

    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# 다음 목표
# =========================================================

next_level = 100

progress = min(st.session_state.xp / next_level, 1.0)

st.progress(
    progress,
    text=f"NEXT LEVEL — {st.session_state.xp} / {next_level} EXP"
)
