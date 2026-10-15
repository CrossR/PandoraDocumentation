.. # =========================================================================
.. # WORK ITEM TEMPLATE
.. # =========================================================================

Final State Track/Shower Counting
----------------------------------------------------------

* **Main Developer:** Leigh Whitehead
* **Added in Version:** :tag:`LArContent v04.19.00 <v04_19_00>` (:pr:`267`)
* **Core File:** :core:`CNNTrackShowerCountingAlgorithm <larpandoradlcontent/LArEventClassification/CNNTrackShowerCountingAlgorithm.cc>`

Overview
^^^^^^^^
This CNN-based algorithm provides some event-level classification outputs for each of the 2D views.
It is designed to run immediately after the deep learning vertexing algorithm, and aims to provide targets
to guide the reconstruction towards given topologies or provide cross-checks later in the reconstruction chain.
A single CNN is used - it was trained using all three readout views and is used for inference on the
three views separately. The outputs from the algorithm are:

 - Number of tracks at the primary neutrino vertex: 0, 1, 2, 3, 4, 5+
 - Number of showers at the primary neutrino vertex: 0, 1, 2, 3, 4, 5+
 - Neutrino interaction type: CC numu, CC nue, NC

The outputs will be stored in a new event-level object that was added to the Pandora SDK.

