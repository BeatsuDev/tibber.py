# tibber.py - The Python wrapper for the Tibber API
![MIT license badge](https://img.shields.io/github/license/BeatsuDev/tibber.py)
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
tibber.py depends on `gql`, `gql[aiohttp]`, `gql[websockets]` and `graphql-core`. tibber.py supports Python versions 3.7 and up!

## Examples
### Getting basic account data
```python
import tibber

account = tibber.Account(tibber.DEMO_TOKEN) # Log in with an access token. All information gets updated here and stored in cache.

# These properties are retrieved from cache and DO NOT reflect data at the given time
# (but rather the data as it was when it last was cached)
print(account.name)         # "Arya Stark"
print(account.user_id)      # "dcc2355e-6f55-45c2-beb9-274241fe450c"
print(account.account_type) # ["tibber", "customer"]
print(account.login)        # "arya@winterfell.com"

# To update the cache with new data straight from the tibber api, run this:
account.update()

# Now use the updated data as you would before:
print(account.name)
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
in asynchronously (at the same time)!
```python
import tibber

account = tibber.Account(tibber.DEMO_TOKEN)
home = account.homes[0]

@home.event("live_measurement")
async def show_current_power(data):
  print(data.power)

# Multiple callback functions for the same event!
@home.event("live_measurement")
async def show_accumulated_cost(data):
  print(f"{data.accumulated_cost} {data.currency}")
  
def when_to_stop(data):
  return data.power < 1500

# Start the live feed. This runs until data.power is less than 1500.
# If a user agent was not defined earlier, this will be required here
home.start_live_feed(user_agent = "UserAgent/0.0.1", exit_condition = when_to_stop) 
```

## Contributing to the project
I'm glad to see you're interested in contributing! When programming, I tend to follow some style guides
and urge you to do the same. Here are two important videos which cover the most important styles to follow
and how to do so. [Never nest](https://www.youtube.com/watch?v=CFRhGnuXG-4), [How to name variables](https://www.youtube.com/watch?v=-J3wNP6u5YU).

To start contributing to the project, create your own fork of this repository on GitHub by clicking "Fork"
in the top right corner. Clone your fork of this project to your own computer using [git](https://git-scm.com/).
Now create a new branch named a short 1-3 word long name, hyphenated (this-is-hyphenated), and prefixed with
one of these:
 - `refactor/` - A refactoring of pre-existing code
 - `bug/` - Fixing a bug
 - `feature/` - Adding a feature
 - `other/` - If it really doesn't fit any of the above

Here are some example branch names:
 - `refactor/async-callbacks`
 - `bug/query-execution`
 - `feature/live-data`
 
Once you have created a new branch, play around, code your changes and then add a pull request back to this
GitHub repository!
