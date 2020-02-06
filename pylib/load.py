import ROOT
ROOT.gSystem.AddIncludePath("-Isrc")
ROOT.gSystem.AddIncludePath("-IIbdSel")
ROOT.gSystem.AddIncludePath("-IIbdSel/selector/stage1")
ROOT.gSystem.AddIncludePath("-IIbdSel/selector/stage2")
# ROOT.gSystem.AddIncludePath("-Iselector/SelectorFramework/core")
ROOT.PyConfig.IgnoreCommandLineOptions = True

import numpy as np
error = np.zeros(1, dtype='int32')
files_to_compile = [
        ".L src/stage1_test.cc+",
        ".L IbdSel/selector/stage1/stage1_main.cc+",
        ".L IbdSel/selector/stage2/stage2_main.cc+"
        ]
for line in files_to_compile:
    ROOT.gROOT.ProcessLine(line, error)
    if error[0]:
        raise Exception('Error processing: '+line)

ROOT.Phase, ROOT.Site                 # preload

