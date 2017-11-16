from networkshorthand import *
from networkshorthand.NetworkGenerator import *
from networkshorthand.DefaultNetworkHandler import DefaultNetworkHandler

################################################################################
###   Reuse network from Example1

from Example1 import net


################################################################################
###   Add some elements to the network & save new JSON

net.populations[0].random_layout = RandomLayout(x=1000,y=100,z=1000)
net.populations[1].random_layout = RandomLayout(x=1000,y=1000,z=1000)

net.populations[0].component = 'hhcell'
net.populations[1].component = 'hhcell'

net.cells.append(Cell(id='hhcell', neuroml2_source_file='test_files/hhcell.cell.nml'))
net.synapses.append(Synapse(id='ampa', neuroml2_source_file='test_files/ampa.synapse.nml'))

print net.to_json()
net.to_json_file('Example2_%s.json'%net.id)


################################################################################
###   Use a handler which just prints info on positions, etc.

def_handler = DefaultNetworkHandler()

generate_network(net, def_handler)


################################################################################
###   Builds a NeuroML 2 representation, save as XML

generate_neuroml2_from_network(net, 
                               nml_file_name='Example2_%s.net.nml'%net.id)

################################################################################
###   Builds a NeuroML 2 representation, save as HDF5

generate_neuroml2_from_network(net, 
                               nml_file_name='Example2_%s.net.nml.h5'%net.id,
                               format='hdf5')
                               