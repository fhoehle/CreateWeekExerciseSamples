import FWCore.ParameterSet.Config as cms
from FWCore.ParameterSet.VarParsing import VarParsing
 
options = VarParsing ('analysis')
options.register ('selectSemiMu',
                   True,
                   VarParsing.multiplicity.singleton,
                   VarParsing.varType.bool,
                   "select semi muonic events (gen Lvl)")
options.register ('printGenParts',
                   False,
                   VarParsing.multiplicity.singleton,
                   VarParsing.varType.bool,
                   "print genParticles")
##################################
options.parseArguments()
################################
process = cms.Process('SemiMuSkim')
process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )

process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(-1))
if options.maxEvents != '':
 process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(options.maxEvents))
print "process maxEvents ",process.maxEvents
process.source = cms.Source("PoolSource",
        fileNames = cms.untracked.vstring('/store/relval/CMSSW_7_1_0/RelValProdTTbar_13/AODSIM/POSTLS171_V15-v1/00000/96855E2B-8DFB-E311-9EEB-0025905A60CA.root')
)
if options.inputFiles != cms.untracked.vstring():
 process.source.fileNames=cms.untracked.vstring(options.inputFiles)
process.load('Configuration.StandardSequences.Services_cff')
process.load("FWCore.MessageService.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = 100

process.printList = cms.EDAnalyzer("ParticleListDrawer",
        src = cms.InputTag("genParticles"),
        maxEventsToPrint = cms.untracked.int32(10)
)
process.TFileService=cms.Service("TFileService",fileName=cms.string('test_SemiMuMcFilter_histos.root'))
genPlots = cms.PSet(
    histograms = cms.VPSet(
    cms.PSet(
    min = cms.untracked.double(-22.33),
    max = cms.untracked.double(22.33),
    nbins = cms.untracked.int32(89),
    name = cms.untracked.string("pdgId"),
    description = cms.untracked.string("pdgId"),
    plotquantity = cms.untracked.string("pdgId"))
    )
  )
process.genHists = cms.EDAnalyzer(
    "CandViewHistoAnalyzer",
    genPlots,
    src = cms.InputTag("genPatStatus3")
)   

process.genMuons  = cms.EDFilter("CandViewSelector",
    src = cms.InputTag("genParticles"),
    cut = cms.string(' abs(pdgId) == 13 && abs(status) == 3'),
    #filter = cms.bool(True) 
)

process.genMuonsFilter = cms.EDFilter("CandViewCountFilter",
   src       = cms.InputTag("genMuons"),
   minNumber = cms.uint32(1),
   maxNumber = cms.uint32(1)
)
 
process.selectSemiMu = cms.Path(process.genMuons) 
if options.printGenParts:
  process.selectSemiMu.insert(0,process.printList)
if options.selectSemiMu:
  process.selectSemiMu += process.genMuonsFilter 
else:
  process.selectSemiMu += ~process.genMuonsFilter

process.output = cms.OutputModule("PoolOutputModule",
                                  fileName = cms.untracked.string('ttbarEvents_semiMutagged_signal.root' if options.selectSemiMu else 'ttbarEvents_semiMutagged_background.root'),
                                  SelectEvents = cms.untracked.PSet(
		SelectEvents = cms.vstring('selectSemiMu')
	),
	outputCommands = cms.untracked.vstring('keep *')
)

if options.outputFile != 'output.root' and  options.outputFile != None and not options.outputFile.startswith('output_numEvent'):
  process.output.fileName.setValue(options.outputFile)
else:
  if options.maxEvents != -1:
    import os
    fileName,ext = os.path.splitext(process.output.fileName.value())
    process.output.fileName.setValue(fileName+'_numEvent'+str(options.maxEvents)+ext)
################
process.output_step = cms.EndPath(process.output)
################
print "source ",process.source.fileNames
print "output ",process.output.fileName
