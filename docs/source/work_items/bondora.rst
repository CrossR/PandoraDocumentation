.. # =========================================================================
.. # WORK ITEM TEMPLATE
.. # =========================================================================

Bayesian Optimisation of Parameters (BOndora)
----------------------------------------------------------

* **Main Developer:** Alex Wilkinson
* **Core Files:** `BOndora Scripts <https://github.com/PandoraPFA/LArMachineLearningData/tree/master/scripts/bondora>`__

Overview
^^^^^^^^
This is a framework for using Bayesian optimisation to optimise algorithm configurations (any  parameter exposed to the xml) w.r.t.
a user-defined goodness of clustering (expected to be some combination of purity, completeness, and ARI).
BOndora can be found in the LArMachineLearningData repository linked above. There is a README with instructions on its use.

The optimisation development was focused on the 2D clustering algorithms and outputs,
it was found to boost clustering performance by a few percent (which is significant but not huge).
The method can be extended to any algorithm(s) in the workflow if desired. The optimisation will be revisited once
new algorithms are ready (DL shower growing, 2D Kalman filter clustering, a rework of the mop-up algs).

