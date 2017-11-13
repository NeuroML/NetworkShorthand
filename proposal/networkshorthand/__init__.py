import collections

from networkshorthand.BaseTypes import Base
from networkshorthand.BaseTypes import BaseWithId
      
class Network(BaseWithId):

    def __init__(self, **kwargs):
        
        self.allowed_children = {'cells':'The cell definitions',
                                 'synapses':'The synapse definitions',
                                 'populations':'The populations',
                                 'projections':'The projections'}
                        
        super(Network, self).__init__(**kwargs)
  
  
class Cell(BaseWithId):

    def __init__(self, **kwargs):
        
        self.allowed_fields = {'neuroml2_source_file':str}
                      
        super(Cell, self).__init__(**kwargs)
  
  
class Synapse(BaseWithId):

    def __init__(self, **kwargs):
        
        self.allowed_fields = {'neuroml2_source_file':str}
                      
        super(Synapse, self).__init__(**kwargs)
    
    
class Population(BaseWithId):

    def __init__(self, **kwargs):
        
        self.allowed_fields = {'size':int,
                               'component':str,
                               'color':str,
                               'random_layout':RandomLayout}
                               
                      
        super(Population, self).__init__(**kwargs)
 
 
class RandomLayout(Base):

    def __init__(self, **kwargs):
        
        self.allowed_fields = {'x':float,
                               'y':float,
                               'z':float}
                               
        super(RandomLayout, self).__init__(**kwargs)

        
class Projection(BaseWithId):

    def __init__(self, **kwargs):
        self.allowed_fields = {'presynaptic':str,
                               'postsynaptic':str,
                               'synapse':str,
                               'random_connectivity':RandomConnectivity}

        super(Projection, self).__init__(**kwargs)


class RandomConnectivity(Base):

    def __init__(self, **kwargs):
        
        self.allowed_fields = {'probability':float}
                               
        super(RandomConnectivity, self).__init__(**kwargs)
    
    
class Simulation(BaseWithId):

    def __init__(self, **kwargs):
        
        self.allowed_fields = {'duration':float,
                               'dt':float,
                               'recordTraces':str}
                        
        super(Simulation, self).__init__(**kwargs)
    
                                   
            
        