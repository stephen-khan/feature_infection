"""
Khan Academy coding project
Infection

Control release of changes to coaches and students

Glossary
infection - Assignment of an infector to an entity
infector - Label that can be used to infect an entity
infectable - Entity that can be infected
"""
from operator import itemgetter
from collections import defaultdict

import networkx as nx
from . import subset_sum as ss


def _generate_connection_graph(users):
    """Convert a list of users into a graph using coaching relationships as the edges"""
    user_graph = nx.Graph()
    for user in users:
        user_graph.add_node(user)
        for coached_student in user.connections:
            user_graph.add_edge(user, coached_student)
    return user_graph


class Infector(object):
    """Feature"""

    def __init__(self, control, name):
        """Create named feature"""
        self.control = control
        self.name = name

    @staticmethod
    def _generate_graph(infectables, connections=iter):
        """Convert a list of users into a graph using coaching relationships as the edges"""
        if isinstance(infectables, nx.Graph):
            return infectables

        infectables_graph = nx.Graph()
        for infectable in infectables:
            infectables_graph.add_node(infectable)
            for connected_infectable in connections(infectable):
                infectables_graph.add_edge(infectable, connected_infectable)
        return infectables_graph

    def _get_total_infection_plan(self, infectables, initial_infected):
        """Create a plan for infecting all user connected to an initial infectable"""
        connected = nx.node_connected_component(infectables, initial_infected)
        return connected

    def _get_limited_infection_plan(self, infectables, target_size):
        groups = [(len(group), group)
                  for group in nx.connected_components(infectables)]
        get_count = itemgetter(0)
        get_users = itemgetter(1)
        _, infection_groups = ss.optimize(groups, target_size, key=get_count)
        infected = map(get_users, infection_groups)
        infection_plan = set.union(*infected) if infected else set()
        print infection_plan
        return infection_plan

    def total_infection(self, infectables_seq, initial_infected, connections=None):
        """Create an infection of all users connected to the target user"""
        if not infectables_seq:
            return set()

        infectables = self._generate_graph(infectables_seq, connections)
        plan = self._get_total_infection_plan(infectables, initial_infected)
        self.control.infect(self, *plan)
        return plan

    def limited_infection(self, infectables_seq, target_size, connections=None):
        """Create an infection that is bounded by the target size"""
        if not infectables_seq:
            return set()

        infectables = self._generate_graph(infectables_seq, connections)
        plan = self._get_limited_infection_plan(infectables, target_size)
        self.control.infect(self, *plan)
        return plan

    def is_infected(self, infectable):
        """Create an infection"""
        return self.control.has_infection(infectable, self)


class InfectionControl(object):
    """Manage infections for a collection of objects"""

    def __init__(self):
        """Create an infection controller"""
        self.infectors = {}
        self.infections = defaultdict(list)

    @staticmethod
    def _get_tag(infector):
        return infector if isinstance(infector, basestring) else infector.name

    def get_infector(self, name):
        """Get or create a feature"""
        return self.infectors.setdefault(name, Infector(self, name))

    def infect(self, infector, *infectables):
        infection_tag = self._get_tag(infector)
        for infectable in infectables:
            self.infections[infectable].append(infection_tag)

    def has_infection(self, infectable, infector):
        """Check if an object has an infection"""
        return self._get_tag(infector) in self.infections.get(infectable, [])


CDC = InfectionControl()
