# ----------------------------------------------
# Script Recorded by Ansys Electronics Desktop Version 2022.1.2
# 14:35:16  Jan 06, 2025
# ----------------------------------------------
import ScriptEnv
ScriptEnv.Initialize("Ansoft.ElectronicsDesktop")
oDesktop.RestoreWindow()
oProject = oDesktop.SetActiveProject("Project1")
oDesign = oProject.SetActiveDesign("HFSSDesign1")
oModule = oDesign.GetModule("AnalysisSetup")
oModule.InsertSetup("HfssEigen", 
	[
		"NAME:Setup1",
		"MinimumFrequency:="	, "0.1GHz",
		"NumModes:="		, 1,
		"MaxDeltaFreq:="	, 10,
		"ConvergeOnRealFreq:="	, False,
		"MaximumPasses:="	, 10,
		"MinimumPasses:="	, 3,
		"MinimumConvergedPasses:=", 2,
		"PercentRefinement:="	, 30,
		"IsEnabled:="		, True,
		[
			"NAME:MeshLink",
			"ImportMesh:="		, False
		],
		"BasisOrder:="		, 2,
		"DoLambdaRefine:="	, True,
		"DoMaterialLambda:="	, True,
		"SetLambdaTarget:="	, False,
		"Target:="		, 0.4,
		"UseMaxTetIncrease:="	, False
	])
oProject.SaveAs("C:\\Users\\Hafi-san\\Documents\\Ansoft\\tes2\\proj\\Project2.aedt", True)
oDesign.AnalyzeAll()
oModule = oDesign.GetModule("Solutions")
oModule.ExportEigenmodes("Setup1 : LastAdaptive", "", "C:\\Users\\Hafi-san\\Documents\\Ansoft\\tes2\\proj\\freq1.eig")
oModule = oDesign.GetModule("FieldsReporter")
oModule.CopyNamedExprToStack("Mag_E")
oModule.EnterVol("PolyLine1")
oModule.CalcOp("Maximum")
oModule.ClcEval("Setup1 : LastAdaptive", 
	[
		"Phase:="		, "0deg"
	], "Fields")
oModule.CalculatorWrite("C:\\Users\\Hafi-san\\Documents\\Ansoft\\tes2\\proj\\maxE.fld", 
	[
		"Solution:="		, "Setup1 : LastAdaptive"
	], 
	[
		"Phase:="		, "0deg"
	])
oModule.CalcStack("clear")
oModule.CopyNamedExprToStack("Mag_H")
oModule.EnterVol("PolyLine1")
oModule.CalcOp("Maximum")
oModule.ClcEval("Setup1 : LastAdaptive", 
	[
		"Phase:="		, "0deg"
	], "Fields")
oModule.CalculatorWrite("C:\\Users\\Hafi-san\\Documents\\Ansoft\\tes2\\proj\\maxH.fld", 
	[
		"Solution:="		, "Setup1 : LastAdaptive"
	], 
	[
		"Phase:="		, "0deg"
	])
oModule.CalcStack("clear")

