# tibber.py - The Python wrapper for the Tibber API
![MIT license badge](https://img.shields.io/github/license/BeatsuDev/tibber.py)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/BeatsuDev/tibber.py.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/BeatsuDev/tibber.py/context:python)
![Code Coverage](https://img.shields.io/codecov/c/github/BeatsuDev/tibber.py)
[![PyPI version](https://badge.fury.io/py/tibber.py.svg)](https://badge.fury.io/py/tibber.py)

![Tests 3.9](https://github.com/BeatsuDev/tibber.py/actions/workflows/pytest-version-3.9.yml/badge.svg)
![Tests 3.10](https://github.com/BeatsuDev/tibber.py/actions/workflows/pytest-version-3.10.yml/badge.svg)
![Publish to PyPi status](https://github.com/BeatsuDev/tibber.py/actions/workflows/publish-to-pypi.yml/badge.svg)

A python wrapper package for communication with the [Tibber API](https://developer.tibber.com/). This package aims to cover all functionalities of the Tibber API. 

## Installation
### Install via pip
```
python -m pip install tibber.py
```
### Requirements
tibber.py depends only on aiohttp and websockets. As of now, the project requires Python 3.9+ as well (this might change in the future to support Python 3.7+).

## Examples
### Getting basic client data
```python
import tibber

client = tibber.Client(tibber.DEMO_TOKEN) # Log in with an access token. All information gets updated here and stored in cache.

# These properties are retrieved from cache
print(client.name)         # "Arya Stark"
print(client.user_id)      # "df4b53bf-0709-4679-8744-08876cbb03c1"
print(client.account_type) # ["tibber", "customer"]
print(client.login)        # "edgeir@tibber.com"
```

### Getting basic home data
```python
import tibber

client = tibber.Client(tibber.DEMO_TOKEN)
home = client.homes[0]

print(home.id)                     # "cc83e83e-8cbf-4595-9bf7-c3cf192f7d9c"
print(home.time_zone)              # "Europe/Oslo"
print(home.app_nickname)           # "Ulltang casa"
print(home.app_avatar)             # "FLOORHOUSE2"
print(home.size)                   # 200
print(home.type)                   # "HOUSE"
print(home.number_of_residents)    # 4
print(home.primary_heating_source) # "AIR2AIR_HEATPUMP"
print(home.has_ventilation_system) # True
print(home.main_fuse_size)         # 63
```
### Reading live measurements
Note how you can register multiple callbacks for the same event. These will be run
in order of which they were registered.
 > INFO: In the future, events should be declared async and all callbacks will be
 > ran asynchronously instead of sequentially.
```python
import tibber

client = tibber.Client(tibber.DEMO_TOKEN)
home = client.homes[0]

@home.event("consumption")
def show_current_power(data):
  print(data.power)

# Multiple callback functions for the same event!
@home.event("consumption")
def show_accumulated_cost(data):
  print(f"{data.accumulated_cost} {data.currency}")
  
# Start the live feed. This runs forever.
home.start_livefeed()
```
## 100% API coverage TODO / Progress list
All the API features are documented here: https://developer.tibber.com/docs/reference
- [x] Address
- [x] Consumption
- [x] ContactInfo
- [x] Home
- [x] HomeConsumptionConnection
- [x] HomeConsumptionEdge
- [x] HomeConsumptionPageInfo
- [x] HomeFeatures
- [x] HomeProductionConnection
- [x] HomeProductionEdge
- [x] HomeProductionPageInfo
- [x] LegalEntity
- [x] LiveMeasurement
- [ ] MeterReadingResponse
- [x] MeteringPointData
- [x] Price
- [x] PriceInfo
- [x] PriceRating
- [x] PriceRatingEntry
- [x] PriceRatingThresholdPercentages
- [x] PriceRatingType
- [x] Production
- [ ] PushNotificationResponse
- [ ] RootMutation
- [ ] RootSubscription
- [x] Subscription
- [ ] SubscriptionPriceConnection
- [ ] SubscriptionPriceConnectionPageInfo
- [ ] SubscriptionPriceEdge
- [x] Viewer
