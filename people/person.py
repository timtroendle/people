from enum import Enum

from .location import same_location


class Activity(Enum):
    TRANSIT = 1
    SLEEP = 2
    WORK = 3


class Person():

    def __init__(self, activity_markov_chains, initial_activity, number_generator,
                 initial_time, initial_location, velocity, building_query, time_step_size):
        self.__chain = _TimeHeterogenousMarkovChain(activity_markov_chains, number_generator)
        if not isinstance(initial_activity, Activity):
            raise ValueError('Initial activity must be derived from Activity.')
        self.activity = initial_activity
        self.location = initial_location
        self.__travelling_to = None
        self.__travelling_for = None
        self.__distance_per_step = velocity * time_step_size.total_seconds()
        self.__building_query = building_query
        self.__time = initial_time
        self.__time_step_size = time_step_size

    def step(self):
        self.__time += self.__time_step_size
        if self.activity == Activity.TRANSIT:
            self.location = self.__determine_next_location()
        self.activity = self.__determine_next_activity()

    def __determine_next_location(self):
        vector_to_desired_location = self.__travelling_to - self.location
        if vector_to_desired_location.norm() <= self.__distance_per_step:
            new_location = self.__travelling_to
        else:
            new_location = self.location + \
                vector_to_desired_location.normalize() * self.__distance_per_step
        return new_location

    def __determine_next_activity(self):
        if self.activity == Activity.TRANSIT:
            if not same_location(self.location, self.__travelling_to):
                return Activity.TRANSIT
            else:
                next_activity = self.__travelling_for
                self.__travelling_to = None
                self.__travelling_for = None
                return next_activity
        else:
            next_activity = self.__chain.move(current_state=self.activity, current_time=self.__time)
            if next_activity is not self.activity:
                next_building = self._choose_building(next_activity)
                if not same_location(next_building.location, self.location):
                    self.__travelling_to = next_building.location
                    self.__travelling_for = next_activity
                    return Activity.TRANSIT
                else:
                    return next_activity
            else:
                return next_activity

    def _choose_building(self, activity_choice):
        possible_buildings = self.__building_query(activity_choice)
        assert len(possible_buildings) > 0, "Couldn't find any buildings for \
                                             activity {}.".format(activity_choice)
        return possible_buildings[0]


class _TimeHeterogenousMarkovChain():

    def __init__(self, activity_markov_chains, number_generator):
        self.__number_generator = number_generator
        if 'weekday' not in activity_markov_chains.keys():
            raise ValueError('Activity markov chains have wrong format.')
        if 'weekend' not in activity_markov_chains.keys():
            raise ValueError('Activity markov chains have wrong format.')
        if any(hour not in activity_markov_chains['weekday'] for hour in range(24)):
            raise ValueError('Activity markov chains have wrong format.')
        if any(hour not in activity_markov_chains['weekend'] for hour in range(24)):
            raise ValueError('Activity markov chains have wrong format.')
        self.__chains = {day: activity_markov_chains['weekday'] if day < 5
                         else activity_markov_chains['weekend']
                         for day in range(7)}
        for day in range(7):
            for hour in range(24):
                activities = self.__chains[day][hour].states()
                if not all(isinstance(activity, Activity) for activity in activities):
                    msg = 'At least one activity in {} is not \
                          derived from Activity.'.format(activities)
                    raise ValueError(msg)

    def move(self, current_state, current_time):
        return self._select_chain(current_time).move(
            state=current_state,
            random_func=self.__number_generator
        )

    def _select_chain(self, current_time):
        return self.__chains[current_time.weekday()][current_time.hour]
