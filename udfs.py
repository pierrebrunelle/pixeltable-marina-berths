"""Pixeltable UDFs for marina berth booking (recorded by module path, e.g. `udfs.berth_fee`)."""
import pixeltable as pxt

RATE_PER_M_NIGHT = 3.75


@pxt.udf
def berth_fee(loa_m: float, nights: int) -> float:
    """Length-overall x nights x rate, with a weekly discount."""
    fee = loa_m * nights * RATE_PER_M_NIGHT
    return round(fee * (0.85 if nights >= 7 else 1.0), 2)


@pxt.udf
def stay_band(nights: int) -> str:
    return 'transient' if nights <= 2 else ('weekly' if nights < 28 else 'seasonal')


@pxt.udf
def size_class(loa_m: float) -> str:
    return 'small' if loa_m < 9 else ('medium' if loa_m < 15 else 'large')


@pxt.udf
def slip_label(dock: str, slip_id: str, length_m: float) -> str:
    return f'Dock {dock} · {slip_id} · {length_m:g} m'
