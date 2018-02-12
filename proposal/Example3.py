from networkshorthand import *
from networkshorthand.NetworkGenerator import *
from networkshorthand.utils import load_network_json
import sys

################################################################################
###   Reuse network from Example2

filename = 'Example2_TestNetwork.json'
net = load_network_json(filename)
net.id = 'Example3_Network'
print net

################################################################################
###   Build Simulation object & save as JSON


sim = Simulation(id='SimExample3',
                 duration='1000',
                 dt='0.025',
                 recordTraces='all')
                 
sim.to_json_file()


################################################################################
###   Run in some simulators

if '-netpyne' in sys.argv:
    generate_and_run(sim, net, simulator='NetPyNE')
    
else:
    
    generate_and_run(sim, net, simulator='jNeuroML')

#generate_and_run(sim, net, simulator='jNeuroML_NEURON')


#generate_and_run(sim, net, simulator='NEURON')







