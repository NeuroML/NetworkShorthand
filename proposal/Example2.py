from networkshorthand import *
from networkshorthand.NetworkGenerator import *
from networkshorthand.DefaultNetworkHandler import DefaultNetworkHandler

import logging
logging.basicConfig(level=logging.DEBUG, format="%(name)-19s %(levelname)-5s - %(message)s")

from Example1 import net


################################################################################
###   Add some elements to the network

net.populations[0].random_layout = RandomLayout(x=1000,y=100,z=1000)
net.populations[1].random_layout = RandomLayout(x=1000,y=1000,z=1000)

net.cells.append(Cell(id='iaf', neuroml2_source_file='test_files/iaf.cell.nml'))
net.synapses.append(Synapse(id='ampa', neuroml2_source_file='test_files/ampa.synapse.nml'))

print net.to_json()
net.to_json_file('Example2_%s.json'%net.id)


################################################################################
###   Use a handler which just prints info on positions, etc.

def_handler = DefaultNetworkHandler()

generate_network(net, def_handler)


################################################################################
###   Builds a NeuroML 2 representation

generate_neuroml2_from_network(net, nml_file_name='Example2_%s.net.nml'%net.id)

