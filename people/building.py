from people import Activity


class Building():
    """A Building of the city.

    Parameters:
        * location: a people.Vector giving the x,y coordinates of the building
    """

    def __init__(self, location):
        self.location = location
