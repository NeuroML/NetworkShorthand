## JSON based Network Shorthand

As discussed during the 2017 NeuroML editors meeting there is some overlap between the format used for [NetPyNE to create cells/populations/connections](http://neurosimlab.org/netpyne/tutorial.html#network-parameters-tutorial-2) and that used in [MOOSE (Rdesigneur)](https://moose.ncbs.res.in/Rdesigneur/RdesigneurDocumentation.html). We should investigate whether it would be possible/useful to have a common format for these, which would also be supported natively by NeuroML libraries.

An end goal for this would be to have complex connectivity information like [this for the Traub et al 2005 model](https://github.com/OpenSourceBrain/Thalamocortical/blob/master/neuroConstruct/pythonScripts/netbuild/netConnList) expressible in such a shorthand notation (not verbosely in XML, or procedurally in Python), which can be read and edited by hand, but is standardised.
