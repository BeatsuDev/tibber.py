"""Tests for reading tibber.Client properties from cached values after the Tibber client is initialized."""
import pytest

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join('..', '..')))

import tibber


@pytest.fixture
def client():
    return tibber.Client(tibber.DEMO_TOKEN)


def test_getting_name(client):
    assert client.name == "Arya Stark"
    
def test_getting_login(client):
    assert client.login == "edgeir@tibber.com"
    
def test_getting_user_id(client):
    assert client.user_id == "df4b53bf-0709-4679-8744-08876cbb03c1"

def test_getting_account_type(client):
    assert client.account_type == ["tibber", "customer"]
    
def test_getting_homes(client):
    assert len(client.homes) == 1