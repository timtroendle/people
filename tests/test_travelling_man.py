from collections import OrderedDict

import pytest
import pykov

from test_person import pseudo_random, sleeping_person

from people import Activity, Building, Vector
from people.location import distance, same_location


@pytest.fixture
def home():
    return Building(location=Vector(0, 0))


@pytest.fixture
def work():
    return Building(location=Vector(10010, 0))


@pytest.fixture
def building_query(home, work):
    def query(activity):
        if activity is Activity.SLEEP:
            return (home,)
        else:
            return (work,)
    return query


@pytest.fixture
def activity_markov_chains():
    chain = pykov.Chain(OrderedDict([
        ((Activity.SLEEP, Activity.WORK), 1.0),
        ((Activity.SLEEP, Activity.SLEEP), 0.0),
        ((Activity.WORK, Activity.SLEEP), 1.0),
        ((Activity.WORK, Activity.WORK), 0.0)
    ]))
    return {
        'weekday': {hour: chain for hour in range(24)},
        'weekend': {hour: chain for hour in range(24)}
    }


def test_person_starts_commute(sleeping_person):
    sleeping_person.step()
    assert sleeping_person.activity == Activity.TRANSIT


def test_commuting_person_moves_towards_next_building(sleeping_person, work):
    initial_location = sleeping_person.location
    sleeping_person.step()
    sleeping_person.step() # location is updated at the end of a travelling time step
    assert (distance(sleeping_person.location, work.location) <
            distance(initial_location, work.location))


def test_work_not_reached_after_one_time_step(sleeping_person, work):
    sleeping_person.step()
    sleeping_person.step()
    assert not same_location(sleeping_person.location, work.location)
    assert sleeping_person.activity is Activity.TRANSIT


def test_commuting_to_work_takes_two_time_steps(sleeping_person, work):
    sleeping_person.step()
    sleeping_person.step()
    sleeping_person.step()
    assert same_location(sleeping_person.location, work.location)
    assert sleeping_person.activity == Activity.WORK
