"""Tests for subscribing to real time data"""
import sys
import os
sys.path.insert(0, os.path.abspath('..'))

import pytest

import tibber


@pytest.fixture
def client():
    return tibber.Client(tibber.DEMO_TOKEN)