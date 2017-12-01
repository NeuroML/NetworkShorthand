from networkshorthand import *
from networkshorthand.NetworkGenerator import *

################################################################################
###   Build new network

net = Network(id='Example6_PyNN', notes = 'Another network for PyNN')

cell = Cell(id='CorticalCell', pynn_cell='IF_curr_exp')
cell.parameters = {
    'cm'        : 0.25,  # nF
    'i_offset'  : 0.0,   # nA
    'tau_m'     : 10.0,  # ms
    'tau_refrac': 2.0,   # ms
    'tau_syn_E' : 0.5,   # ms
    'tau_syn_I' : 0.5,   # ms
    'v_reset'   : -65.0,  # mV
    'v_rest'    : -65.0,  # mV
    'v_thresh'  : -50.0  # mV
}
net.cells.append(cell)

input_cell = Cell(id='InputCell', pynn_cell='SpikeSourcePoisson')
input_cell.parameters = {
    'start':    0,
    'duration': 10000000000,
     'rate':      150
}
net.cells.append(input_cell)


scale = 0.1
l23e = Population(id='L23_E', size=int(100*scale), component=cell.id)
l23i = Population(id='L23_I', size=int(100*scale), component=cell.id)
l23ei = Population(id='L23_E_input', size=int(100*scale), component=input_cell.id)
l23ii = Population(id='L23_I_input', size=int(100*scale), component=input_cell.id)

net.populations.append(l23e)
net.populations.append(l23ei)
net.populations.append(l23i)
net.populations.append(l23ii)

pops = [l23e.id, l23i.id]

conn_probs = [[0.1009,  0.1689, 0.0437, 0.0818, 0.0323, 0.,     0.0076, 0.    ],
             [0.1346,   0.1371, 0.0316, 0.0515, 0.0755, 0.,     0.0042, 0.    ],
             [0.0077,   0.0059, 0.0497, 0.135,  0.0067, 0.0003, 0.0453, 0.    ],
             [0.0691,   0.0029, 0.0794, 0.1597, 0.0033, 0.,     0.1057, 0.    ],
             [0.1004,   0.0622, 0.0505, 0.0057, 0.0831, 0.3726, 0.0204, 0.    ],
             [0.0548,   0.0269, 0.0257, 0.0022, 0.06,   0.3158, 0.0086, 0.    ],
             [0.0156,   0.0066, 0.0211, 0.0166, 0.0572, 0.0197, 0.0396, 0.2252],
             [0.0364,   0.001,  0.0034, 0.0005, 0.0277, 0.008,  0.0658, 0.1443]]

for p in pops:
    proj = Projection(id='proj_input_%s'%p,
                    presynaptic='%s_input'%p, 
                    postsynaptic=p,
                    synapse='???',
                    delay=2,
                    weight=10)
    proj.one_to_one_connector=OneToOneConnector()
    net.projections.append(proj)
    
for pre_i in range(len(pops)):
    for post_i in range(len(pops)):
        pre = pops[pre_i]
        post = pops[post_i]
        prob = conn_probs[post_i][pre_i]   #######   TODO: check!!!!
        weight = 1
        if 'I'in pre:
            weight = -1
        proj = Projection(id='proj_%s_%s'%(pre,post),
                        presynaptic=pre, 
                        postsynaptic=post,
                        synapse='???',
                        delay=1,
                        weight=weight)
        proj.random_connectivity=RandomConnectivity(probability=prob)
        net.projections.append(proj)


print net.to_json()
net.to_json_file('%s.json'%net.id)

################################################################################
###   Build Simulation object & save as JSON


sim = Simulation(id='Sim%s'%net.id,
                 duration='100',
                 dt='0.025',
                 recordTraces='all')
                 
sim.to_json_file()


################################################################################
###   Run in some simulators

print("**** Generating and running in NeuroML ****")

generate_and_run(sim, net, simulator='PyNN_NeuroML')
generate_and_run(sim, net, simulator='PyNN_NEURON')

'''
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







