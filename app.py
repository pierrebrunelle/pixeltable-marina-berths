"""Marina Berth Booking API built with Pixeltable.

    pxt schema update app.py marina
    pxt service run app.py marina
"""
from pixeltable.serving import FastAPIRouter

from models import Bookings, Slips, TableModel, Vessels  # noqa: F401  (TableModel lets `pxt schema` find the models)
from queries import slip_bookings, slips_that_fit

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
