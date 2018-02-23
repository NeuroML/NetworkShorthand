from networkshorthand import Network, Cell, InputSource, Population
from networkshorthand import Projection, RandomConnectivity, Input, Simulation
from networkshorthand.NetworkGenerator import generate_and_run
import sys

################################################################################
###   Build new network

net = Network(id='Example4_PyNN')
net.notes = 'Example 4: a network with PyNN cells & inputs'

cell = Cell(id='testcell', pynn_cell='IF_cond_alpha')
cell.parameters = { "tau_refrac":5, "i_offset":.1 }
net.cells.append(cell)

cell2 = Cell(id='testcell2', pynn_cell='IF_cond_alpha')
cell2.parameters = { "tau_refrac":5, "i_offset":-.1 }
net.cells.append(cell2)

input_source = InputSource(id='iclamp0', 
                           pynn_input='DCSource', 
                           parameters={'amplitude':0.99, 'start':200., 'stop':800.})
net.input_sources.append(input_source)


p0 = Population(id='pop0', size=2, component=cell.id)
p1 = Population(id='pop1', size=2, component=cell2.id)

net.populations.append(p0)
net.populations.append(p1)

net.projections.append(Projection(id='proj0',
                                  presynaptic=p0.id, 
                                  postsynaptic=p1.id,
                                  synapse='ampa',
                                  delay=2,
                                  weight=0.02))
net.projections[0].random_connectivity=RandomConnectivity(probability=1)

net.inputs.append(Input(id='stim',
                        input_source=input_source.id,
                        population=p0.id,
                        percentage=70))

print net.to_json()
net.to_json_file('%s.json'%net.id)

################################################################################
###   Build Simulation object & save as JSON


sim = Simulation(id='SimExample4',
                 duration='1000',
                 dt='0.025',
                 recordTraces='all')
                 
sim.to_json_file()


################################################################################
###   Run in some simulators

print("**** Generating and running ****")


if '-pynnnest' in sys.argv:
    generate_and_run(sim, net, simulator='PyNN_NEST')
    
elif '-pynnnrn' in sys.argv:
    generate_and_run(sim, net, simulator='PyNN_NEURON')
    
elif '-pynnbrian' in sys.argv:
    generate_and_run(sim, net, simulator='PyNN_Brian')
    
#elif '-jnml' in sys.argv:
#    generate_and_run(sim, net, simulator='jNeuroML')
    
else:
    generate_and_run(sim, net, simulator='PyNN_NeuroML')



'''
generate_and_run(sim, net, simulator='PyNN_NEURON')
generate_and_run(sim, net, simulator='PyNN_NEST')
generate_and_run(sim, net, simulator='PyNN_Brian')

generate_and_run(sim, net, simulator='PyNN_NEST')
generate_and_run(sim, net, simulator='PyNN_NeuroML')
generate_and_run(sim, net, simulator='PyNN_NEURON')
print("**** Generating and running in NEURON ****")


print("**** Generating and running in NEST ****")

generate_and_run(sim, net, simulator='PyNN_NEST')

print("**** Generating and running in Brian ****")
'''







