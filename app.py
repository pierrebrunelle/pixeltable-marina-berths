"""Marina Berth Booking API built with Pixeltable.

    pxt schema update app.py marina
    pxt service run app.py marina
"""
import pixeltable as pxt
import pixeltable.functions as pxtf
from pixeltable.serving import FastAPIRouter

from udfs import berth_fee, size_class, slip_label, stay_band

# ---- tables ----
TableModel = pxt.model_base()


class Slips(TableModel, name='slips'):
    slip_id = pxt.Column(type=pxt.String, primary_key=True)
    dock: pxt.String
    length_m: pxt.Float
    power_amps: pxt.Int

    label = slip_label(dock, slip_id, length_m)


class Vessels(TableModel, name='vessels'):
    id = pxt.Column(value=pxtf.uuid.uuid7(), primary_key=True)
    name: pxt.String
    loa_m: pxt.Float
    owner: pxt.String
    note_bin: pxt.Binary | None

    size = size_class(loa_m)


class Bookings(TableModel, name='bookings'):
    id = pxt.Column(value=pxtf.uuid.uuid7(), primary_key=True)
    slip_id: pxt.String
    vessel_name: pxt.String
    loa_m: pxt.Float
    nights: pxt.Int

    fee = berth_fee(loa_m, nights)
    band = stay_band(nights)


# ---- queries ----
@pxt.query
def slips_that_fit(loa_m: float):
    """Slips long enough for a vessel, tightest fit first."""
    return Slips.where(Slips.length_m >= loa_m).select(Slips.slip_id, Slips.label, Slips.power_amps).order_by(Slips.length_m)


@pxt.query
def slip_bookings(slip_id: str):
    return Bookings.where(Bookings.slip_id == slip_id).select(
        Bookings.id, Bookings.vessel_name, Bookings.nights, Bookings.fee, Bookings.band
    ).order_by(Bookings.vessel_name)


# ---- routes ----
marina_api = FastAPIRouter(name='marina_api')
marina_api.add_insert_route(Slips, path='/slips', inputs=[Slips.slip_id, Slips.dock, Slips.length_m, Slips.power_amps],
                            outputs=[Slips.slip_id, Slips.label])
marina_api.add_insert_route(Vessels, path='/vessels', inputs=[Vessels.name, Vessels.loa_m, Vessels.owner],
                            outputs=[Vessels.id, Vessels.size])
marina_api.add_insert_route(Bookings, path='/bookings',
                            inputs=[Bookings.slip_id, Bookings.vessel_name, Bookings.loa_m, Bookings.nights],
                            outputs=[Bookings.id, Bookings.fee, Bookings.band])
marina_api.add_update_route(Bookings, path='/bookings/extend', inputs=[Bookings.nights],
                            outputs=[Bookings.id, Bookings.nights, Bookings.fee, Bookings.band])
marina_api.add_delete_route(Bookings, path='/bookings/cancel')
marina_api.add_compute_route(Bookings, path='/band', inputs=[Bookings.nights], outputs=[Bookings.band])
marina_api.add_compute_route(Bookings, path='/quote', inputs=[Bookings.loa_m, Bookings.nights],
                             outputs=[Bookings.fee, Bookings.band])
marina_api.add_query_route(path='/slips/fit', query=slips_that_fit, method='get')
marina_api.add_query_route(path='/slips/bookings', query=slip_bookings, method='get')
