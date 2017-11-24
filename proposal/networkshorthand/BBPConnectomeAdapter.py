
import tables   # pytables for HDF5 support
import os

from neuroml.hdf5.NetworkContainer import *
from networkshorthand.BaseTypes import NetworkAdapter


class BBPConnectomeAdapter(NetworkAdapter):
    
    
    def __init__(self, **parameters):
                     
        print("Creating BBPConnectomeAdapter with %s..."%parameters)
        self.parameters = parameters
        
        self.current_population = None
        


    def parse(self, handler):

        filename = os.path.abspath(self.parameters['filename'])
        id=filename.split('/')[-1].split('.')[0]
        
        self.handler = handler
    
        notes = "Network read in from BBP connectome: %s"%filename
        handler.handleDocumentStart(id, notes)
        
        handler.handleNetwork(id, notes)
        
        h5file=tables.open_file(filename,mode='r')

        print("Opened HDF5 file: %s"%(h5file.filename))

        self.parse_group(h5file.root.populations)
        

        h5file.close()


    def parse_group(self, g):
        print("Parsing group: "+ str(g)+", name: "+g._v_name)

        for node in g:
            print("Sub node: %s, class: %s, name: %s (parent: %s)"   % (node,node._c_classid,node._v_name, g._v_name))

            if node._c_classid == 'GROUP':
                if g._v_name=='populations':
                    pop_id = node._v_name.replace('-','_')
                    self.current_population = pop_id
                    
                self.parse_group(node)

            if self._is_dataset(node):
                self.parse_dataset(node)
                
                
        self.current_population = None

        

    def _is_dataset(self, node):
          return node._c_classid == 'ARRAY' or node._c_classid == 'CARRAY'   


    def parse_dataset(self, d):
        print("Parsing dataset/array: "+ str(d))
        if self.current_population and d.name=='locations':
            
            size = min(self.parameters['max_cells_per_pop'],d.shape[0])
            

            self.handler.handlePopulation(self.current_population, 
                                     self.parameters['DEFAULT_CELL_ID'], 
                                     size,
                                     None)
                                     
            print("   There are %i cells in: %s"%(size, self.current_population))
            for i in range(0, d.shape[0]):
                
                if i<self.parameters['max_cells_per_pop']:
                    row = d[i,:]
                
                    self.handler.handleLocation(i, self.current_population, self.parameters['DEFAULT_CELL_ID'], row[0],row[1],row[2])
                
    
if __name__ == '__main__':

    filename = 'test_files/cons_locs_pathways_mc0_Column.h5'

    max_cells_per_pop=10
    
    parameters={'filename':filename, 'max_cells_per_pop':max_cells_per_pop}

    bbp = BBPConnectomeAdapter(parameters)
    
    from networkshorthand.DefaultNetworkHandler import DefaultNetworkHandler
    def_handler = DefaultNetworkHandler()
    
    bbp.parse(def_handler)   
    
    from neuroml.hdf5.NetworkBuilder import NetworkBuilder

    neuroml_handler = NetworkBuilder()
    
    bbp = BBPConnectomeAdapter(parameters)
    bbp.parse(neuroml_handler)  
    
    nml_file_name = 'BBP.net.nml'

    from neuroml.writers import NeuroMLWriter
    NeuroMLWriter.write(neuroml_handler.get_nml_doc(),nml_file_name)
    
    '''
    from networkshorthand.NeuronHandler import NeuronHandler


    nrn_handler = NeuronHandler()
    
    nrn_handler.executeHoc('load_file("hhcell.hoc")')
    bbp = BBPConnectomeAdapter()
    bbp.parse(file_name, nrn_handler)  
    
    #bbp.save_to_hdf5(nml_h5_file_name)'''