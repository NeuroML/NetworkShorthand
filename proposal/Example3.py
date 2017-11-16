from networkshorthand import *
from networkshorthand.NetworkGenerator import *

################################################################################
###   Reuse network from Example1

from Example2 import net
net.id = 'Example3_Network'


################################################################################
###   Build Simulation object & save as JSON


sim = Simulation(id='SimExample3',
                 duration='1000',
                 dt='0.025',
                 recordTraces='all')
                 
sim.to_json_file()


################################################################################
###   Run in some simulators

generate_and_run(sim, net, simulator='jNeuroML')

generate_and_run(sim, net, simulator='jNeuroML_NEURON')

generate_and_run(sim, net, simulator='NetPyNE')

#generate_and_run(sim, net, simulator='NEURON')







