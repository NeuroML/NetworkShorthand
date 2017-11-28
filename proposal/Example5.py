from networkshorthand import *
from networkshorthand.NetworkGenerator import *


################################################################################
###   Build new network

net = Network(id='Example5_bbpNet', notes = 'A network with the Blue Brain Project connectivity data')

default_cell = 'hhcell'
net.network_reader = NetworkReader(type='BBPConnectomeReader',
                                   parameters={'filename':'test_files/cons_locs_pathways_mc0_Column.h5',
                                               'max_cells_per_pop':5,
                                               'DEFAULT_CELL_ID':default_cell})
                                               

#net.cells.append(Cell(id=default_cell, neuroml2_source_file='test_files/hhcell.cell.nml'))

cell = Cell(id=default_cell, pynn_cell='IF_cond_alpha')
cell.parameters = { "tau_refrac":5, "i_offset":0 }
net.cells.append(cell)

input_source = InputSource(id='iclamp0', 
                           pynn_input='DCSource', 
                           parameters={'amplitude':1, 'start':50., 'stop':400.})
net.input_sources.append(input_source)

net.inputs.append(Input(id='stim_L4',
                        input_source=input_source.id,
                        population='L4_PC',
                        percentage=80))

print net.to_json()
net.to_json_file('Example5_%s.json'%net.id)


################################################################################
###   Builds a NeuroML 2 representation, save as XML

generate_neuroml2_from_network(net, 
                               nml_file_name='%s.net.nml'%net.id)
                               
sim = Simulation(id='SimExample5',
                 duration='500',
                 dt='0.025',
                 recordTraces='all')
                 
#generate_and_run(sim, net, simulator='NEURON')
#generate_and_run(sim, net, simulator='NetPyNE')
generate_and_run(sim, net, simulator='PyNN_NeuroML')
generate_and_run(sim, net, simulator='PyNN_NEURON')
