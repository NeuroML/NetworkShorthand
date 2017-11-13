from networkshorthand import *
from networkshorthand.NetworkGenerator import *

from Example2 import net
net.id = 'Example3_Network'

sim = Simulation(id='Example3',
                 duration='1000',
                 dt='0.025',
                 recordTraces='all')
                 
sim.to_json_file()


generate_and_run(sim, net, simulator='jNeuroML')





