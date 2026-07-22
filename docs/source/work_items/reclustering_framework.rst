.. # =========================================================================
.. # WORK ITEM TEMPLATE
.. # =========================================================================

Reclustering Framework
----------------------------------------------------------

* **Main Developers:** Maria Brigida Brunetti, Alex Wilkinson
* **Added in Version:** :tag:`LArContent v04.14.01 <v04_14_01>` (:pr:`240`)
* **Core File:** :core:`ThreeDMultiReclusteringAlgorithm <larpandoracontent/LArReclustering/ThreeDMultiReclusteringAlgorithm.cc>`

Overview
^^^^^^^^
A framework to perform reclustering in Pandora has been implemented via an algorithm that can be found in LArContent at the link above.
The algorithm operates on the 3D hits, and uses a figure of merit tool that evaluates some score for goodness of clustering,
and then a sequence of algorithm tools that can be used to perform new clusterings of the 3D hits and propose new clusters.
The framework then uses the best clusters, as defined by the figure of merit, and propagates these changes to all Pandora
objects linked to the 3D hits (2D clusters, 3D clusters, Pfos). Example algorithm tools that can be used with it can be seen in the PR,
but are not active in the current Pandora workflow.

