import pytest

from test_person import pseudo_random, sleeping_person
from test_travelling_man import home, work, activity_markov_chains, person

from people import Building, Vector, Activity
from people.location import same_location


@pytest.fixture
def alternative_work():
    return Building(Vector(20020, 0))


@pytest.fixture
def building_query(home, work, alternative_work):
    class BuildingQuery():

        work_places = (work, alternative_work)

        def __call__(self, activity):
            if activity is Activity.SLEEP:
                return (home,)
            else:
                return self.work_places
    return BuildingQuery()


def test_chance_of_choosing_closer_building_is_higher(work, pseudo_random, person):
    pseudo_random.number = 0.66
    person.step()
    assert person.activity == Activity.TRANSIT
    while person.activity == Activity.TRANSIT:
        person.step()
    assert person.location == work.location


def test_chance_of_choosing_further_work_is_lower(alternative_work, pseudo_random, person):
    pseudo_random.number = 0.67
    person.step()
    assert person.activity == Activity.TRANSIT
    while person.activity == Activity.TRANSIT:
        person.step()
    assert person.location == alternative_work.location


@pytest.mark.parametrize("random_number", [(0.0), (0.2), (0.8), (1.0)])
def test_no_travel_if_activity_can_be_performed_locally(person, home, work, alternative_work,
                                                        building_query, random_number,
                                                        pseudo_random):
    pseudo_random.number = random_number
    building_query.work_places = (home, work, alternative_work)
    person.step()
    assert same_location(person.location, home.location)
    assert person.activity == Activity.WORK
