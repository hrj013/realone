# =========================================================
# CARBON FACTORS
# =========================================================
#
# 현재 값은 프로토타입용 예시입니다.
# 실제 서비스에서는 신뢰할 수 있는 최신 배출계수로 교체해야 합니다.
#

CAR_FACTORS = {
    "car": 0.21,
    "bus": 0.05,
    "subway": 0.02,
}


def calculate_transport_carbon(
    car_minutes,
    bus_minutes,
    subway_minutes,
):
    """
    이동 시간을 이용하여
    예상 교통 탄소배출량을 계산한다.
    """

    # -----------------------------------------
    # 시간 → 예상 이동거리
    # -----------------------------------------

    # 평균속도 역시 프로토타입용 가정값
    car_speed = 30
    bus_speed = 20
    subway_speed = 25

    car_distance = (
        car_minutes / 60
    ) * car_speed

    bus_distance = (
        bus_minutes / 60
    ) * bus_speed

    subway_distance = (
        subway_minutes / 60
    ) * subway_speed

    # -----------------------------------------
    # 거리 → 탄소배출량
    # -----------------------------------------

    car_carbon = (
        car_distance
        * CAR_FACTORS["car"]
    )

    bus_carbon = (
        bus_distance
        * CAR_FACTORS["bus"]
    )

    subway_carbon = (
        subway_distance
        * CAR_FACTORS["subway"]
    )

    # -----------------------------------------
    # 총합
    # -----------------------------------------

    total = (
        car_carbon
        + bus_carbon
        + subway_carbon
    )

    return total
