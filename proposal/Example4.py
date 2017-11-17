from networkshorthand import *
from networkshorthand.NetworkGenerator import *

################################################################################
###   Build new network

net = Network(id='pynnNet', notes = 'A network for PyNN')

hhcell = Cell(id='pynnhhcell', pynn_cell='HH_cond_exp')
net.cells.append(hhcell)

p0 = Population(id='pop0', size=5, component=hhcell.id)
p1 = Population(id='pop1', size=10, component=hhcell.id)

net.populations.append(p0)
net.populations.append(p1)

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

generate_and_run(sim, net, simulator='PyNN_NeuroML')

print("**** Generating and running in NEURON ****")

generate_and_run(sim, net, simulator='PyNN_NEURON')

print("**** Generating and running in NEST ****")

generate_and_run(sim, net, simulator='PyNN_NEST')

print("**** Generating and running in Brian ****")

generate_and_run(sim, net, simulator='PyNN_Brian')







