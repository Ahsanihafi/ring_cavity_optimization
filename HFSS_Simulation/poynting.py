# ----------------------------------------------
# Script Recorded by Ansys Electronics Desktop Version 2022.1.2
# 22:49:38  Jan 06, 2025
# ----------------------------------------------
import ScriptEnv
ScriptEnv.Initialize("Ansoft.ElectronicsDesktop")
oDesktop.RestoreWindow()
oProject = oDesktop.SetActiveProject("Project2")
oDesign = oProject.SetActiveDesign("HFSSDesign1")
oModule = oDesign.GetModule("FieldsReporter")
oModule.CalcStack("clear")
oModule.EnterQty("H")
oModule.EnterSurf("PolyLine1")
oModule.CalcOp("Normal")
oModule.CalcOp("Cross")
oModule.CalcStack("push")
oModule.CalcOp("Conj")
oModule.CalcOp("Dot")
oModule.CalcOp("Real")
oModule.EnterSurf("PolyLine1")
oModule.CalcOp("Integrate")
oModule.ClcEval("Setup1 : LastAdaptive", 
	[
		"Phase:="		, "0deg"
	], "Fields")
oModule.CalculatorWrite("C:\\Users\\Hafi-san\\Documents\\Ansoft\\tes2\\proj\\HHdA.fld", 
	[
		"Solution:="		, "Setup1 : LastAdaptive"
	], 
	[
		"Phase:="		, "0deg"
	])
