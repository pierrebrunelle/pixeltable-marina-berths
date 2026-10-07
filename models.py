"""Slips (string PK), vessels (with a Binary column) and bookings."""
import pixeltable as pxt
import pixeltable.functions as pxtf

from udfs import berth_fee, size_class, slip_label, stay_band

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
