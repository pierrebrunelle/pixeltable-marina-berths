"""Seed slips, vessels (one with a binary note) and bookings.

Usage:
    python seed.py            # seeds the local `marina` catalog directory
    python seed.py my_dir     # or another directory you passed to `pxt schema update`
"""
import sys
from pathlib import Path

import pixeltable as pxt

target = sys.argv[1] if len(sys.argv) > 1 else 'marina'
HERE = Path(__file__).resolve().parent

SEED = {
    'slips': [
        {'slip_id': 'A-10', 'dock': 'A', 'length_m': 9.0, 'power_amps': 30},
        {'slip_id': 'A-12', 'dock': 'A', 'length_m': 12.0, 'power_amps': 30},
        {'slip_id': 'B-03', 'dock': 'B', 'length_m': 15.0, 'power_amps': 50},
        {'slip_id': 'B-07', 'dock': 'B', 'length_m': 18.0, 'power_amps': 50},
        {'slip_id': 'C-01', 'dock': 'C', 'length_m': 24.0, 'power_amps': 100},
    ],
    'vessels': [
        {'name': 'Kittiwake', 'loa_m': 8.5, 'owner': 'J. Moreau', 'note_bin': None},
        {'name': 'Sea Lark', 'loa_m': 11.6, 'owner': 'P. Agarwal', 'note_bin': b'insurance cert #SL-2291'},
        {'name': 'Northern Star', 'loa_m': 17.2, 'owner': 'Halvorsen LLC', 'note_bin': None},
    ],
    'bookings': [
        {'slip_id': 'A-12', 'vessel_name': 'Sea Lark', 'loa_m': 11.6, 'nights': 3},
        {'slip_id': 'B-07', 'vessel_name': 'Northern Star', 'loa_m': 17.2, 'nights': 30},
    ],
}

for table_name, rows in SEED.items():
    t = pxt.get_table(f'{target}/{table_name}')
    if t.count() > 0:
        print(f'{target}/{table_name} already has {t.count()} rows; skipping')
        continue
    for row in rows:
        for k, v in row.items():
            if isinstance(v, str) and v.startswith('data/'):
                row[k] = str(HERE / v)   # local sample media file
    t.insert(rows)
    print(f'inserted {len(rows)} rows into {target}/{table_name}')
