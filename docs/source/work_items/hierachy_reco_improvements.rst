.. # =========================================================================
.. # WORK ITEM TEMPLATE
.. # =========================================================================

Hierarchy Reconstruction Improvements
----------------------------------------------------------

* **Main Developer:** Isobel Mawby
* **Added in Version:** :tag:`LArContent v04.15.00 <v04_15_00>` (:pr:`236`)
* **Core File:** :core:`DLNeutrinoHierarchyAlgorithm <larpandoradlcontent/LArThreeDReco/LArEventBuilding/DLNeutrinoHierarchyAlgorithm.cc>`

Overview
^^^^^^^^
This algorithm is a deep learning alternative to the existing :code:`NeutrinoHierarchyAlgorithm`, and its role is to build the neutrino hierarchy
i.e. to identify all parent-child links in the event.
The algorithm identifies the primary (direct children of the neutrino) particles using an MLP-based network.
The algorithm then iteratively builds each ‘tier’ within the hierarchy by using a second MLP network to identifying
the children of particles in the previously built tier. If any particles in the event remain,
a recovery procedure runs in which reduced thresholds are used to identify parent-child links.
Finally, any remaining particles are identified as neutrino children.

The :code:`NeutrinoHierarchyAlgorithm` is very cautious and identifies non-neutrino children only if a strict criterion is met.
This results in pure, but rather incomplete ‘later’ tiers. The :code:`DLNeutrinoHierarchyAlgorithm` significantly improves upon this,
whilst retaining the efficiency with which primary particles are identified as such.

Usage & Configuration
^^^^^^^^^^^^^^^^^^^^^
At the time of writing this algorithm has been released into Pandora software and is active in the LBL workflow of the DUNE HD.
Training is ongoing for the atmospheric workflow, and for the VD detector. Training instructions can be found
`here <https://github.com/imawby/Documentation/blob/feature/MLDocs/ML_Documentation/Pandora_ML_Guide.pdf>`___.
To activate the deep learning neutrino hierarchy building algorithm, one needs to replace the :code:`LArNeutrinoHierarchy`
algorithm block with the following block in the :code:`PandoraSettings_Neutrino_DETECTOR.xml`.

.. code-block:: xml

   <algorithm type = "LArDLNeutrinoHierarchy">
       <tool type = "LArDLPrimaryHierarchy" description = "DLPrimaryHierarchyTool">
           <PrimaryShowerClassifierModelName> PandoraNetworkData/PandoraNet_Hierarchy_DUNEFD_HD_S_Class_v014_15_00.pt</PrimaryShowerClassifierModelName>
           <PrimaryTrackBranchModelName> PandoraNetworkData/PandoraNet_Hierarchy_DUNEFD_HD_T_Edge_v014_15_00.pt</PrimaryTrackBranchModelName>
           <PrimaryTrackClassifierModelName> PandoraNetworkData/PandoraNet_Hierarchy_DUNEFD_HD_T_Class_v014_15_00.pt</PrimaryTrackClassifierModelName>
       </tool>
       <tool type = "LArDLLaterTierHierarchy" description = "DLLaterTierHierarchyTool">
           <TrackShowerBranchModelName> PandoraNetworkData/PandoraNet_Hierarchy_DUNEFD_HD_TS_Edge_v014_15_00.pt</TrackShowerBranchModelName>
           <TrackShowerClassifierModelName> PandoraNetworkData/PandoraNet_Hierarchy_DUNEFD_HD_TS_Class_v014_15_00.pt</TrackShowerClassifierModelName>
           <TrackTrackBranchModelName> PandoraNetworkData/PandoraNet_Hierarchy_DUNEFD_HD_TT_Edge_v014_15_00.pt</TrackTrackBranchModelName>
           <TrackTrackClassifierModelName> PandoraNetworkData/PandoraNet_Hierarchy_DUNEFD_HD_TT_Class_v014_15_00.pt</TrackTrackClassifierModelName>
       </tool>
   </algorithm>

