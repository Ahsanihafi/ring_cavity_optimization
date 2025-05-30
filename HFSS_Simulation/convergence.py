# ----------------------------------------------
# Script Recorded by Ansys Electronics Desktop Version 2022.1.2
# 18:10:10  Jan 14, 2025
# ----------------------------------------------
import ScriptEnv
ScriptEnv.Initialize("Ansoft.ElectronicsDesktop")
oDesktop.RestoreWindow()
oProject = oDesktop.SetActiveProject("Project2")
oDesign = oProject.SetActiveDesign("HFSSDesign1")
oDesign.ExportConvergence("Setup1", "", "D:/ring_cyclotron/convergence/conv1.conv")
