import collections

from networkshorthand.BaseTypes import Base
from networkshorthand.BaseTypes import BaseWithId
      
class Network(BaseWithId):

    def __init__(self, **kwargs):
        
        self.allowed_children = {'cells':('The cell definitions...',Cell),
                                 'synapses':('The synapse definitions...',Synapse),
                                 'populations':('The populations...',Population),
                                 'projections':('The projections...',Projection)}
                        
        super(Network, self).__init__(**kwargs)
  
  
class Cell(BaseWithId):

    def __init__(self, **kwargs):
        
        self.allowed_fields = {'neuroml2_source_file':('File name of NeuroML2 file',str),
                               'pynn_cell':('Name of standard PyNN cell type',str),
                               'parameters':('Dict of parameters for the cell',dict)}
                      
        super(Cell, self).__init__(**kwargs)
  
  
class Synapse(BaseWithId):

    def __init__(self, **kwargs):
        
        self.allowed_fields = {'neuroml2_source_file':('File name of NeuroML2 file',str)}
                      
        super(Synapse, self).__init__(**kwargs)
    
    
class Population(BaseWithId):

    def __init__(self, **kwargs):
        
        self.allowed_fields = {'size':('Size of population',int),
                               'component':('Type of cell to use in population',str),
                               'color':('Optional color to use for visualizing population',str),
                               'random_layout':('Layout in random region',RandomLayout)}
                               
                      
        super(Population, self).__init__(**kwargs)
 
 
class RandomLayout(Base):

    def __init__(self, **kwargs):
        
        self.allowed_fields = {'width':('Width of rectangular region',float),
                               'height':('Height of rectangular region',float),
                               'depth':('Depth of rectangular region',float) }
                               
        super(RandomLayout, self).__init__(**kwargs)

        
class Projection(BaseWithId):

    def __init__(self, **kwargs):
        self.allowed_fields = {'presynaptic':('Presynaptic population',str),
                               'postsynaptic':('Postsynaptic population',str),
                               'synapse':('Synapse to use',str),
                               'random_connectivity':('Use random connectivity',RandomConnectivity)}

        super(Projection, self).__init__(**kwargs)


class RandomConnectivity(Base):

    def __init__(self, **kwargs):
        
        self.allowed_fields = {'probability':('Random probability of connection',float)}
                               
        super(RandomConnectivity, self).__init__(**kwargs)
    
    
class Simulation(BaseWithId):

    def __init__(self, **kwargs):
        
        self.allowed_fields = {'duration':('Duration of simulation (ms)',float),
                               'dt':('Timestep of simulation (ms)',float),
                               'recordTraces':('Record traces?',str)}
                        
        super(Simulation, self).__init__(**kwargs)
    
                                   
            
        