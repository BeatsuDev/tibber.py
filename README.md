# tibber.py - The Python wrapper for the Tibber API
![MIT license badge](https://img.shields.io/github/license/BeatsuDev/tibber.py)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/BeatsuDev/tibber.py.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/BeatsuDev/tibber.py/context:python)
![Publish to PyPi status](https://github.com/BeatsuDev/tibber.py/actions/workflows/publish-to-pypi.yml/badge.svg)

![Tests 3.9](https://github.com/BeatsuDev/tibber.py/actions/workflows/pytest-version-3.9.yml/badge.svg)
![Tests 3.10](https://github.com/BeatsuDev/tibber.py/actions/workflows/pytest-version-3.10.yml/badge.svg)

A python wrapper module for communication with the [Tibber API](https://developer.tibber.com/). This package requires Python 3.9+ (This may be changed in the future to support 3.7+. For now the simpler solution was simply to require Python 3.9+) and depends only on aiohttp.

## Installation
```
python -m pip install tibber.py
```

## Examples
Getting basic client data:
```python
import tibber

client = tibber.Client(tibber.DEMO_TOKEN) # Log in with an access token. All information gets updated here and stored in cache.

# These properties are retrieved from cache
print(client.name)         # "Arya Stark"
print(client.user_id)      # "df4b53bf-0709-4679-8744-08876cbb03c1"
print(client.account_type) # ["tibber", "customer"]
print(client.login)        # "edgeir@tibber.com"
```

Getting basic home data:
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
