## JSON based Network Shorthand

As discussed during the [2016 NeuroML editors meeting](https://www.neuroml.org/workshops) there is some overlap between the format used for [NetPyNE to create cells/populations/connections](http://neurosimlab.org/netpyne/tutorial.html#network-parameters-tutorial-2) and that used in [MOOSE (Rdesigneur)](https://moose.ncbs.res.in/Rdesigneur/RdesigneurDocumentation.html). We should investigate whether it would be possible/useful to have a common format for these, which would also be supported natively by NeuroML libraries.

An end goal for this would be to have complex connectivity information as specified for networks such as:

- [the Traub et al 2005 model](https://github.com/OpenSourceBrain/Thalamocortical/blob/master/neuroConstruct/pythonScripts/netbuild/netConnList) 
- [the Potjans and Diesmann (2014) spiking column model](https://github.com/NeuralEnsemble/PyNN/blob/4854346d5f7dd33fe4140a49cddd84038f7f3495/examples/Potjans2014/network_params.py#L74)
- [Destexhe 2009 cortical network](https://github.com/dguarino/Destexhe2009/blob/master/params.py)
- [Blue Brain neocortical microcolumn](https://bbp.epfl.ch/nmc-portal/downloads)
- [Bezaire et al. 2016 Hippocampal CA1 network model](https://github.com/mbezaire/ca1/blob/master/datasets/conndata_163.dat)

expressible in a common shorthand notation (not verbosely in XML), which can be read and edited by hand or GUI, but is standardised. Shorthand (non XML based) network connectivity formats are being used in the Blue Brain Project and [Allen Institute](http://neuralensemble.org/media/slides/Sergey_Gratiy_bionet_representation.pdf) also.

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

#### Possible scope

- A format in JSON that can be validated that multiple tools can load in 
- Allows specification of simple cell models with small numbers of compartments
- Allows generative network connectivity specification
- Standard reference implementation for reading this format and generating NeuroML2 where cell/networks are fully specified 

