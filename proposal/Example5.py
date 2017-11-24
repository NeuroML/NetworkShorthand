from networkshorthand import *
from networkshorthand.NetworkGenerator import *


from networkshorthand.BaseTypes import NetworkAdapter
from BBPConnectomeAdapter import BBPConnectomeAdapter

################################################################################
###   Build new network

net = Network(id='bbpNet', notes = 'A network with the Blue Brain Project connectivity data')

default_cell = 'hhcell'
net.network_reader = NetworkReader(type='BBPConnectomeAdapter',
                                   parameters={'filename':'test_files/cons_locs_pathways_mc0_Column.h5',
                                               'max_cells_per_pop':10,
                                               'DEFAULT_CELL_ID':default_cell})
                                               

#net.cells.append(Cell(id=default_cell, neuroml2_source_file='test_files/hhcell.cell.nml'))

cell = Cell(id=default_cell, pynn_cell='EIF_cond_exp_isfa_ista')
cell.parameters = { "tau_refrac":5, "i_offset":.9 }
net.cells.append(cell)

print net.to_json()
net.to_json_file('Example5_%s.json'%net.id)


################################################################################
###   Builds a NeuroML 2 representation, save as XML

generate_neuroml2_from_network(net, 
                               nml_file_name='Example5_%s.net.nml'%net.id)
                               
sim = Simulation(id='SimExample5',
                 duration='100',
                 dt='0.025',
                 recordTraces='all')
                 
#generate_and_run(sim, net, simulator='NEURON')
#generate_and_run(sim, net, simulator='NetPyNE')
#generate_and_run(sim, net, simulator='PyNN_NeuroML')
generate_and_run(sim, net, simulator='PyNN_NEURON')
