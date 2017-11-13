from networkshorthand import *


################################################################################
###   Build a new network

net = Network(id='net0')
net.notes = 'The network'

print net


################################################################################
###   Add some populations

p0 = Population(id='pop0', size=5, component='iaf')
p1 = Population(id='pop1', size=10, component='iaf')
p1.size = 9

print p0
print p1

print p1.to_json()

net.populations.append(p0)
net.populations.append(p1)


################################################################################
###   Add a projection

net.projections.append(Projection(id='proj0',
                                  presynaptic=p0.id, 
                                  postsynaptic=p1.id,
                                  synapse='ampa'))
                                  
net.projections[0].random_connectivity=RandomConnectivity(probability=0.5)


################################################################################
###   Save to JSON format
                                 
print net
net.id = 'TestNetwork'

print net.to_json()
net.to_json_file('Example1_%s.json'%net.id)
