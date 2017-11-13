import random
import numpy as np

def generate_network(nl_model, handler, seed=1234):
    
    pop_locations = {}
    
    print("Starting net generation...")
    rng = random.Random(seed)
    
    handler.handleDocumentStart(nl_model.id, "Generated network")
    
    handler.handleNetwork(nl_model.id, nl_model.notes)
    
    for p in nl_model.populations:
        
        handler.handlePopulation(p.id, p.component, p.size)
        pop_locations[p.id] = np.zeros((p.size,3))
        
        for i in range(p.size):
            if p.random_layout:
                x = rng.random()*p.random_layout.x
                y = rng.random()*p.random_layout.y
                z = rng.random()*p.random_layout.z
                pop_locations[p.id][i]=(x,y,z)

                handler.handleLocation(i, p.id, p.component, x, y, z)
        
    for p in nl_model.projections:
        
        handler.handleProjection(p.id, p.presynaptic, p.postsynaptic, p.synapse)
        
        conn_count = 0
        if p.random_connectivity:
            for pre_i in range(len(pop_locations[p.presynaptic])):
                for post_i in range(len(pop_locations[p.postsynaptic])):
                    flip = rng.random()
                    #print("Is cell %i conn to %i, prob %s - %s"%(pre_i, post_i, flip, p.random_connectivity.probability))
                    if flip<p.random_connectivity.probability:
                        handler.handleConnection(p.id, 
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
                                         delay = 0, \
                                         weight = 1)
                        conn_count+=1
        
        
        
def generate_neuroml2_from_network(nl_model, nml_file_name=None, print_summary=True, seed=1234):

    from neuroml.hdf5.NetworkBuilder import NetworkBuilder

    neuroml_handler = NetworkBuilder()

    generate_network(nl_model, neuroml_handler, seed=seed)

    nml_doc = neuroml_handler.get_nml_doc()

    if print_summary:
        # Print info
        print(nml_doc.summary())

    # Save to file
    if not nml_file_name:
        nml_file_name = '%s.net.nml'%nml_doc.id
        
    from neuroml.writers import NeuroMLWriter
    NeuroMLWriter.write(nml_doc,nml_file_name)

    print("Written NeuroML to %s"%nml_file_name)
    
    return nml_file_name, nml_doc



def generate_and_run(simulation, network, simulator):

    if simulator=='jNeuroML':

        from pyneuroml.lems import generate_lems_file_for_neuroml

        lems_file_name='LEMS_%s.xml'%simulation.id

        from networkshorthand.NetworkGenerator import generate_neuroml2_from_network

        nml_file_name, nml_doc = generate_neuroml2_from_network(network)

        included_files = []

        if network.cells:
            for c in network.cells:
                included_files.append(c.source_file)

        if network.synapses:
            for s in network.synapses:
                included_files.append(s.source_file)

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


    
