"""Tests for reading tibber.types.LegalEntity properties from cached values after the Tibber account is initialized."""
import pytest

import tibber
from tibber.types import LegalEntity

@pytest.fixture
def legal_entity():
    account = tibber.Account(tibber.DEMO_TOKEN)
    try:
        return account.homes[0].owner
    except IndexError:
        raise ValueError("The instanciated demo account does not have any homes. Cannot perform home tests.")

def test_correct_type(legal_entity):
    assert isinstance(legal_entity, LegalEntity)

def test_getting_id(legal_entity):
    assert legal_entity.id == "df4b53bf-0709-4679-8744-08876cbb03c1"

def test_getting_first_name(legal_entity):
    assert legal_entity.first_name == "Arya"

def test_getting_name(legal_entity):
    assert legal_entity.name == "Arya Stark"

def test_getting_last_name(legal_entity):
    assert legal_entity.last_name == "Stark"

def test_getting_contact_info(legal_entity):
    assert legal_entity.contact_info.email == "arya@winterfell.com"