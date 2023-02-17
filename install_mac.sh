#!/bin/bash
NUM_CPUS=8
echo "Please make sure that 'wget' is installed!"
echo "Please make sure that 'cmake' is installed!"
echo "Please make sure that 'python' is a valid command pointing to a Python binary!"
# Download OMNeT++ v5.6.2, unpack and go to directory.
echo "Downloading OMNeT++"
wget https://github.com/omnetpp/omnetpp/releases/download/omnetpp-5.6.2/omnetpp-5.6.2-src-macosx.tgz
echo -e "\n\nUnpacking OMNeT++"
tar -xvzf omnetpp-5.6.2-src-macosx.tgz
rm omnetpp-5.6.2-src-macosx.tgz
echo -e "\n\nCompiling OMNeT++"
cd omnetpp-5.6.2/
# Set PATH, configure and build.
WORKDIR=$(pwd)
export PATH=${WORKDIR}/bin:$PATH
./setenv
./configure CC=gcc CXX=g++ WITH_OSG=no WITH_OSGEARTH=no WITH_QTENV=no
make -j$NUM_CPUS MODE=release base
#make -j$NUM_CPUS MODE=debug base
# Download INET, unpack and go to directory.
echo -e "\n\nDownloading INET"
mkdir workspace
cd workspace
wget https://github.com/eltayebmusab/inet/archive/refs/tags/v4.2.5.tar.gz
echo -e "\n\nUnpacking INET"
tar -xvzf v4.2.5.tar.gz 
rm -R v4.2.5.tar.gz
mv inet-4.2.5/ inet4
cd inet4/
# Build.
echo -e "\n\nCompiling INET"
make makefiles
# this empty file can prevent building https://stackoverflow.com/questions/66094801/whats-the-reason-of-ipv6-feasure-disabled-error-while-building-inet-4-1-2-in
rm src/inet/features.h
make -j$NUM_CPUS MODE=release
#make -j$NUM_CPUS MODE=debug
cd ..
# Compile GLUE
echo -e "\n\nDownloading GLUE lib"
git clone git@collaborating.tuhh.de:e-4/research-projects/intairnet-collection/intairnet-linklayer-glue.git
cd intairnet-linklayer-glue
git pull
mkdir cmake-build-release
cd cmake-build-release
cmake -DCMAKE_BUILD_TYPE=Release ..
make -j$NUM_CPUS intairnet_linklayer_glue
# cd ..
# mkdir cmake-build-debug
# cd cmake-build-debug
# cmake -DCMAKE_BUILD_TYPE=Debug ..
# make -j$NUM_CPUS intairnet_linklayer_glue
cd ../..
# Compile RLC
echo -e "\n\nDownloading and compiling RLC lib"
git clone git@collaborating.tuhh.de:e-4/research-projects/intairnet-collection/avionic-rlc.git
cd avionic-rlc
ln -s ../intairnet-linklayer-glue/ glue-lib-headers
mkdir cmake-build-release
cd cmake-build-release
cmake -DCMAKE_BUILD_TYPE=Release ..
make -j$NUM_CPUS tuhh_intairnet_rlc
# cd ..
# mkdir cmake-build-debug
# cd cmake-build-debug
# cmake -DCMAKE_BUILD_TYPE=Debug ..
# make -j$NUM_CPUS tuhh_intairnet_rlc
cd ../..
# Compile ARQ
echo -e "\n\nDownloading and compiling ARQ lib"
git clone git@collaborating.tuhh.de:e-4/research-projects/intairnet-collection/avionic-arq.git
cd avionic-arq/dev
ln -s ../../intairnet-linklayer-glue/ glue-lib-headers
mkdir cmake-build-release
cd cmake-build-release
cmake -DCMAKE_BUILD_TYPE=Release ..
make -j$NUM_CPUS tuhh_intairnet_arq
# cd ..
# mkdir cmake-build-debug
# cd cmake-build-debug
# cmake -DCMAKE_BUILD_TYPE=Debug ..
# make -j$NUM_CPUS tuhh_intairnet_arq
cd ../../..
# Compile MCSOTDMA
echo -e "\n\nDownloading and compiling MCSOTDMA lib"
git clone git@collaborating.tuhh.de:e-4/research-projects/intairnet-collection/mc-sotdma.git
cd mc-sotdma
ln -s ../intairnet-linklayer-glue/ glue-lib-headers
mkdir cmake-build-release
cd cmake-build-release
cmake -DCMAKE_BUILD_TYPE=Release ..
make -j$NUM_CPUS tuhh_intairnet_mc-sotdma
# cd ..
# mkdir cmake-build-debug
# cd cmake-build-debug
# cmake -DCMAKE_BUILD_TYPE=Debug ..
# make -j$NUM_CPUS tuhh_intairnet_mc-sotdma
cd ../..

# # Clone radio
echo -e "\n\nDownloading channel model"
git clone git@collaborating.tuhh.de:e-4/research-projects/intairnet-collection/intairnet-radio.git
cd intairnet-radio/src
opp_makemake -f -s --deep -O out -KINET4_PROJ=../../inet4 -DINET_IMPORT -I../../inet4 -I. -I../../inet4/src -L../../inet4/src -lINET
#opp_makemake -f -s --deep -O out -KINET4_PROJ=../../inet4 -DINET_IMPORT -I../../inet4 -I. -I../../inet4/src -L../../inet4/src -lINET_dbg
# make MODE=debug -j$NUM_CPUS
make MODE=release -j$NUM_CPUS
cd ../..

# # Clone traceBacedApp
echo -e "\n\nDownloading UdpTracedBasedApp"
git clone git@collaborating.tuhh.de:e-4/research-projects/intairnet-collection/intairnet-tracebasedapp.git
cd intairnet-tracebasedapp/src
opp_makemake --make-so -f --deep -KINET_PROJ=../../inet4 -DINET_IMPORT -I../../inet4/src -L../../inet4/src -lINET
make MODE=release -j$NUM_CPUS

cd ../..

# # Clone tdma
echo -e "\n\nDownloading abstract TDMA"
git clone git@collaborating.tuhh.de:e-4/publications/ahmed-fuger-lindner-omnet-summit-2021/tdma.git
cd tdma/tdma/src
opp_makemake --make-so -f --deep -KINET_PROJ=../../../inet4 -DINET_IMPORT -I../../../inet4/src -L../../../inet4/src -lINET
make MODE=release -j$NUM_CPUS

cd ../../..

# # Clone gpsr
echo -e "\n\nDownloading GPSR modified"
git clone git@collaborating.tuhh.de:e-4/research-projects/intairnet-collection/intairnet-gpsr.git
cd intairnet-gpsr
cd src
opp_makemake -f -s --deep -O out -KINET4_PROJ=../../inet4 -DINET_IMPORT -I../../inet4 -I. -I../../inet4/src -L../../inet4/src -lINET
# make MODE=debug -j$NUM_CPUS
make MODE=release -j$NUM_CPUS

cd ../..

# # Clone aodv
echo -e "\n\nDownloading AODV modified"
git clone git@collaborating.tuhh.de:e-4/research-projects/intairnet-collection/intairnet-aodv.git
cd intairnet-aodv
cd src
opp_makemake -f -s --deep -O out -KINET4_PROJ=../../inet4 -DINET_IMPORT -I../../inet4 -I. -I../../inet4/src -L../../inet4/src -lINET
# make MODE=debug -j$NUM_CPUS
make MODE=release -j$NUM_CPUS

cd ../..

# Clone wrapper
echo -e "\n\nDownloading OMNET++ wrapper"
git clone git@collaborating.tuhh.de:e-4/research-projects/intairnet-collection/intairnet-omnet-wrapper.git
cd intairnet-omnet-wrapper/intairnet-link-layer
echo "Compiling simulation binary"
unlink glue-lib
ln -s ../../intairnet-linklayer-glue/cmake-build-release ./glue-lib
unlink glue-lib-headers
ln -s ../../intairnet-linklayer-glue ./glue-lib-headers

unlink avionic-rlc
ln -s ../../avionic-rlc/cmake-build-release ./avionic-rlc
unlink avionic-rlc-headers
ln -s ../../avionic-rlc ./avionic-rlc-headers

unlink mc-sotdma
ln -s ../../mc-sotdma/cmake-build-release ./mc-sotdma
unlink mc-sotdma-headers
ln -s ../../mc-sotdma ./mc-sotdma-headers

unlink avionic-arq
ln -s ../../avionic-arq/dev/cmake-build-release ./avionic-arq
unlink avionic-arq-headers
ln -s ../../avionic-arq/dev ./avionic-arq-headers
cd src
opp_makemake -f --deep -O out -KINET4_PROJ=../../../inet4 -DINET_IMPORT -I../../../inet4 -I../../../intairnet-tracebasedapp/src -I../../../intairnet-radio/src -I../../../intairnet-gpsr/src -I../glue-lib-headers -I../avionic-rlc-headers -I../avionic-arq-headers -I../mc-sotdma-headers -I. -I../../../inet4/src -L../../../inet4/src -L../../../intairnet-tracebasedapp/out/gcc-release/src/ -L../../../intairnet-radio/out/gcc-release/src/ -L../../../intairnet-gpsr/out/gcc-release/src/ -L../glue-lib -L../avionic-rlc -L../avionic-arq -L../mc-sotdma -lINET -lintairnet-tracebasedapp -lintairnet-radio -lintairnet-gpsr -lintairnet_linklayer_glue -ltuhh_intairnet_rlc -ltuhh_intairnet_arq -ltuhh_intairnet_mc-sotdma
#opp_makemake -f --deep -O out -KINET4_PROJ=../../../inet4 -DINET_IMPORT -I../../../inet4 -I../../../intairnet-traceBasedApp/src -I../../../intairnet-radio/src -I../../../intairnet-gpsr/src -I../glue-lib-headers -I../avionic-rlc-headers -I../avionic-arq-headers -I../mc-sotdma-headers -I. -I../../../inet4/src -L../../../inet4/src -L../../../intairnet-traceBasedApp/out/gcc-release/src/ -L../../../intairnet-radio/out/gcc-debug/src/ -L../../../intairnet-gpsr/out/gcc-debug/src/ -L../glue-lib -L../avionic-rlc -L../avionic-arq -L../mc-sotdma -lINET_dbg -lintairnet-traceBasedApp_dbg -lintairnet-radio_dbg -lintairnet-gpsr_dbg -lintairnet_linklayer_glue -ltuhh_intairnet_rlc -ltuhh_intairnet_arq -ltuhh_intairnet_mc-sotdma
# make MODE=debug -j$NUM_CPUS
make MODE=release -j$NUM_CPUS

cd ../../..

#echo -e "\n\nDownloading abstract TDMA"
#git clone git@collaborating.tuhh.de:e-4/publications/ahmed-fuger-lindner-omnet-summit-2021/tdma.git
#cd tdma/tdma/src
#opp_makemake --make-so -f --deep -KINET_PROJ=../../../inet4 -DINET_IMPORT -I../../../inet4/src -L../../../inet4/src -lINET
#make MODE=release -j$NUM_CPUS

#cd ../../..

#echo -e "\n\nDownloading UdpTracedBasedApp"
#git clone git@collaborating.tuhh.de:e-4/publications/ahmed-fuger-lindner-omnet-summit-2021/application.git intairnet-traceBasedApp
#cd intairnet-traceBasedApp/src
#opp_makemake --make-so -f --deep -KINET_PROJ=../../inet4 -DINET_IMPORT -I../../inet4/src -L../../inet4/src -lINET
#make MODE=release -j$NUM_CPUS

#cd ../..

echo -e "\n\nDownloading GPSR original"
git clone git@collaborating.tuhh.de:e-4/research-projects/intairnet-collection/original-gpsr.git
cd original-gpsr/src
#opp_makemake --make-so -f --deep -KINET_PROJ=../../inet4 -DINET_IMPORT -I../../inet4/src -I../../tdma/tdma/src -I../../intairnet-tracebasedapp/src -L../../inet4/src -L../../tdma/tdma/src -L../../intairnet-tracebasedapp/src -lINET -lintairnet-tracebasedapp -ltdma 
opp_makemake -f --deep -O out -KINET_PROJ=../../inet4 -DINET_IMPORT -I../../inet4/src -I../../tdma/tdma/src -I../../intairnet-tracebasedapp/src -L../../inet4/src -L../../tdma/tdma/src -L../../intairnet-tracebasedapp/src -lINET -lintairnet-tracebasedapp -ltdma
make MODE=release -j$NUM_CPUS

cd ../..

#echo -e "\n\nDownloading GPSR modified"
#git clone git@collaborating.tuhh.de:e-4/research-projects/intairnet-collection/intairnet-gpsr.git
#cd intairnet-gpsr/src
#opp_makemake -f -s --deep -O out -KINET4_PROJ=../../inet4 -DINET_IMPORT -I../../inet4 -I. -I../../inet4/src -L../../inet4/src -lINET
#opp_makemake -f --deep -O out -KINET4_PROJ=../../../inet4 -DINET_IMPORT -I../../../inet4 -I../../../intairnet-traceBasedApp/src -I../../../tdma/tdma/src -I../../../original-gpsr/src -I. -I../../../inet4/src -L../../../inet4/src -L../../../intairnet-traceBasedApp/out/gcc-release/src/ -L../../../tdma/tdma/out/gcc-release/src/ -L../../../original-gpsr/out/gcc-release/src/ -lINET -lintairnet-traceBasedApp -ltdma -loriginal-gpsr
#make MODE=release -j$NUM_CPUS

cd ../../scenarios/results
echo -e "\n\nInstall python packages into local pipenv environment"
make install-python-env
echo -e "\n\nAll done! Try it by running the following commands:\ncd scenarios/results\nmake sanity-check\nThis should start simulations and create graphs in the scenarios/results/_imgs/ directory."

