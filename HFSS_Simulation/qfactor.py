# ----------------------------------------------
# Script Recorded by Ansys Electronics Desktop Version 2022.1.2
# 22:09:12  Jan 06, 2025
# ----------------------------------------------
import ScriptEnv
ScriptEnv.Initialize("Ansoft.ElectronicsDesktop")
oDesktop.RestoreWindow()
oProject = oDesktop.SetActiveProject("Project2")
oDesign = oProject.SetActiveDesign("HFSSDesign1")
oModule = oDesign.GetModule("FieldsReporter")
oModule.EnterQty("H")
oModule.EnterSurf("PolyLine1")
oModule.CalcOp("Normal")
oModule.CalcOp("Cross")
oModule.CalcStack("push")
oModule.CalcOp("Conj")
oModule.CalcOp("Dot")
oModule.CalcOp("CmplxR")
oModule.CalcOp("Abs")
oModule.CalcStack("undo")
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
