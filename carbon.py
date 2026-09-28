# carbon.py

CAR_FACTORS = {
    "car": 0.21,
    "bus": 0.05,
    "subway": 0.02,
    "walking": 0.0,
}


def calculate_transport_carbon(
    car_minutes,
    bus_minutes,
    subway_minutes,
):
    """
    이동시간을 이용해 예상 탄소배출량을 계산한다.

    주의:
    현재는 프로토타입용 예시값이다.
    실제 서비스에서는 신뢰할 수 있는 배출계수를 사용해야 한다.
    """

    # 시간 → 예상 거리
    car_distance = car_minutes / 60 * 30
    bus_distance = bus_minutes / 60 * 20
    subway_distance = subway_minutes / 60 * 25

    car_carbon = car_distance * CAR_FACTORS["car"]
    bus_carbon = bus_distance * CAR_FACTORS["bus"]
    subway_carbon = subway_distance * CAR_FACTORS["subway"]

    total = (
        car_carbon
        + bus_carbon
        + subway_carbon
    )

    return total
