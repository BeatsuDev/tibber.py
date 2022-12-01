# tibber.py - The Python wrapper for the Tibber API
![MIT license badge](https://img.shields.io/github/license/BeatsuDev/tibber.py)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/BeatsuDev/tibber.py.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/BeatsuDev/tibber.py/context:python)
![Code Coverage](https://img.shields.io/codecov/c/github/BeatsuDev/tibber.py)
[![PyPI version](https://badge.fury.io/py/tibber.py.svg)](https://badge.fury.io/py/tibber.py)
![](https://img.shields.io/librariesio/github/BeatsuDev/tibber.py)
![](https://img.shields.io/pypi/dw/tibber.py)
![](https://img.shields.io/github/contributors-anon/BeatsuDev/tibber.py)

![Tests 3.9](https://github.com/BeatsuDev/tibber.py/actions/workflows/pytest-version-3.9.yml/badge.svg)
![Tests 3.10](https://github.com/BeatsuDev/tibber.py/actions/workflows/pytest-version-3.10.yml/badge.svg)
![Publish to PyPi status](https://github.com/BeatsuDev/tibber.py/actions/workflows/publish-to-pypi.yml/badge.svg)

Head over to https://tibberpy.readthedocs.io/en/latest/ to read the documentation for this library!

tibber.py is a python wrapper package for communication with the [Tibber API](https://developer.tibber.com/).
This package aims to cover all functionalities of the Tibber API in the most beginner-friendly way. You can read all the capabilites of the API and explore it 
with [Tibbers' API explorer](https://developer.tibber.com/explorer). 

Every field of the API types should be found in the corresponding `tibber.type` (e.g. the `size: Int` field of `Home`
type, should be accessed in the tibber.py package as: `Home.size` and return an int). In addition to these "1 to 1",
field to property/method functions, there might be extra properties or methods for simpler access of common properties
(one example: it is possible to simply write `home.address1` instead of `home.address.address1`, although the latter is
also supported). The docstrings of the `tibber.types` correspond to the description of each type in the api explorer
docs (located on the right side of the Tibber API explorer).

## Installation
### Install via pip
```
python -m pip install tibber.py
```
### Requirements
tibber.py depends on `aiohttp`, `gql`, `gql[websockets]` and `graphql-core`. As of now, the project ***requires Python 3.9+***.
Soon the project will most likely support Python 3.7 and up.

## Examples
### Getting basic account data
```python
import tibber

account = tibber.Account(tibber.DEMO_TOKEN) # Log in with an access token. All information gets updated here and stored in cache.

# These properties are retrieved from cache
print(account.name)         # "Arya Stark"
print(account.user_id)      # "dcc2355e-6f55-45c2-beb9-274241fe450c"
print(account.account_type) # ["tibber", "customer"]
print(account.login)        # "arya@winterfell.com"
```

### Getting basic home data
```python
import tibber

account = tibber.Account(tibber.DEMO_TOKEN)
home = account.homes[0]

print(home.id)                     # "cc83e83e-8cbf-4595-9bf7-c3cf192f7d9c"
print(home.time_zone)              # "Europe/Stockholm"
print(home.app_nickname)           # "Vitahuset"
print(home.app_avatar)             # "FLOORHOUSE3"
print(home.size)                   # 195
print(home.type)                   # "HOUSE"
print(home.number_of_residents)    # 5
print(home.primary_heating_source) # "GROUND"
print(home.has_ventilation_system) # False
print(home.main_fuse_size)         # 25
```

### Reading historical data
```python
import tibber

account = tibber.Account(tibber.DEMO_TOKEN)
home = account.homes[0]

# Get the first 10 hours of consumption available
hour_data = home.fetch_consumption("HOURLY", first=10)

# Get the last 3 days of consumption
day_data = home.fetch_consumption("DAILY", last=3)

# Get last 2 months
month_data = home.fetch_consumption("MONTHLY", last=2)

for hour in hour_data:
    print(hour.from_time)
    print(hour.to_time)
    print(f"{hour.unit_price}{hour.currency}")
    print(hour.consumption)
    print(hour.cost)
```

### Reading live measurements
Note how you can register multiple callbacks for the same event. These will be run
in order of which they were registered.
 > INFO: In the future, events should be declared async and all callbacks will be
 > ran asynchronously instead of sequentially.
```python
import tibber

account = tibber.Account(tibber.DEMO_TOKEN)
home = account.homes[0]

@home.event("live_measurement")
def show_current_power(data):
  print(data.power)

# Multiple callback functions for the same event!
@home.event("live_measurement")
def show_accumulated_cost(data):
  print(f"{data.accumulated_cost} {data.currency}")
  
def when_to_stop(data):
  return data.power < 1500

# Start the live feed. This runs until data.power is less than 1500.
home.start_live_feed(exit_condition = when_to_stop)
```
