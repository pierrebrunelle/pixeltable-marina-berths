<!-- pixeltable-example-app: 20261001-marina-berths -->
# Marina Berth Booking API built with Pixeltable

[![Built with Pixeltable](https://img.shields.io/badge/built%20with-Pixeltable-5b4bff)](https://pixeltable.com)
[![PyPI - pixeltable](https://img.shields.io/pypi/v/pixeltable?label=pixeltable)](https://pypi.org/project/pixeltable/)
[![GitHub stars](https://img.shields.io/github/stars/pixeltable/pixeltable?style=social)](https://github.com/pixeltable/pixeltable)
[![License: Apache-2.0](https://img.shields.io/badge/license-Apache--2.0-blue)](LICENSE)

Run a small marina: **slips** keyed by a human-readable string id (`A-12`), **vessels** with an optional binary attachment, and **bookings** that price a stay from the boat's length overall and the number of nights. Pixeltable computes the berth fee, a stay band and a booking label. The example leans on everyday data reads and writes: string-PK lookups with `pxt get`, bulk inserts, filtered queries, updates and deletes, from both the API and the CLI.

[Pixeltable](https://pixeltable.com) is open-source, Python-native **multimodal AI data infrastructure**: tables, incremental computed columns, UDFs, indexes and serving in one library, running locally or on Pixeltable Cloud.

> ⭐ **Like this example?** Star [pixeltable/pixeltable](https://github.com/pixeltable/pixeltable) on GitHub. It helps other developers find it.

## What this example shows

- **Reads and writes**: Json columns, primary-key updates and deletes, and quick inspection with the `pxt` CLI (`pxt rows`, `pxt get`, `pxt count`)
- **`pixeltable.toml` project config**: local and Pixeltable Cloud database sizing in one file
- **Multi-table layout and schema evolution** with `pxt schema update`
- **Incremental computed columns** powered by plain Python UDFs (`@pxt.udf`)
- **FastAPI serving**: one `FastAPIRouter` turns tables and `@pxt.query` functions into typed REST routes (insert, update, delete, compute and query) with OpenAPI docs
- **Importable UDF module**: UDFs in `udfs.py`, tables in `models.py`, queries in `queries.py`, routes in `app.py` (Pixeltable resolves UDFs by module path)
- **`pixeltable.toml`** declares a local database and a **Pixeltable Cloud** database, so the same code deploys with `pxt db update`

## Reads and writes, four ways

| Task | API | Python SDK | CLI |
|------|-----|------------|-----|
| Add rows | `POST /bookings` | `pxt.get_table('marina/bookings').insert([...])` | n/a |
| Look up by primary key | `GET /slips/fit?loa_m=12` (query) | `t.where(t.slip_id == 'A-12').collect()` | `pxt get marina/slips A-12` |
| Change a row | `POST /bookings/extend` | `t.update({'nights': 5}, where=t.id == ...)` | n/a |
| Remove a row | `POST /bookings/cancel` | `t.delete(where=...)` | n/a |
| Peek / count | n/a | `t.head(5)`, `t.count()` | `pxt rows marina/bookings -n 5`, `pxt count marina/bookings` |

`vessels.note_bin` is a `pxt.Binary` column: `seed.py` stores raw bytes, and they round-trip unchanged.

## What's inside

| File | What it is |
|------|------------|
| `app.py` | The API: one `FastAPIRouter` wiring the tables and queries into REST routes |
| `client_demo.py` | Quote, find a slip, book, extend and cancel a berth through the API |
| `models.py` | Tables declared as Python classes: columns, computed columns, indexes |
| `pixeltable.toml` | Project config: the local database plus a Pixeltable Cloud database (sizing, deploy excludes) |
| `queries.py` | `@pxt.query` functions served as query routes |
| `seed.py` | Seed slips, vessels (one with a binary note) and bookings |
| `udfs.py` | Pixeltable UDFs (`@pxt.udf`) in their own importable module |
| `requirements.txt` / `pyproject.toml` | Dependencies (`pixeltable[serve]>=0.7.14`) |

**Tables**

| Table | Stored columns | Computed columns |
|-------|---------|------------------|
| `slips` | `slip_id`, `dock`, `length_m`, `power_amps` | `label` |
| `vessels` | `name`, `loa_m`, `owner`, `note_bin` | `id`, `size` |
| `bookings` | `slip_id`, `vessel_name`, `loa_m`, `nights` | `id`, `fee`, `band` |

**API routes** (service `marina_api`)

| Method | Path | Kind | Backed by | Notes |
|--------|------|------|-----------|-------|
| `POST` | `/slips` | insert | `Slips` |  |
| `POST` | `/vessels` | insert | `Vessels` |  |
| `POST` | `/bookings` | insert | `Bookings` |  |
| `POST` | `/bookings/extend` | update | `Bookings` |  |
| `POST` | `/bookings/cancel` | delete | `Bookings` |  |
| `POST` | `/band` | compute | `Bookings` |  |
| `POST` | `/quote` | compute | `Bookings` |  |
| `GET` | `/slips/fit` | query | `slips_that_fit` |  |
| `GET` | `/slips/bookings` | query | `slip_bookings` |  |

## Quickstart

Requires Python 3.11+ and `pixeltable[serve]>=0.7.14`.

```bash
git clone https://github.com/pierrebrunelle/pixeltable-marina-berths.git
cd pixeltable-marina-berths
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Create the tables in a local catalog directory named `marina`
pxt schema update app.py marina

python seed.py marina
pxt service run app.py marina --port 8000   # open http://localhost:8000/docs
python client_demo.py                      # in another terminal
pxt get marina/slips A-12                  # string primary key lookup
```

Try it:

```bash
curl -s -X POST localhost:8000/quote -H 'Content-Type: application/json' -d '{"loa_m": 11.0, "nights": 7}'
curl -s 'localhost:8000/slips/fit?loa_m=12'
```

## Deploy to Pixeltable Cloud

The same `app.py` runs on [Pixeltable Cloud](https://pixeltable.com). Sign in (or get a free trial database with `pxt new`), point the second database entry in `pixeltable.toml` at your own database, then deploy:

```bash
pxt login                       # or: export PIXELTABLE_API_KEY=<your-api-key>
# edit pixeltable.toml: name = 'pxt://<your-org>:<your-db>'
pxt db update pxt://<your-org>:<your-db>                 # build the image and upload the project
pxt schema update app.py pxt://<your-org>:<your-db>/marina   # create the tables in the hosted database
pxt service update app.py pxt://<your-org>:<your-db>/marina  # start the API there
pxt service list pxt://<your-org>:<your-db>              # list hosted services
```

Hosted routes require an API key: send it in the `X-api-key` header (for example `-H "X-api-key: $PIXELTABLE_API_KEY"`). Keep keys in environment variables or `pxt secret set`, never in code.

## Code walkthrough

**1. Business logic is plain Python, in `udfs.py`.** A `@pxt.udf` function can be used as a column expression. Pixeltable records UDFs by module path (`udfs.berth_fee`), so they live in their own importable module rather than inline in the app: the daemon, serving workers and Pixeltable Cloud import it again by that path.

```python
# udfs.py
@pxt.udf
def berth_fee(loa_m: float, nights: int) -> float:
    """Length-overall x nights x rate, with a weekly discount."""
    fee = loa_m * nights * RATE_PER_M_NIGHT
    return round(fee * (0.85 if nights >= 7 else 1.0), 2)
```

**2. Tables are Python classes (`models.py`).** Annotated attributes are stored columns; attributes assigned an expression are **computed columns** (`id`, `fee`, `band`), evaluated incrementally on every insert or update and recomputed when their inputs change.

```python
# models.py
class Bookings(TableModel, name='bookings'):
    id = pxt.Column(value=pxtf.uuid.uuid7(), primary_key=True)
    slip_id: pxt.String
    vessel_name: pxt.String
    loa_m: pxt.Float
    nights: pxt.Int

    fee = berth_fee(loa_m, nights)
    band = stay_band(nights)
```

**3. Queries are functions (`queries.py`).** `@pxt.query` wraps a Pixeltable query so it can be called from Python or exposed as a route:

```python
# queries.py
@pxt.query
def slips_that_fit(loa_m: float):
    """Slips long enough for a vessel, tightest fit first."""
    return Slips.where(Slips.length_m >= loa_m).select(Slips.slip_id, Slips.label, Slips.power_amps).order_by(Slips.length_m)
```

**4. One router, a full REST API.** `FastAPIRouter` generates request/response models from the column types, validates input, and publishes OpenAPI docs at `/docs`:

```python
# app.py
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
# ... more routes in app.py
```

## Learn more

- 🌐 Website: https://pixeltable.com
- 📚 Docs: https://docs.pixeltable.com
- 💻 Source: https://github.com/pixeltable/pixeltable (⭐ star it if Pixeltable is useful to you)
- 📦 PyPI: https://pypi.org/project/pixeltable/

---

<sub>Built as part of a daily series of Pixeltable example apps · Pixeltable 0.7.14 · Python, FastAPI, incremental computed columns · Licensed under Apache-2.0.</sub>
