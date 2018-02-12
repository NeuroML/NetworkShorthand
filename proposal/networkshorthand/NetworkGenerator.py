import random
import numpy as np
import os

from networkshorthand.utils import print_v


def generate_network(nl_model, handler, seed=1234):
    
    pop_locations = {}
    cell_objects = {}
    synapse_objects = {}
    
    print_v("Starting net generation...")
    rng = random.Random(seed)
    
    
    if nl_model.network_reader:
        
        exec('from networkshorthand.%s import %s'%(nl_model.network_reader.type,nl_model.network_reader.type))
        #params = ''
        #for k in nl_model.network_reader.parameters:
        #    params += '%s = %s, '%(k, '"%s"'%nl_model.network_reader.parameters[k] if type(nl_model.network_reader.parameters[k])==str else nl_model.network_reader.parameters[k])
        exec('network_reader = %s()'%(nl_model.network_reader.type))
        network_reader.parameters = nl_model.network_reader.parameters
        
        network_reader.parse(handler)
        pop_locations = network_reader.get_locations()
        
    else:
        handler.handle_document_start(nl_model.id, "Generated network")
        handler.handle_network(nl_model.id, nl_model.notes)
        
    
    for c in nl_model.cells:
        if c.neuroml2_source_file:
            from pyneuroml import pynml
            nml2_doc = pynml.read_neuroml2_file(c.neuroml2_source_file, 
                                                include_includes=True)
            cell_objects[c.id] = nml2_doc.get_by_id(c.id)
            
    for s in nl_model.synapses:
        if s.neuroml2_source_file:
            from pyneuroml import pynml
            nml2_doc = pynml.read_neuroml2_file(s.neuroml2_source_file, 
                                                include_includes=True)
            synapse_objects[s.id] = nml2_doc.get_by_id(s.id)
            
            
            
    for p in nl_model.populations:
        
        handler.handle_population(p.id, 
                                 p.component, 
                                 p.size, 
                                 cell_objects[p.component] if p.component in cell_objects else None)
                                 
        pop_locations[p.id] = np.zeros((p.size,3))
        
        for i in range(p.size):
            if p.random_layout:
                x = rng.random()*p.random_layout.width
                y = rng.random()*p.random_layout.height
                z = rng.random()*p.random_layout.depth
                pop_locations[p.id][i]=(x,y,z)

                handler.handle_location(i, p.id, p.component, x, y, z)
        
    for p in nl_model.projections:
        
        handler.handle_projection(p.id, 
                                 p.presynaptic, 
                                 p.postsynaptic, 
                                 p.synapse,
                                 synapse_obj=synapse_objects[p.synapse] if p.synapse in synapse_objects else None)

        delay = p.delay if p.delay else 0
        weight = p.weight if p.weight else 1
        
        conn_count = 0
        if p.random_connectivity:
            for pre_i in range(len(pop_locations[p.presynaptic])):
                for post_i in range(len(pop_locations[p.postsynaptic])):
                    flip = rng.random()
                    #print("Is cell %i conn to %i, prob %s - %s"%(pre_i, post_i, flip, p.random_connectivity.probability))
                    if flip<p.random_connectivity.probability:
                        handler.handle_connection(p.id, 
                                         conn_count, 
                                         p.presynaptic, 
                                         p.postsynaptic, 
                                         p.synapse, \
                                         pre_i, \
                                         post_i, \
                                         preSegId = 0, \
                                         preFract = 0.5, \
                                         postSegId = 0, \
                                         postFract = 0.5, \
                                         delay = delay, \
                                         weight = weight)
                        conn_count+=1
                        
        if p.one_to_one_connector:
            for i in range(min(len(pop_locations[p.presynaptic]),len(pop_locations[p.postsynaptic]))):
                
                        handler.handle_connection(p.id, 
                                         conn_count, 
                                         p.presynaptic, 
                                         p.postsynaptic, 
                                         p.synapse, \
                                         i, \
                                         i, \
                                         preSegId = 0, \
                                         preFract = 0.5, \
                                         postSegId = 0, \
                                         postFract = 0.5, \
                                         delay = delay, \
                                         weight = weight)
                        conn_count+=1
        
        handler.finalise_projection(p.id, 
                                 p.presynaptic, 
                                 p.postsynaptic, 
                                 p.synapse)
                                 
                                 
    for input in nl_model.inputs:
        
        handler.handle_input_list(input.id, 
                                input.population, 
                                input.input_source, 
                                size=0, 
                                input_comp_obj=None)
                          
        input_count = 0      
        for i in range(len(pop_locations[input.population])):
            flip = rng.random()
            if flip*100.<input.percentage:
                handler.handle_single_input(input.id, input_count, i)
                input_count+=1
            
                                
        
        
        
        
def generate_neuroml2_from_network(nl_model, nml_file_name=None, print_summary=True, seed=1234, format='xml'):

    from neuroml.hdf5.NetworkBuilder import NetworkBuilder

    neuroml_handler = NetworkBuilder()

    generate_network(nl_model, neuroml_handler, seed=seed)

    nml_doc = neuroml_handler.get_nml_doc()
    
    for s in nl_model.synapses:
        if nml_doc.get_by_id(s.id)==None:
            if s.neuroml2_source_file:
                import neuroml
                incl = neuroml.IncludeType(s.neuroml2_source_file)
                if not incl in nml_doc.includes:
                    nml_doc.includes.append(incl) 
            
    for i in nl_model.input_sources:
        if nml_doc.get_by_id(i.id)==None:
            if i.neuroml2_source_file:
                import neuroml
                incl = neuroml.IncludeType(i.neuroml2_source_file)
                if not incl in nml_doc.includes:
                    nml_doc.includes.append(incl) 
    
    for c in nl_model.cells:
        if c.neuroml2_source_file:
            
            import neuroml
            incl = neuroml.IncludeType(c.neuroml2_source_file)
            found_cell = False
            for cell in nml_doc.cells:
                if cell.id == c.id:
                    nml_doc.cells.remove(cell) # Better to use imported cell file; will have channels, etc.
                    nml_doc.includes.append(incl) 
                    found_cell = True
                    
            if not found_cell:
                for p in nl_model.populations:
                    if p.component==c.id:
                        pass
            
            if not incl in nml_doc.includes:
                nml_doc.includes.append(incl) 
                        
            
    if print_summary:
        # Print info
        print(nml_doc.summary())

    # Save to file
        
    if format=='xml':
        if not nml_file_name:
            nml_file_name = '%s.net.nml'%nml_doc.id
        from neuroml.writers import NeuroMLWriter
        NeuroMLWriter.write(nml_doc,nml_file_name)
        
    if format=='hdf5':
        if not nml_file_name:
            nml_file_name = '%s.net.nml.h5'%nml_doc.id
        from neuroml.writers import NeuroMLHdf5Writer
        NeuroMLHdf5Writer.write(nml_doc, nml_file_name)

    print_v("Written NeuroML to %s"%nml_file_name)
    
    return nml_file_name, nml_doc


locations_mods_loaded_from = []


def _generate_neuron_files_from_neuroml(network):

    print_v("-------------   Generating NEURON files from NeuroML for %s..."%(network.id))
    nml_src_files = []
    dir_for_mod_files = None

    for c in network.cells:
        if c.neuroml2_source_file:
            nml_src_files.append(c.neuroml2_source_file)
            if not dir_for_mod_files:
                dir_for_mod_files = os.path.dirname(os.path.abspath(c.neuroml2_source_file))

    for s in network.synapses:
        if s.neuroml2_source_file:
            nml_src_files.append(s.neuroml2_source_file)
            if not dir_for_mod_files:
                dir_for_mod_files = os.path.dirname(os.path.abspath(s.neuroml2_source_file))

    for i in network.input_sources:
        if i.neuroml2_source_file:
            nml_src_files.append(i.neuroml2_source_file)
            if not dir_for_mod_files:
                dir_for_mod_files = os.path.dirname(os.path.abspath(i.neuroml2_source_file))
                
    print nml_src_files
    print dir_for_mod_files

    for f in nml_src_files:
        from pyneuroml import pynml
        pynml.run_lems_with_jneuroml_neuron(f, 
                                            nogui=True, 
                                            only_generate_scripts=True,
                                            compile_mods = True,
                                            verbose=True)

    if not dir_for_mod_files in locations_mods_loaded_from:
        print_v("Generated NEURON code; loading mechanisms from %s"%dir_for_mod_files)
        print locations_mods_loaded_from
        try:

            from neuron import load_mechanisms
            #if os.path.get_cwd()==dir_for_mod_files:
                #print_v("Compiled mod files in currents"%dir_for_mod_files)
            load_mechanisms(dir_for_mod_files)

            locations_mods_loaded_from.append(dir_for_mod_files)
        except:
            print_v("Failed to load mod file mechanisms...")


def generate_and_run(simulation, network, simulator):

    print_v("Generating network %s and running in simulator: %s..."%(network.id, simulator))
    if simulator=='NEURON':
        
        _generate_neuron_files_from_neuroml(network)
        
        from networkshorthand.NeuronHandler import NeuronHandler
        
        nrn_handler = NeuronHandler()

        for c in network.cells:
            if c.neuroml2_source_file:
                src_dir = os.path.dirname(os.path.abspath(c.neuroml2_source_file))
                nrn_handler.executeHoc('load_file("%s/%s.hoc")'%(src_dir,c.id))
                
        generate_network(network, nrn_handler)


    elif simulator.startswith('PyNN'):
        
        #_generate_neuron_files_from_neuroml(network)
        simulator_name = simulator.split('_')[1].lower()
        
        
        from networkshorthand.PyNNHandler import PyNNHandler
        
        pynn_handler = PyNNHandler(simulator_name, simulation.dt, network.id)
        
        cells = {}
        for c in network.cells:
            if c.pynn_cell:
                cell_params = c.parameters if c.parameters else {}
                exec('cells["%s"] = pynn_handler.sim.%s(**cell_params)'%(c.id,c.pynn_cell))
                
        pynn_handler.set_cells(cells)
        
        for input_source in network.input_sources:
            if input_source.pynn_input:
                pynn_handler.add_input_source(input_source)
        
        generate_network(network, pynn_handler)
        
        for pid in pynn_handler.populations:
            pop = pynn_handler.populations[pid]
            if simulation.recordTraces=='all':
                if pop.can_record('v'):
                    pop.record('v')
        
        
        pynn_handler.sim.run(simulation.duration)
        pynn_handler.sim.end()
        
        if not 'NeuroML' in simulator:
            from neo.io import PyNNTextIO

            for pid in pynn_handler.populations:
                pop = pynn_handler.populations[pid]

                if simulation.recordTraces=='all':
                    for i in range(len(pop)):
                        if pop.can_record('v'):
                            filename = "%s_%s_v.dat"%(pop.label,i)
                            print("Writing data for %s[%s]"%(pop,i))
                            data =  pop.get_data('v', gather=False)
                            for segment in data.segments:
                                vm = segment.analogsignals[0].transpose()[i]
                                tt = np.array([t*simulation.dt/1000. for t in range(len(vm))])
                                times_vm = np.array([tt, vm/1000.]).transpose()
                                np.savetxt(filename, times_vm , delimiter = '\t', fmt='%s')
                            #filename = "%s.spikes"%(pop.label)
                            #io = PyNNTextIO(filename=filename)
        

    elif simulator=='NetPyNE':
        
        from netpyne import specs
        from netpyne import sim
        from netpyne import neuromlFuncs
        
        _generate_neuron_files_from_neuroml(network)
        
        import pprint; pp = pprint.PrettyPrinter(depth=6)
        
        netParams = specs.NetParams()
        netpyne_handler = neuromlFuncs.NetPyNEBuilder(netParams, verbose=True)
        
        generate_network(network, netpyne_handler)
        
        netpyne_handler.finalise()
        
        simConfig = specs.SimConfig() 
        simConfig.tstop = simulation.duration
        simConfig.duration = simulation.duration
        simConfig.dt = simulation.dt
        simConfig.recordStep = simulation.dt
        
        simConfig.recordCells = ['all'] 
        simConfig.recordTraces = {}
        if simulation.recordTraces=='all':
        
            for pop in netpyne_handler.popParams.values():
                print pop['cellsList']
                for i in pop['cellsList']:
                    id = pop['pop']
                    index = i['cellLabel']
                    simConfig.recordTraces['v_%s_%s'%(id,index)] = {'sec':'soma','loc':0.5,'var':'v','conds':{'pop':id,'cellLabel':index}}

        simConfig.saveDat = True
        
        #pp.pprint(netParams.todict())

        pp.pprint(simConfig.todict())
        
        sim.initialize(netParams, simConfig)  # create network object and set cfg and net params

        sim.net.createPops()  
        cells = sim.net.createCells()                 # instantiate network cells based on defined populations  
        
        
        
        for proj_id in netpyne_handler.projection_infos.keys():
            projName, prePop, postPop, synapse, ptype = netpyne_handler.projection_infos[proj_id]
            print_v("Creating connections for %s (%s): %s->%s via %s"%(projName, ptype, prePop, postPop, synapse))
            
            preComp = netpyne_handler.pop_ids_vs_components[prePop]
            
            ###from neuroml import Cell
           

            for conn in netpyne_handler.connections[projName]:
                
                pre_id, pre_seg, pre_fract, post_id, post_seg, post_fract, delay, weight = conn
                
                #connParam = {'delay':delay,'weight':weight,'synsPerConn':1, 'sec':post_seg, 'loc':post_fract, 'threshold':threshold}
                connParam = {'delay':delay,'weight':weight,'synsPerConn':1, 'sec':post_seg, 'loc':post_fract}
                
                if ptype == 'electricalProjection':

                    if weight!=1:
                        raise Exception('Cannot yet support inputs where weight !=1!')
                    connParam = {'synsPerConn': 1, 
                                 'sec': post_seg, 
                                 'loc': post_fract, 
                                 'gapJunction': True, 
                                 'weight': weight}
                else:
                    connParam = {'delay': delay,
                                 'weight': weight,
                                 'synsPerConn': 1, 
                                 'sec': post_seg, 
                                 'loc': post_fract} 
                                 #'threshold': threshold}

                connParam['synMech'] = synapse

                if post_id in sim.net.lid2gid:  # check if postsyn is in this node's list of gids
                    sim.net._addCellConn(connParam, pre_id, post_id)
                    
                    
        stims = sim.net.addStims()                    # add external stimulation to cells (IClamps etc)
        simData = sim.setupRecording()              # setup variables to record for each cell (spikes, V traces, etc)
        sim.runSim()                      # run parallel Neuron simulation  
        sim.gatherData()                  # gather spiking data and cell info from each node
        sim.saveData()                    # save params, cell info and sim output to file (pickle,mat,txt,etc)
        
    elif simulator=='jNeuroML' or  simulator=='jNeuroML_NEURON':

        from pyneuroml.lems import generate_lems_file_for_neuroml
        from pyneuroml import pynml

        lems_file_name='LEMS_%s.xml'%simulation.id

        nml_file_name, nml_doc = generate_neuroml2_from_network(network)

        included_files = []
        '''
        if network.cells:
            for c in network.cells:
                included_files.append(c.neuroml2_source_file)

        if network.synapses:
            for s in network.synapses:
                included_files.append(s.neuroml2_source_file)'''

        generate_lems_file_for_neuroml(simulation.id, 
                               nml_file_name, 
                               network.id, 
                               simulation.duration, 
                               simulation.dt, 
                               lems_file_name,
                               '.',
                               nml_doc = None,  # Use this if the nml doc has already been loaded (to avoid delay in reload)
                               include_extra_files = included_files,
                               gen_plots_for_all_v = True,
                               plot_all_segments = False,
                               gen_plots_for_quantities = {},   # Dict with displays vs lists of quantity paths
                               gen_plots_for_only_populations = [],   # List of populations, all pops if = []
                               gen_saves_for_all_v = simulation.recordTraces=='all',
                               save_all_segments = False,
                               gen_saves_for_only_populations = [],  # List of populations, all pops if = []
                               gen_saves_for_quantities = {},   # Dict with file names vs lists of quantity paths
                               gen_spike_saves_for_all_somas = False,
                               gen_spike_saves_for_only_populations = [],  # List of populations, all pops if = []
                               gen_spike_saves_for_cells = {},  # Dict with file names vs lists of quantity paths
                               spike_time_format='ID_TIME',
                               copy_neuroml = True,
                               lems_file_generate_seed=12345,
                               simulation_seed=12345)
              
        if simulator=='jNeuroML':
            pynml.run_lems_with_jneuroml(lems_file_name, nogui=True)
        elif simulator=='jNeuroML_NEURON':
            pynml.run_lems_with_jneuroml_neuron(lems_file_name, nogui=True)


    
