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
process = cms.Process('Analysis')
process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )

process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(-1))
if options.maxEvents != '':
 process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(options.maxEvents))
print process.maxEvents
process.source = cms.Source("PoolSource",
        fileNames = cms.untracked.vstring('file:semiTTbar_AOD_numEvent100.root')
)
if options.inputFiles != cms.untracked.vstring():
 process.source.fileNames=cms.untracked.vstring(options.inputFiles)

process.load('Configuration.StandardSequences.Services_cff')
process.load("FWCore.MessageService.MessageLogger_cfi")
process.MessageLogger.cerr.threshold = 'INFO'
process.MessageLogger.cerr.FwkReport.reportEvery = 100

from TopQuarkAnalysis.Configuration.patRefSel_triggerSelection_cff import triggerResults
process.selectMCTTbarSemiMu = triggerResults
process.selectMCTTbarSemiMu.hltResults = cms.InputTag("TriggerResults","","SemiMuSkim")
process.selectMCTTbarSemiMu.triggerConditions = cms.vstring('generation_step')
process.p = cms.Path(process.selectMCTTbarSemiMu)

#process.output = cms.OutputModule("PoolOutputModule",
#                                  fileName = cms.untracked.string('semiMuTTbar.root'),
#                                  SelectEvents = cms.untracked.PSet(
#		SelectEvents = cms.vstring()
#	),
#	outputCommands = cms.untracked.vstring('keep *','drop *_myTTbarGenEvent10Parts_*_*')#,'keep *_MyTTbarGenEventProd_*_*')
#)
#if options.outputFile != 'output.root' and  options.outputFile != None:
#  process.output.fileName.setValue(options.outputFile)
#process.output_step = cms.EndPath(process.output)
print "source ",process.source.fileNames
#print "output ",process.output.fileName
