from networkshorthand import *
from networkshorthand.NetworkGenerator import *


from networkshorthand.BaseTypes import NetworkAdapter
from BBPConnectomeAdapter import BBPConnectomeAdapter

################################################################################
###   Build new network

net = Network(id='bbpNet', notes = 'A network with the Blue Brain Project connectivity data')

net.network_reader = NetworkReader(type='BBPConnectomeAdapter',
                                   parameters={'filename':'test_files/cons_locs_pathways_mc0_Column.h5',
                                               'max_cells_per_pop':10,
                                               'DEFAULT_CELL_ID':'bbpcell'})

print net.to_json()
net.to_json_file('Example5_%s.json'%net.id)


################################################################################
###   Builds a NeuroML 2 representation, save as XML

generate_neuroml2_from_network(net, 
                               nml_file_name='Example5_%s.net.nml'%net.id)
