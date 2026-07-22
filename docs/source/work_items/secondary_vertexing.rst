.. # =========================================================================
.. # WORK ITEM TEMPLATE
.. # =========================================================================

Secondary Vertexing
----------------------------------------------------------

* **Main Developer:** Andy Chappell
* **Added in Version:** :tag:`LArContent v04.13.00 <v04_13_00>` (:pr:`237`)
* **Core File:** :core:`DlSecondaryVertexingAlgorithm <larpandoradlcontent/LArVertex/DlSecondaryVertexingAlgorithm.cc>`

Overview
^^^^^^^^
Secondary vertexing attempts to extend the primary interaction vertexing technique to identify topologically interesting higher order vertices.
In principle, such vertices can be used to aid downstream clustering decisions.
Unlike the primary vertexing, this is a single pass technique, as the vertex multiplicity would make second pass processing computationally
prohibitive under the current implementation. As a result, the candidate vertices are identified less precisely than in the primary vertexing case,
and should therefore be viewed as a region of interest identifier, rather than a precise vertex location. This network runs on hits,
and therefore has no dependence on any preceding reconstruction algorithms.

Training set preparation
^^^^^^^^^^^^^^^^^^^^^^^^
The mode of operation and output is largely the same as for primary vertexing, with the algorithm inheriting much of the implementation from primary vertexing.
The XML file for training in DUNE can be found
`here <https://github.com/PandoraPFA/LArReco/blob/master/settings/development/PandoraSettings_SecVtxTrain_DUNEFD.xml>`__,
other experimental contexts will be similar.
Output files from training will be CSV files with the specified prefix, followed by a tag denoting the view.
Multiple files per view can be safely concatenated together.
It may also be worthwhile to concatenate, for example, mirror reflected (e.g. U and V in DUNE)
views to create a single shared network for those views. Distance thresholds are given in terms of the fraction of the image diagonal that the distance represents
(i.e. hits at the bottom left and top right of the image will be separated by a distance of 1).
For :code:`N` distance classes, you should define :code:`N + 1` points on the range :code:`[0, 1]`. :code:`N`, and the specific thresholds can be varied for each use case,
as long as they are consistent between training and inference.

Training the network
^^^^^^^^^^^^^^^^^^^^
`Python Notebooks <https://github.com/PandoraPFA/LArMachineLearningData/tree/master/scripts/deep_learning/vertex>`__
are provided for training the network.
These notebooks are self-documenting, so only a brief overview will be given here.
You will need the CSV files created during training set preparation, The :code:`make_images.ipynb` notebook can be run from start to finish,
modulo any edits that may be needed according to any customisations you applied (as described in the notebook). Remember, only pass 1 needs to be run.

The :code:`network.ipynb` notebook can then run on the resultant compressed numpy arrays from the image generation step.
You'll need GPU resources for this, and ensure your files are available on the GPU node (or a suitable high speed, highly parallel I/O system).
As with the previous notebook, potential edits according to customisation and which view you are running on will need to be made,
but otherwise you can run the notebook from start to finish.

This will produce the trained networks for every epoch, and the TorchScript (.pt)  network that will actually run in Pandora,
along with various metrics showing training and validation loss and accuracy, to check for over-fitting, and confusion matrices.

Usage & Configuration
^^^^^^^^^^^^^^^^^^^^^
At the time of writing, the secondary vertexing network is not part of any default workflow, but it can be used,
assuming the training configuration above, by inclusion of the following (DUNE) XML

.. code-block:: xml

    <algorithm type = "LArDLSecondaryVertexing">
      <TrainingMode>false</TrainingMode>
      <OutputVertexListName>SecondaryVertices3D</OutputVertexListName>
      <CaloHitListNames>CaloHitListW CaloHitListU CaloHitListV</CaloHitListNames>
      <ModelFileNameU>PandoraNetworkData/PandoraNet_SecVertex_DUNEFD_Accel_1_U_v04_13_00.pt</ModelFileNameU>
      <ModelFileNameV>PandoraNetworkData/PandoraNet_SecVertex_DUNEFD_Accel_1_V_v04_13_00.pt</ModelFileNameV>
      <ModelFileNameW>PandoraNetworkData/PandoraNet_SecVertex_DUNEFD_Accel_1_W_v04_13_00.pt</ModelFileNameW>
      <DistanceThresholds>0. 0.00275 0.00825 0.01925 0.03575 0.05775 0.08525 0.12375 0.15125 0.20625 0.26125 0.31625 0.37125 0.42625 0.50875 0.59125 0.67375 0.75625 0.85 1.0</DistanceThresholds>
      <Visualise>false</Visualise>
    </algorithm>

It is recommended to include this XML block immediately after the second pass of the primary vertexing network.
Outputs are then available to subsequent algorithms by accessing the :code:`SecondaryVertices3D` vertex list.

