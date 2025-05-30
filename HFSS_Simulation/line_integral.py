# ----------------------------------------------
# Script Recorded by Ansys Electronics Desktop Version 2022.1.2
# 15:35:15  Jan 06, 2025
# ----------------------------------------------
import ScriptEnv
ScriptEnv.Initialize("Ansoft.ElectronicsDesktop")
oDesktop.RestoreWindow()
oProject = oDesktop.SetActiveProject("Project2")
oDesign = oProject.SetActiveDesign("HFSSDesign1")
oModule = oDesign.GetModule("FieldsReporter")
oModule.EnterQty("E")
oModule.CalcOp("Real")
oModule.EnterLine("integral_line")
oModule.CalcOp("TangentComponent")
oModule.CalcOp("Integrate")
oModule.CalcOp("Abs")
oModule.ClcEval("Setup1 : LastAdaptive", 
	[
		"Phase:="		, "0deg"
	], "Fields")
oModule.CalculatorWrite("C:\\Users\\Hafi-san\\Documents\\Ansoft\\tes2\\proj\\accE.fld", 
	[
		"Solution:="		, "Setup1 : LastAdaptive"
	], 
	[
		"Phase:="		, "0deg"
	])
