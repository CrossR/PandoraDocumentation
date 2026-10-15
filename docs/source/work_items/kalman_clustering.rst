.. # =========================================================================
.. # WORK ITEM TEMPLATE
.. # =========================================================================

Kalman Clustering
----------------------------------------------------------

* **Main Developer:** Andy Chappell
* **Added in Version:** :tag:`LArContent v04.17.00 <v04_17_00>` (:pr:`252`)
* **Core File:** :core:`ProvisionalClusteringAlgorithm <larpandoracontent/LArTwoDReco/LArClusterCreation/ProvisionalClusteringAlgorithm.cc>`

Overview
^^^^^^^^
The provisional clustering algorithm is an alternative to the track clustering algorithm, using a Kalman filter to make clustering decisions.
The algorithm partitions the detector into its daughter volumes (e.g. per APA in wireplane detector) and acts within those volumes
to construct provisional clusters. This avoids some potential issues with stacked TPCs, as seen in DUNEFD HD and
ICARUS, where hits can be inappropriately clustered across volumes (this does not mean the problem cannot occur downstream).
The algorithm attempts to identify regions of complex activity in order to ignore them in initial clustering,
and then attempts to cluster them with the context provided by more simple clusters that enter those regions.

Usage & Configuration
^^^^^^^^^^^^^^^^^^^^^
This should be run as the first clustering algorithm within each 2D view, and should run as part of the :code:`LArClusteringParent`
algorithm, as per the example given for the U view below:

.. code-block:: xml

   <algorithm type = "LArClusteringParent">
        <algorithm type = "LArProvisionalClustering" description = "ClusterFormation"/>
        <InputCaloHitListName>CaloHitListU</InputCaloHitListName>
        <ClusterListName>ClustersU</ClusterListName>
        <ReplaceCurrentCaloHitList>true</ReplaceCurrentCaloHitList>
        <ReplaceCurrentClusterList>true</ReplaceCurrentClusterList>
    </algorithm>

