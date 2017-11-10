from networkshorthand import *

from Example2 import net
net.id = 'Example3_Network'

sim = Simulation(id='Example3',
                 duration='100',
                 dt='0.025',
                 recordTraces='all')
                 
sim.to_json_file()


sim.generate_and_run(net, simulator='jNeuroML')





