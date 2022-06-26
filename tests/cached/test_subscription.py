"""Tests for reading tibber.types.Subscription properties from cached values after the Tibber account is initialized."""
import pytest

import tibber
from tibber.types import Subscription
from tibber.types import LegalEntity
from tibber.types import PriceInfo
from tibber.types import PriceRating


@pytest.fixture
def subscription():
    account = tibber.Account(tibber.DEMO_TOKEN)
    try:
        return account.homes[0].current_subscription
    except IndexError:
        raise ValueError("The instanciated demo account does not have any homes. Cannot perform home tests.")


def test_correct_type(subscription):
    assert isinstance(subscription, Subscription)

def test_getting_id(subscription):
    assert subscription.id == "e9c0f9eb-4a7d-447f-8598-0794c33ca5aa"

def test_getting_subscriber(subscription):
    assert isinstance(subscription.subscriber, LegalEntity)

def test_getting_valid_from(subscription):
    assert subscription.valid_from == "2020-04-26T22:00:00+00:00"

def test_getting_status(subscription):
    assert subscription.status == "running"

def test_getting_price_info(subscription):
    assert isinstance(subscription.price_info, PriceInfo)

def test_getting_price_rating(subscription):
    assert isinstance(subscription.price_rating, PriceRating)