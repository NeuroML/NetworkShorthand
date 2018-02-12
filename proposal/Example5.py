from networkshorthand import Network, Cell, Synapse, NetworkReader, InputSource, Input
from networkshorthand.NetworkGenerator import generate_neuroml2_from_network


################################################################################
###   Build new network

percent = 5
net = Network(id='BBP_%spercent'%percent, notes = 'A network with the Blue Brain Project connectivity data (%s% of total cells)')

default_cell = 'hhcell'
net.network_reader = NetworkReader(type='BBPConnectomeReader',
                                   parameters={'filename':'test_files/cons_locs_pathways_mc0_Column.h5',
                                               'percentage_cells_per_pop':percent,
                                               'DEFAULT_CELL_ID':default_cell,
                                               'id':net.id})
                            
net.cells.append(Cell(id=default_cell, neuroml2_source_file='test_files/hhcell.cell.nml'))
net.synapses.append(Synapse(id='ampa', neuroml2_source_file='test_files/ampa.synapse.nml'))
net.synapses.append(Synapse(id='gaba', neuroml2_source_file='test_files/gaba.synapse.nml'))

                            
input_source = InputSource(id='poissonFiringSyn', neuroml2_source_file='test_files/inputs.nml')
net.input_sources.append(input_source)

for pop in ['L23_PC']:
    net.inputs.append(Input(id='stim_%s'%pop,
                            input_source=input_source.id,
                            population=pop,
                            percentage=80))

print net.to_json()
net.to_json_file('%s.json'%net.id)


################################################################################
###   Builds a NeuroML 2 representation, save as XML

format_='xml'
generate_neuroml2_from_network(net, 
                               nml_file_name='%s.net.nml%s'%(net.id, '.h5' if format_=='hdf5' else ''), 
                               format=format_)
 
exit()

from networkshorthand import Simulation
from networkshorthand.NetworkGenerator import generate_and_run
sim = Simulation(id='SimExample5',
                 duration='100',
                 dt='0.025',
                 recordTraces='all')
                               
generate_and_run(sim, net, simulator='NetPyNE')
'''                    
generate_and_run(sim, net, simulator='jNeuroML_NEURON')
                 
#generate_and_run(sim, net, simulator='NEURON')
generate_and_run(sim, net, simulator='PyNN_NeuroML')
#generate_and_run(sim, net, simulator='PyNN_NEURON')'''
