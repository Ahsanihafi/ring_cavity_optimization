def calcEigen(oModule, oDesign, i):
    oModule.InsertSetup("HfssEigen", 
        [
            "NAME:Setup1",
            "MinimumFrequency:="	, "20MHz",
            "NumModes:="		, 1,
            "MaxDeltaFreq:="	, 0.001,
            "ConvergeOnRealFreq:="	, False,
            "MaximumPasses:="	, 15,
            "MinimumPasses:="	, 5,
            "MinimumConvergedPasses:=", 1,
            "PercentRefinement:="	, 30,
            "IsEnabled:="		, True,
            [
                "NAME:MeshLink",
                "ImportMesh:="		, False
            ],
            "BasisOrder:="		, 2,
            "DoLambdaRefine:="	, True,
            "DoMaterialLambda:="	, False,
            "SetLambdaTarget:="	, False,
            "Target:="		, 0.4,
            "UseMaxTetIncrease:="	, True
        ])
    oDesign.AnalyzeAll()
    oModule = oDesign.GetModule("Solutions")
    oModule.ExportEigenmodes("Setup1 : LastAdaptive", "", "C:\\Users\\Hafi-san\\Documents\\data_generator\\lower_vertex0\\single\\freq\\freq%d.eig" %i)
    oDesign.ExportConvergence("Setup1", "", "C:\\Users\\Hafi-san\\Documents\\data_generator\\lower_vertex0\\single\\convergence\\conv%d.conv" %i)
    oModule = oDesign.GetModule("FieldsReporter")
    oModule.CopyNamedExprToStack("Mag_E")
    oModule.EnterVol("PolyLine1")
    oModule.CalcOp("Maximum")
    oModule.ClcEval("Setup1 : LastAdaptive", 
        [
            "Phase:="		, "0deg"
        ], "Fields")
    oModule.CalculatorWrite("C:\\Users\\Hafi-san\\Documents\\data_generator\\lower_vertex0\\single\\maxE\\maxE%d.fld" %i, 
        [
            "Solution:="		, "Setup1 : LastAdaptive"
        ], 
        [
            "Phase:="		, "0deg"
        ])
    oModule.CalcStack("clear")
    oModule.CopyNamedExprToStack("ComplexMag_H")
    oModule.EnterVol("PolyLine1")
    oModule.CalcOp("Maximum")
    oModule.ClcEval("Setup1 : LastAdaptive", 
        [
            "Phase:="		, "0deg"
        ], "Fields")
    oModule.CalculatorWrite("C:\\Users\\Hafi-san\\Documents\\data_generator\\lower_vertex0\\single\\maxH\\maxH%d.fld" %i, 
        [
            "Solution:="		, "Setup1 : LastAdaptive"
        ], 
        [
            "Phase:="		, "0deg"
        ])
    oModule.CalcStack("clear")
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
    oModule.CalculatorWrite("C:\\Users\\Hafi-san\\Documents\\data_generator\\lower_vertex0\\single\\accE\\accE%d.fld"%i, 
        [
            "Solution:="		, "Setup1 : LastAdaptive"
        ], 
        [
            "Phase:="		, "0deg"
        ])
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
    oModule.CalculatorWrite("C:\\Users\\Hafi-san\\Documents\\data_generator\\lower_vertex0\\single\\hhdA\\HHdA%d.fld"%i, 
        [
            "Solution:="		, "Setup1 : LastAdaptive"
        ], 
        [
            "Phase:="		, "0deg"
        ])


    
    
