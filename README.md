# JSON based Network Shorthand

## Introduction

As discussed during the [2016 NeuroML editors meeting](https://www.neuroml.org/workshops) there is some overlap between the format used for [NetPyNE to create cells/populations/connections](http://neurosimlab.org/netpyne/tutorial.html#network-parameters-tutorial-2) and that used in [MOOSE (Rdesigneur)](https://moose.ncbs.res.in/Rdesigneur/RdesigneurDocumentation.html). [NeuroML](http://www.neuroml.org) has support for instance based network specifications, as well as some template based networks, and [PyNN](http://neuralensemble.org/PyNN/) can procedurally create networks. [Brain Modelling Tookit](https://alleninstitute.github.io/bmtk/) is working on a similar format. 

We should investigate whether it would be possible/useful to have a **common format** for these, which would also be supported natively by NeuroML and PyNN libraries, as well as other applications.

An end goal for this would be to have complex connectivity information as specified for networks such as:

- [the Traub et al 2005 model](https://github.com/OpenSourceBrain/Thalamocortical/blob/master/neuroConstruct/pythonScripts/netbuild/netConnList) 
- [the Potjans and Diesmann (2014) spiking column model](https://github.com/NeuralEnsemble/PyNN/blob/4854346d5f7dd33fe4140a49cddd84038f7f3495/examples/Potjans2014/network_params.py#L74)
- [Destexhe 2009 cortical network](https://github.com/dguarino/Destexhe2009/blob/master/params.py)
- [Blue Brain neocortical microcolumn](https://bbp.epfl.ch/nmc-portal/downloads)
- [Bezaire et al. 2016 Hippocampal CA1 network model](https://github.com/mbezaire/ca1/blob/master/datasets/conndata_163.dat)

expressible in a common shorthand notation (not verbosely in XML), which can be read and edited by hand or GUI, but is standardised.

## Scope

- A format in JSON that can be validated, that multiple tools can load in 
- Allows specification of simple cell models with small numbers of compartments
- Allows generative network connectivity specification
- Standard reference implementation (in Python) for reading this format and generating NeuroML2 etc. where instances of cell/connections are fully specified 
- Existing formats for storing connections (e.g. in HDF5) can be read in and out for easy use in supporting tools

## Existing work

**Example from Rdesigneur**

```
rdes = rd.rdesigneur(
    chanProto = [['make_HH_Na()', 'Na'], ['make_HH_K()', 'K']],
    chanDistrib = [
        ['Na', 'soma', 'Gbar', '1200' ],
        ['K', 'soma', 'Gbar', '360' ]],
    stimList = [['soma', '1', '.', 'inject', '(t>0.1 && t<0.2) * 1e-8' ]],
    plotList = [['soma', '1', '.', 'Vm', 'Membrane potential']]
)
```

**Example from NetPyNE**

    cellRule = {'conds': {'cellType': 'PYR'},  'secs': {}}  # cell rule dict
    cellRule['secs']['soma'] = {'geom': {}, 'mechs': {}}                                                                                          
    cellRule['secs']['soma']['geom'] = {'diam': 18.8, 'L': 18.8, 'Ra': 123.0}                                                                           
    cellRule['secs']['soma']['mechs']['hh'] = {'gnabar': 0.12, 'gkbar': 0.036, 'gl': 0.003, 'el': -70}              # soma hh mechanisms
    ...
    netParams.popParams['artif1'] = {'cellModel': 'IntFire2', 'taum': 100, 'noise': 0.5, 'numCells': 100}  # Intfire2
    netParams.popParams['artif2'] = {'cellModel': 'NetStim', 'rate': 100, 'noise': 0.5, 'numCells': 100}  # NetsStim
    ...
    netParams.connParams['bg->all'] = {
        'preConds': {'pop': 'background'},
        'postConds': {'cellType': ['S','M'], 'ynorm': [0.1,0.6]}, # background -> S,M with ynrom in range 0.1 to 0.6
        'synReceptor': 'AMPA',                                  # target synaptic mechanism
        'weight': 0.01,                                         # synaptic weight
        'delay': 5}     
    
**Example from BMTK**

    "networks": {
      "nodes": [
        {
          "name": "V1",
          "nodes_file": "$NETWORK_DIR/v1_nodes.h5",
          "node_types_file": "$NETWORK_DIR/v1_node_types.csv"
        },
              ...
      ],

      "edges": [
        {
          "target": "V1",
          "source": "V1",
          "edges_file": "$NETWORK_DIR/v1_v1_edges.h5",
          "edge_types_file": "$NETWORK_DIR/v1_v1_edge_types.csv"
        },
      ...
      ]
    }
    
    
**Example from PyNN**

     params = {


    'Populations' : {
        'ext' : {
            'n' : 1,
            'type': SpikeSourcePoisson,
            'cellparams' : {
                'start':0.0,
                'rate':50.,
                'duration':100.0
            }
        },
        ....
    },
    ...
    'Projections' : {
        'ext_py' : {
            'source' : 'ext',
            'target' : 'py',
            'connector' : FixedProbabilityConnector(.02),
            'synapse_type' : StaticSynapse,
            'weight' : 6e-3,
            'receptor_type' : 'excitatory'
    },



    
## Proposal
    
A proposed solution for this format, tightly integrated with NeuroML2, is here: **https://github.com/NeuroML/NeuroMLlite**
