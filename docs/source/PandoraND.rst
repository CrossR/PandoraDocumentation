Pandora for the DUNE ND
=======================

The DUNE Near Detector (ND) has many unique reconstruction challenges which make
it an interesting testbed for Pandora.

These challenges can be summarised into three main points:

 - **Pileup**: Being so close to the DUNE neutrino beam, the ND suite will see
   pileup of neutrino interactions never seen at other neutrino experiments
   before. Pandora needs to be able to accurately split up and reconstruct both
   the primary neutrino interactions inside the detector, but also the barrage of
   rock muons that come from interactions occurring in the surrounding rock. This
   requires extensive bespoke development, extending the workflows already present
   in Pandora, to ensure we can deal with O(100) total interactions per beam
   spill.
 - **Multi-Detector**: As mentioned, the DUNE ND isn't a single detector, it is
   composed of a suite of detectors, with each detector solving different Physics
   needs. Pandora needs to be able to understand this multi-detector environment,
   and in the first case, enable matching between detectors. Exploration is
   on-going about performing full multi-detector reconstruction too, at least
   where the existing suite of Pandora algorithms make sense to be applied.
 - **Native 3D**: The LArTPC component of the DUNE ND is a native 3D LArTPC,
   unlike essentially all other LArTPCs. This makes the first issue easier to deal
   with! But it does mean Pandora needs to upgrade or replace its existing suite
   of 2D algorithms to 3D, ensuring we can take advantage of the full 3D
   information available in the detector. This is a significant undertaking, but
   one that is already underway.

LArRecoND
----------

To tackle these challenges, a new Pandora algorithm repository has been created,
called **LArRecoND**. This contains specific algorithms targeted at the unique
challenges of the DUNE ND: rock muon reconstruction, 3D pileup separation
algorithms, and upgraded versions of existing Pandora algorithms to work in 3D.

This essentially replaces the default Pandora :code:`LArReco` repository which
is used for all other LArTPCs, and is the main Pandora repository used for DUNE
ND reconstruction.  Of course, as we update and improve the existing Pandora
algorithms, changes are also made to the upstream :code:`LArContent` algorithm
repository, which is used by all of Pandora for LArTPCs.  When possible, we like
to keep ND-specific changes in :code:`LArRecoND`, with minimal changes to
:code:`LArContent` to enable efficient code re-use: I.e. allowing overriding or
extending existing algorithms, rather than duplicating them.

Near Detector Specific Algorithms
---------------------------------

A large number of the algorithms that exist in LArRecoND are built on top of the
existing Pandora algorithms, but with modifications to make them work in 3D, or
to improve their performance in the presence of pileup. However, there are also
a number of new algorithms that have been developed specifically for the ND.

These can all be found inside the :code:`LArRecoND/src` directory, and include:

 - **Core Reconstruction Algorithms**: The bulk of the code in the
   :code:`LArRecoND/src` directory is refactored reconstruction algorithms, which
   are modified versions of existing Pandora algorithms, to make them work in 3D,
   or to improve their performance in the presence of pileup. These are still
   under development, and will be improved over time. Most of the changes required
   are to either remove a 2D assumption or restriction, such that the algorithm
   can fully exploit the rich 3D information available in the ND.

 - **Rock Muon Reconstruction**: A suite of algorithms that can identify and
   reconstruct rock muons, which are a significant source of pileup in the ND.
   These algorithms are also still under development.

 - **3D Pileup Separation**: A suite of algorithms that can take a 3D
   reconstructed event, and separate it into its constituent interactions. This
   is a significant challenge, and is still under development. Whilst initially
   developed as part of the ND reconstruction, as it has the potential for usage
   in other LArTPCs, this code lives in the more general :code:`LArContent`
   repository, rather than :code:`LArRecoND`.


Near Detector Build / Workflow Changes
--------------------------------------

In general, building for the Near Detector is the same as building Pandora in
its regular standalone mode (as LArSoft is not used for the ND).  The main
change is cloning and building the :code:`LArRecoND` repository, rather than the
regular :code:`LArReco` repository. Otherwise, the instructions are the same as
outlined in the :ref:`building-pandora` page.

One of the main differences at the ND is the input files. As previously
mentioned, the ND does not use LArSoft, and the files we get from the simulation
and later data, are in HDF5 format.  There is then a 2 step process to convert
these files:

 1) Run :code:`LArRecoND/ndlarflow/h5_to_root_ndlarflow.py` on the HDF5 files to
    convert them into a ROOT file format.
 2) Run :code:`LArRecoND/ndlarflow/rootToRootConversion.C` to rejig the ROOT
    file in a more Pandora-friendly format. This is a ROOT macro, and can be run
    with :code:`root -l
    rootToRootConversion.C\(\"inputFile.root\",\"outputFile.root\"\)`. The input
    file is the output of the previous step, and the output file is the final file
    that Pandora will use.

From here, this input can now go into :code:`PandoraInterface` as normal, though there
are recommended config files that vary versus the recommended configs for other
LArTPCs.

The recommended configs right now are:

 - :code:`LArRecoND/settings/PandoraSettings_LArRecoND_ThreeD.xml`: This runs
   the full ND reconstruction, dealing with rock muons, pileup and more. However,
   whilst the code for pileup separation is under development, the secondary
   config may be of more use.
 - :code:`LArRecoND/settings/PandoraSettings_LArRecoND_ThreeD_PartialCheated.xml`:
   This runs full, real per-interaction reconstruction, but with "cheated" (i.e.
   using MC truth information) pileup separation. This is useful for development
   and testing of the reconstruction algorithms, without having to wait for the
   pileup separation algorithms to be fully developed.

There is also a touch of friction in things like the input geometry, and other
input files which will be improved as we develop this codebase further. In
general, if you have a complete build of Pandora for the ND, these are the steps
you need to take:

.. code-block::

    # Run the h5 to root conversion script on the HDF5 files
    python LArRecoND/ndlarflow/h5_to_root_ndlarflow.py inputFile.h5 outputFile.root

    # Run the root to root conversion macro on the output of the previous steps
    root -l rootToRootConversion.C\(\"outputFile.root\",\"finalInputFile.root\"\)

    # Setup the local directory for the Geometry and more.
    ln -s finalInputFile.root LArRecoNDInput.root

    # Make sure to follow the instructions in the README to build the geometry file!
    #
    # This can be found at https://github.com/PandoraPFA/LArRecoND#geometry-files

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

This should run through the full reconstruction workflow, and write out a few
output files. These can then be analysed with :code:`PandoraOuterface`, which
performs the higher-level reconstruction tasks: track and shower fits, PID,
energy calibration and more.  In a production environment, these would then form
the final Pandora output, which in turn forms the input in the Common Analysis
Framework (CAF) for physics analysis.

To run :code:`PandoraOuterface`, you can use the following command:

.. code-block::

    ~/build/path/LArRecoND/build/PandoraOuterface \
        -x ~/build/path/LArRecoND/settings/PandoraSettings_Outerface_Voxelise.xml \
        -f LArRecoND.root

Which will in turn produce its own, final output. This file should be usable
directly via ROOT, or via any ROOT-compatible library such as :code:`uproot`.
