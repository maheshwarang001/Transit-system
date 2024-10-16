
# Calculates additional fees based on the zone

def additional_zone_fee(zone: int) -> float:

    match zone:
        case 1:
            return 0.80
        case 2 | 3:
            return 0.50
        case 4 | 5:
            return 0.30
        case _:
            return 0.10  # Default case for zones 6 and above
