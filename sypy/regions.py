#    SyPy: A Python framework for evaluating graph-based Sybil detection
#    algorithms in social and information networks.
#
#    Copyright (C) 2013  Yazan Boshmaf
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

from graphs import *
from stats import *

import random
import networkx as nx
import matplotlib.pyplot as plt


class Region:

    def __init__(self, graph, name, is_sybil=False):
        self.graph = graph
        self.name = name
        self.is_sybil = is_sybil
        self.known_honests = None

    def pick_random_honest_nodes(self, num_nodes=1, seed=None):
        if self.is_sybil:
            raise Exception("Cannot pick honest nodes in a Sybil region")

        if num_nodes > self.graph.order():
            raise Exception("Too many honest nodes to pick")

        if seed:
            random.seed(seed)

        self.known_honests = random.sample(
            self.graph.nodes(),
            num_nodes
        )

    def visualize(self, file_name=None, file_format="pdf"):
        layout = nx.spring_layout(self.graph.structure)

        node_color = "green"
        label = "Honest"
        if self.is_sybil:
            node_color = "red"
            label = "Sybil"

        handles = []
        nodes_handle = nx.draw_networkx_nodes(
            self.graph.structure,
            layout,
            node_size=150,
            node_color=node_color
        )
        nodes_handle.set_label(label)
        handles.append(nodes_handle)

        if not self.is_sybil:
            known_handle = nx.draw_networkx_nodes(
                self.graph.structure,
                layout,
                nodelist=self.known_honests,
                node_color="orange",
                node_size=150
            )
            known_handle.set_label("Known")
            handles.append(known_handle)

        nx.draw_networkx_edges(
            self.graph.structure,
            layout,
            edge_color="black",
            alpha=0.5
        )

        labels = [handle.get_label() for handle in handles]
        plt.legend(
            handles,
            labels,
            scatterpoints=1
        )
        plt.title("{0}".format(self.name))
        plt.axis('off')

        if file_name:
            plt.savefig(
                "{0}.{1}".format(file_name, file_format),
                format=file_format
            )
            plt.clf()
        else:
            plt.show()