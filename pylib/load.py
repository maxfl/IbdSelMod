import ROOT
ROOT.gSystem.AddIncludePath("-Iselector/stage1")
ROOT.gSystem.AddIncludePath("-Iselector/stage2")
# ROOT.gSystem.AddIncludePath("-Iselector/SelectorFramework/core")
ROOT.PyConfig.IgnoreCommandLineOptions = True

import numpy as np
error = np.zeros(1, dtype='int32')
for line in (".L selector/stage1/stage1_main.cc+", ".L selector/stage2/stage2_main.cc+"):
    ROOT.gROOT.ProcessLine(line, error)
    if error[0]:
        raise Exception('Error processing: '+line)

ROOT.Phase, ROOT.Site                 # preload

