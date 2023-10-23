import heapq
from random import Random
from typing import List, Dict

import numpy as np
from networkx import random_regular_graph

from event import Event


class Simulation:

    POISSON_RATE = 1.0       # The rate at which edges are "activated" for a swap
    EXPERIMENT_TIME = 60     # The duration of the experiment, in seconds
    K = 4                    # The degree of the k-regular graph

    def __init__(self, nodes: int, seed: int):
        self.current_time: float = 0
        self.nodes: int = nodes
        self.seed: int = seed
        self.events: List[Event] = []
        self.swaps: int = 0
        self.nb_frequencies: List[int] = [0] * self.nodes
        self.node_to_track: int = Random(self.seed).randint(0, self.nodes - 1)
        heapq.heapify(self.events)

        self.vertex_to_node_map: Dict[int, int] = {}
        self.node_to_vertex_map: Dict[int, int] = {}
        for i in range(self.nodes):
            self.vertex_to_node_map[i] = i
            self.node_to_vertex_map[i] = i

        # Create the topology
        self.G = random_regular_graph(self.K, self.nodes, self.seed)

    def generate_inter_arrival_times(self):
        return np.random.exponential(scale=1 / self.POISSON_RATE)

    def schedule(self, event: Event):
        heapq.heappush(self.events, event)

    def register_neighbours_of_tracked_node(self):
        for nb_vertex in self.G.neighbors(self.node_to_vertex_map[self.node_to_track]):
            nb_peer = self.vertex_to_node_map[nb_vertex]
            self.nb_frequencies[nb_peer] += 1

    def process_event(self, event: Event):
        #print("[t=%.2f] Activating edge (%d - %d)" % (self.current_time, event.from_vertex, event.to_vertex))

        # Swap nodes
        node_at_from_edge: int = self.vertex_to_node_map[event.from_vertex]
        node_at_to_edge: int = self.vertex_to_node_map[event.to_vertex]
        self.vertex_to_node_map[event.from_vertex] = node_at_to_edge
        self.vertex_to_node_map[event.to_vertex] = node_at_from_edge
        self.node_to_vertex_map[node_at_from_edge] = event.to_vertex
        self.node_to_vertex_map[node_at_to_edge] = event.from_vertex
        self.swaps += 1

        # Schedule new edge activation
        delay = self.generate_inter_arrival_times()
        event = Event(self.current_time + delay, event.from_vertex, event.to_vertex)
        self.schedule(event)

    def run(self):
        # Create the initial events in the queue, for each edge
        for edge in self.G.edges:
            delay = self.generate_inter_arrival_times()
            event = Event(delay, *edge)
            self.schedule(event)

        while self.events:
            event = heapq.heappop(self.events)
            self.current_time = event.time
            if self.current_time >= self.EXPERIMENT_TIME:
                break
            self.process_event(event)

        self.register_neighbours_of_tracked_node()
