#
#
#   A class to handle events by PyNN...
#
#

from networkshorthand.utils import print_v
from networkshorthand.DefaultNetworkHandler import DefaultNetworkHandler

from importlib import import_module


class PyNNHandler(DefaultNetworkHandler):
        
    def __init__(self, simulator):
        print_v("Initiating PyNN with simulator %s"%simulator)
        self.sim = import_module("pyNN.%s" % simulator)

    def set_cells(self, cells):
        self.cells = cells

    def handleDocumentStart(self, id, notes):
            
        print_v("Document: %s"%id)
        self.sim.setup()
        

    def handleNetwork(self, network_id, notes, temperature=None):
            
        print_v("Network: %s"%network_id)
        if temperature:
            print_v("  Temperature: "+temperature)
        if notes:
            print_v("  Notes: "+notes)

    def handlePopulation(self, population_id, component, size=-1, component_obj=None):
        sizeInfo = " as yet unspecified size"
        if size>=0:
            sizeInfo = " size: "+ str(size)+ " cells"
        if component_obj:
            compInfo = " (%s)"%component_obj.__class__.__name__
        else:
            compInfo=""
            
        print_v("Population: "+population_id+", component: "+component+compInfo+sizeInfo)
        
        exec('%s = self.sim.Population(%s, self.cells["%s"], label="%s")'%(population_id,size,component,population_id))
        
        
    #
    #  Should be overridden to create specific cell instance
    #    
    def handleLocation(self, id, population_id, component, x, y, z):
        self.printLocationInformation(id, population_id, component, x, y, z)
        


    #
    #  Should be overridden to create population array
    #
    def handleProjection(self, projName, prePop, postPop, synapse, hasWeights=False, hasDelays=False, type="projection", synapse_obj=None, pre_synapse_obj=None):

        synInfo=""
        if synapse_obj:
            synInfo += " (syn: %s)"%synapse_obj.__class__.__name__
            
        if pre_synapse_obj:
            synInfo += " (pre comp: %s)"%pre_synapse_obj.__class__.__name__

        print_v("Projection: "+projName+" ("+type+") from "+prePop+" to "+postPop+" with syn: "+synapse+synInfo)


    #
    #  Should be overridden to handle network connection
    #  
    def handleConnection(self, projName, id, prePop, postPop, synapseType, \
                                                    preCellId, \
                                                    postCellId, \
                                                    preSegId = 0, \
                                                    preFract = 0.5, \
                                                    postSegId = 0, \
                                                    postFract = 0.5, \
                                                    delay = 0, \
                                                    weight = 1):
        
        self.printConnectionInformation(projName, id, prePop, postPop, synapseType, preCellId, postCellId, weight)
        if preSegId != 0 or postSegId!=0 or preFract != 0.5 or postFract != 0.5:
            print_v("Src cell: %d, seg: %f, fract: %f -> Tgt cell %d, seg: %f, fract: %f; weight %s, delay: %s ms" % (preCellId,preSegId,preFract,postCellId,postSegId,postFract, weight, delay))
        
    #
    #  Should be overridden to handle end of network connection
    #  
    def finaliseProjection(self, projName, prePop, postPop, synapse=None, type="projection"):
   
        print_v("Projection: "+projName+" from "+prePop+" to "+postPop+" completed")
        
        
    #
    #  Should be overridden to create input source array
    #  
    def handleInputList(self, inputListId, population_id, component, size, input_comp_obj=None):
            
        self.printInputInformation(inputListId, population_id, component, size)
        
        if size<0:
            self.log.error("Error! Need a size attribute in sites element to create spike source!")
            return
             
        
    #
    #  Should be overridden to to connect each input to the target cell
    #  
    def handleSingleInput(self, inputListId, id, cellId, segId = 0, fract = 0.5, weight=1):
        
        print_v("Input: %s[%s], cellId: %i, seg: %i, fract: %f, weight: %f" % (inputListId,id,cellId,segId,fract,weight))
        
        
    #
    #  Should be overridden to to connect each input to the target cell
    #  
    def finaliseInputSource(self, inputName):
        print_v("Input : %s completed" % inputName)
        
        

    #
    #  To signify network is distributed over parallel nodes
    #    
    def setParallelStatus(self, val):
        
        print_v("Parallel status (0=serial mode, 1=parallel distributed): "+str(val))
        self.isParallel = val
        