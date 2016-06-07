"""
Feature Infection

Control release of changes to groups of users

This module provides the entities for the feature infection
module.  Infections are tags that can be applied to entities
while respecting clustering relationships between users.

Exports:
    Infector: class that represents a named feature
    InfectionControl: scope for registering infections on entities
    CDC: module scoped InfectionControl instance (a pun on
        the center for disease control)

Usage:
    Generally, users will use the module scoped CDC to do an infection
    >>> User = collections.namedtuple("User", "name coaches")
    >>> user1 = User("one", ())
    >>> user2 = User("two", ("one"))
    >>> user3 = User("three", ())
    >>> users = [user1, user2, user3]
    >>> coaches = operator.itemgetter("coaches")
    >>> super_learning = feature_infection.CDC.get_infector("super-learning")
    >>> super_learning.total_infection(users, user1, connections=coaches)
    set([User(name='one', coaches=()), User(name='two', coaches=User(name=\
'one, coaches=()))])

Glossary:
    infection - Assignment of an infector to an entity
    infector - Label that can be used to infect an entity
    infectable - Entity that can be infected
"""
from operator import itemgetter
from collections import defaultdict
import logging

import networkx as nx
from . import subset_sum as ss


_LOG = logging.getLogger(__name__)


class Infector(object):
    """Class representing a feature or other tag to apply to entities"""

    def __init__(self, control, name):
        """Create named feature and tie it to an InfectionControl scope"""
        self.control = control
        self.name = name

    @staticmethod
    def _generate_graph(infectables, connections=iter):
        """Convert a list of infectables into a graph via connections"""
        if not callable(connections):
            raise ValueError("connections is not a function")

        if isinstance(infectables, nx.Graph):
            return infectables

        infectables_graph = nx.Graph()
        for infectable in infectables:
            infectables_graph.add_node(infectable)
            for connected_infectable in connections(infectable):
                infectables_graph.add_edge(infectable, connected_infectable)
        return infectables_graph

    @staticmethod
    def _get_total_infection_plan(infectables, initial_infected):
        """Plan for infecting everything connected to an initial infectable"""
        connected = nx.node_connected_component(infectables, initial_infected)
        return connected

    @staticmethod
    def _get_limited_infection_plan(infectables, target_size):
        """Plan for infecting a group infectables no larger than target_size"""
        groups = [(len(group), group)
                  for group in nx.connected_components(infectables)]
        get_count = itemgetter(0)
        get_users = itemgetter(1)
        _, infection_groups = ss.optimize(groups, target_size, key=get_count)
        infected = map(get_users, infection_groups)
        infection_plan = set.union(*infected) if infected else set()
        return infection_plan

    def total_infection(self, infectables_seq, initial_infected,
                        connections=None):
        """Create an infection of all users connected to the target user.

        Starting at the root provided by initial_infected, infect all the
        connected infectable entities in the infectables graph

        Args:
            infectables_seq: list or graph of infectables.  If a list is
                provided it will be converted to a graph with edges
                defined by using the connections parmeter
            inital_infected: infectable to form the root of the infection
            (optional) connections: function that produces adjacent
                infectables for a given infectable.  The produced graph
                is undirected but connections only is required to produce
                adjecency in one direction.

        Returns:
            set infected: returns a set of the infectables that were infected

        Raises:
            ValueError: connection is not a function
        """
        if not infectables_seq:
            return set()

        infectables = self._generate_graph(infectables_seq, connections)
        plan = self._get_total_infection_plan(infectables, initial_infected)
        self.control.infect(self, *plan)
        return plan

    def limited_infection(self, infectables_seq, target_size,
                          connections=None):
        """Create an infection that is bounded by the target size

        Finds a subset of infectables that approximates as well as
        possible an infection of the target_size.

        This function will not break apart groups to get closer to
        the target_size.  Callers who need a closer approximation in
        the presence of a large connected cluster will need to provide
        a pruned connections function.

        Args:
            infectables_seq: list or graph of infectables.  If a list is
                provided it will be converted to a graph with edges
                defined by using the connections parmeter
            target_size: limit to the number of infected produced
            (optional) connections: function that produces adjacent
                infectables for a given infectable.  The produced graph
                is undirected but connections only is required to produce
                adjecency in one direction.

        Returns:
            set infected: returns a set of the infectables that were infected

        Raises:
            ValueError: connection is not a function
        """
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
        """Infect all provided infectables with the given feature."""
        infection_tag = self._get_tag(infector)
        for infectable in infectables:
            self.infections[infectable].append(infection_tag)
            _LOG.info("User %s infected with feature %s.", infectable,
                      infection_tag)

    def has_infection(self, infectable, infector):
        """Check if an infectable entity has an infection"""
        return self._get_tag(infector) in self.infections.get(infectable, [])


CDC = InfectionControl()
