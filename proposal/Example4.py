from networkshorthand import *
from networkshorthand.NetworkGenerator import *

################################################################################
###   Build new network

net = Network(id='pynnNet', notes = 'A network for PyNN')

cell = Cell(id='testcell', pynn_cell='EIF_cond_exp_isfa_ista')
cell.parameters = { "tau_refrac":5, "i_offset":0 }
net.cells.append(cell)

input_source = InputSource(id='iclamp0', 
                           pynn_input='DCSource', 
                           parameters={'amplitude':1, 'start':200, 'stop':800})
net.input_sources.append(input_source)


p0 = Population(id='pop0', size=1, component=cell.id)
p1 = Population(id='pop1', size=1, component=cell.id)

net.populations.append(p0)
net.populations.append(p1)

net.projections.append(Projection(id='proj0',
                                  presynaptic=p0.id, 
                                  postsynaptic=p1.id,
                                  synapse='ampa',
                                  delay=2,
                                  weight=0.0002))
net.projections[0].random_connectivity=RandomConnectivity(probability=1)

net.inputs.append(Input(id='stim',
                        input_source=input_source.id,
                        population=p0.id,
                        percentage=100))

print net.to_json()
net.to_json_file('Example4_%s.json'%net.id)

################################################################################
###   Build Simulation object & save as JSON


sim = Simulation(id='SimExample4',
                 duration='1000',
                 dt='0.025',
                 recordTraces='all')
                 
sim.to_json_file()


################################################################################
###   Run in some simulators

print("**** Generating and running in NeuroML ****")

generate_and_run(sim, net, simulator='PyNN_NEURON')
'''
generate_and_run(sim, net, simulator='PyNN_Brian')
generate_and_run(sim, net, simulator='PyNN_NEST')
generate_and_run(sim, net, simulator='PyNN_NEST')
generate_and_run(sim, net, simulator='PyNN_NeuroML')
generate_and_run(sim, net, simulator='PyNN_NeuroML')
generate_and_run(sim, net, simulator='PyNN_NEURON')
print("**** Generating and running in NEURON ****")


print("**** Generating and running in NEST ****")

generate_and_run(sim, net, simulator='PyNN_NEST')

print("**** Generating and running in Brian ****")
'''







