"""Marina queries."""
import pixeltable as pxt

from models import Bookings, Slips


@pxt.query
def slips_that_fit(loa_m: float):
    """Slips long enough for a vessel, tightest fit first."""
    return Slips.where(Slips.length_m >= loa_m).select(Slips.slip_id, Slips.label, Slips.power_amps).order_by(Slips.length_m)


@pxt.query
def slip_bookings(slip_id: str):
    return Bookings.where(Bookings.slip_id == slip_id).select(
        Bookings.id, Bookings.vessel_name, Bookings.nights, Bookings.fee, Bookings.band
    ).order_by(Bookings.vessel_name)
