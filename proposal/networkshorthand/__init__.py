import collections

from networkshorthand.BaseTypes import Base
from networkshorthand.BaseTypes import BaseWithId
from networkshorthand.BaseTypes import NetworkAdapter
      
class Network(BaseWithId):

    def __init__(self, **kwargs):
        
        self.allowed_children = {'cells':('The cell definitions...',Cell),
                                 'synapses':('The synapse definitions...',Synapse),
                                 'input_sources':('The input definitions...',InputSource),
                                 'populations':('The populations...',Population),
                                 'projections':('The projections...',Projection),
                                 'inputs':('The inputs to apply...',Input)}
                                 
        self.allowed_fields = {'network_reader':('Can read in network',NetworkAdapter)}
                        
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
  
  
class InputSource(BaseWithId):

    def __init__(self, **kwargs):
        
        self.allowed_fields = {'neuroml2_source_file':('File name of NeuroML2 file',str),
                               'pynn_input':('Name of standard PyNN input',str),
                               'parameters':('Dict of parameters for the cell',dict)}
                      
        super(InputSource, self).__init__(**kwargs)
    
    
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
                               'delay':('Delay to use',float),
                               'weight':('Weight to use',float),
                               'random_connectivity':('Use random connectivity',RandomConnectivity)}

        super(Projection, self).__init__(**kwargs)
        
        
class Input(BaseWithId):

    def __init__(self, **kwargs):
        
        self.allowed_fields = {'input_source':('Type of input to use in population',str),
                               'population':('Population to target',str),
                               'percentage':('Percentage of cells to apply this input to',float)}
                               
                      
        super(Input, self).__init__(**kwargs)


class RandomConnectivity(Base):

    def __init__(self, **kwargs):
        
        self.allowed_fields = {'probability':('Random probability of connection',float)}
                               
        super(RandomConnectivity, self).__init__(**kwargs)
        
        
  
class NetworkReader(Base):

    def __init__(self, **kwargs):
        
        self.allowed_fields = {'type':('Type of NetworkReader',str),
                               'parameters':('Dict of parameters for the cell',dict)}
                      
        super(NetworkReader, self).__init__(**kwargs)
    
    
class Simulation(BaseWithId):

    def __init__(self, **kwargs):
        
        self.allowed_fields = {'duration':('Duration of simulation (ms)',float),
                               'dt':('Timestep of simulation (ms)',float),
                               'recordTraces':('Record traces?',str)}
                        
        super(Simulation, self).__init__(**kwargs)
    
                                   
            
        
