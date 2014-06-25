cmsswVer=CMSSW_7_1_0


echo "Installing ... "
#
#export SCRAM_ARCH=slc5_amd64_gcc462
if [ -z "$CMSSW_BASE" ]; then
  if [[ "$PWD" =~ "$cmsswVer" ]]; then
   echo "you forgot cmsenv"
  else
   echo "creating "$cmsswVer
   scramv1 project CMSSW $cmsswVer # this is cmsrel
   cd $cmsswVer
 fi
else
  cd $CMSSW_BASE
fi
eval `scramv1 runtime -sh` # this is cmsenv
cd src
##
git clone git@github.com:fhoehle/CMSSW_MyDataFormats.git
cd CMSSW_MyDataFormats
#git checkout V00-01
cd $CMSSW_BASE/src

git clone git@github.com:fhoehle/CMSSW_MyFilters.git
cd CMSSW_MyFilters
#git checkout V00-01
cd $CMSSW_BASE/src

git clone git@github.com:fhoehle/CMSSW_MyProducers.git
cd CMSSW_MyProducers
#git checkout V00-01
cd $CMSSW_BASE/src

scram b -j 4
cd $CMSSW_BASE/CreateWeekExerciseSamples
 
