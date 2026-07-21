Pandora for the DUNE ND
=======================

The DUNE Near Detector (ND) has many unique reconstruction challenges which make it an interesting testbed for Pandora.

These challenges can be summarised into three main points:

 - **Pileup**: Being so close to the DUNE neutrino beam, the ND suite will see pileup of neutrino interactions never seen at other neutrino experiments before. Pandora needs to be able to accurately split up and reconstruct both the primary neutrino interactions inside the detector, but also the barrage of rock muons that come from interactions occurring in the surrounding rock. This requires extensive bespoke development, extending the workflows already present in Pandora, to ensure we can deal with O(100) total interactions per beam spill.
 - **Multi-Detector**: As mentioned, the DUNE ND isn't a single detector, it is composed of a suite of detectors, with each detector solving different Physics needs. Pandora needs to be able to understand this multi-detector environment, and in the first case, enable matching between detectors. Exploration is on-going about performing full multi-detector reconstruction too, at least where the existing suite of Pandora algorithms make sense to be applied.
 - **Native 3D**: The LArTPC component of the DUNE ND is a native 3D LArTPC, unlike essentially all other LArTPCs. This makes the first issue easier to deal with! But it does mean Pandora needs to upgrade or replace its existing suite of 2D algorithms to 3D, ensuring we can take advantage of the full 3D information available in the detector. This is a significant undertaking, but one that is already underway.

LArRecoND
----------

To tackle these challenges, a new Pandora algorithm repository has been created, called **LArRecoND**. This contains specific algorithms targeted at the
unique challenges of the DUNE ND: rock muon reconstruction, 3D pileup separation algorithms, and upgraded versions of existing Pandora algorithms to work in 3D.

This essentially replaces the default Pandora `LArReco` repository which is used for all other LArTPCs, and is the main Pandora repository used for DUNE ND reconstruction.
Of course, as we update and improve the existing Pandora algorithms, changes are also made to the upstream `LArContent` algorithm repository, which is used by all of Pandora for LArTPCs.
When possible, we like to keep ND-specific changes in `LArRecoND`, with minimal changes to `LArContent` to enable efficient code re-use: I.e. allowing overriding or extending existing algorithms, rather than duplicating them.

Near Detector Specific Algorithms
---------------------------------


Near Detector Build / Workflow Changes
--------------------------------------

In general, building for the Near Detector is the same as building Pandora in its regular standalone mode (as LArSoft is not used for the ND).
The main change is cloning and building the `LArRecoND` repository, rather than the regular `LArReco` repository. Otherwise, the instructions are the same as outlined in the :ref:`building-pandora` page.

One of the main differences at the ND is the input files. As previously mentioned, the ND does not use LArSoft, and the files we get from the simulation and later data, are in HDF5 format.
There is then a 2 step process to convert these files:

 1) Run `LArRecoND/ndlarflow/h5_to_root_ndlarflow.py` on the HDF5 files to convert them into a ROOT file format.
 2) Run `LArRecoND/ndlarflow/rootToRootConversion.C` to rejig the ROOT file in a more Pandora-friendly format. This is a ROOT macro, and can be run with `root -l rootToRootConversion.C\(\"inputFile.root\",\"outputFile.root\"\)`. The input file is the output of the previous step, and the output file is the final file that Pandora will use.

From here, this input can now go into `PandoraInterface` as normal, though there are recommended config files that vary versus the recommended configs for other LArTPCs.

The recommended configs right now are:

 - `LArRecoND/settings/PandoraSettings_LArRecoND_ThreeD.xml` - This runs the full ND reconstruction, dealing with rock muons, pileup and more. However, whilst the code for pileup separation is under development, the secondary config may be of more use.
 - `LArRecoND/settings/PandoraSettings_LArRecoND_ThreeD_PartialCheated.xml` - This runs full, real per-interaction reconstruction, but with "cheated" (i.e. using MC truth information) pileup separation. This is useful for development and testing of the reconstruction algorithms, without having to wait for the pileup separation algorithms to be fully developed.

There is also a touch of friction in things like the input geometry, and other input files which will be improved as we develop this codebase further. In general, if you have a complete build of Pandora for the ND, these are the steps you need to take:

.. code-block::

    # Run the h5 to root conversion script on the HDF5 files
    python LArRecoND/ndlarflow/h5_to_root_ndlarflow.py inputFile.h5 outputFile.root

    # Run the root to root conversion macro on the output of the previous steps
    root -l rootToRootConversion.C\(\"outputFile.root\",\"finalInputFile.root\"\)

    # Setup the local directory for the Geometry and more.
    ln -s finalInputFile.root LArRecoNDInput.root

    # Finally, run PandoraInterface with the recommended config file
    #
    # This runs the partial cheated workflow, with pileup mitigation,
    # over 15 events, using the provided geometry file.
    #
    # More information can be pulled out with --help.
    ~/build/path/LArRecoND/build/PandoraInterface \
        -r Full \
        -i ~/build/path/LArRecoND/settings/PandoraSettings_LArRecoND_ThreeD_PartialCheated.xml \
        -j both \
        -f SPMC \
        -g NDLArGeom.root \
        -M \
        -e finalInputFile.root \
        -s 0 -n 15

