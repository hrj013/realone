CAR_FACTORS = {
    "car": 0.21,
    "bus": 0.05,
    "subway": 0.02,
}


def calculate_transport_carbon(
    car_minutes,
    bus_minutes,
    subway_minutes
):

    # 프로토타입용 평균속도
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

    return (
        car_carbon
        + bus_carbon
        + subway_carbon
    )
