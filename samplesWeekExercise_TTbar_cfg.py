import FWCore.ParameterSet.Config as cms
from FWCore.ParameterSet.VarParsing import VarParsing
 
options = VarParsing ('analysis')
# add a list of strings for events to process
#options.register ('eventsToProcess',
#                   '',
#                   VarParsing.multiplicity.list,
#                   VarParsing.varType.string,
#                   "Events to process")
#options.register ('maxSize',
#                   0,
#                   VarParsing.multiplicity.singleton,
#                   VarParsing.varType.int,
#                   "Maximum (suggested) file size (in Kb)")

options.parseArguments()
process = cms.Process('SemiMuSkim')
process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )

process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(-1))
if options.maxEvents != '':
 process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(options.maxEvents))
print process.maxEvents
process.source = cms.Source("PoolSource",
        fileNames = cms.untracked.vstring('/store/mc/Fall11/TT_TuneZ2_7TeV-mcatnlo/AODSIM/PU_S6_START42_V14B-v1/0001/FED956DF-7F2A-E111-8124-002618943958.root',
'/store/mc/Fall11/TT_TuneZ2_7TeV-mcatnlo/AODSIM/PU_S6_START42_V14B-v1/0001/FE77BD53-752A-E111-AD03-002618943905.root',
'/store/mc/Fall11/TT_TuneZ2_7TeV-mcatnlo/AODSIM/PU_S6_START42_V14B-v1/0001/FE51F179-732A-E111-8586-002618943985.root',
'/store/mc/Fall11/TT_TuneZ2_7TeV-mcatnlo/AODSIM/PU_S6_START42_V14B-v1/0001/FE35F649-6F2A-E111-A7F7-00261894392C.root',
'/store/mc/Fall11/TT_TuneZ2_7TeV-mcatnlo/AODSIM/PU_S6_START42_V14B-v1/0001/FC77ECAD-7A2A-E111-829B-002618943877.root',
'/store/mc/Fall11/TT_TuneZ2_7TeV-mcatnlo/AODSIM/PU_S6_START42_V14B-v1/0001/FC2D45A8-672A-E111-BF45-0026189438C4.root')
)
if options.inputFiles != cms.untracked.vstring():
 process.source.fileNames=cms.untracked.vstring(options.inputFiles)

process.load('Configuration.StandardSequences.Services_cff')
process.load("FWCore.MessageService.MessageLogger_cfi")
process.MessageLogger.cerr.threshold = 'INFO'
process.MessageLogger.cerr.FwkReport.reportEvery = 100

process.load("CMSSW_MyFilters.SemiMuMcFilter.semiMuMcFilter_cfi")
process.printList = cms.EDAnalyzer("ParticleListDrawer",
        src = cms.InputTag("genParticles"),
        maxEventsToPrint = cms.untracked.int32(10)
)
process.TFileService=cms.Service("TFileService",fileName=cms.string('test_SemiMuMcFilter_histos.root'))

process.generation_step = cms.Path(process.myTTbarGenEvent10Parts*process.SemiMuMcFilter )#* process.genHists)# * process.printList)

process.output = cms.OutputModule("PoolOutputModule",
                                  fileName = cms.untracked.string('ttbarEvents_semiMutagged_5_3_11.root'),
                                  SelectEvents = cms.untracked.PSet(
		SelectEvents = cms.vstring()
	),
	outputCommands = cms.untracked.vstring('keep *','drop *_myTTbarGenEvent10Parts_*_*')#,'keep *_MyTTbarGenEventProd_*_*')
)
if options.outputFile != 'output.root' and  options.outputFile != None:
  process.output.fileName.setValue(options.outputFile)
process.output_step = cms.EndPath(process.output)
print "source ",process.source.fileNames
print "output ",process.output.fileName
