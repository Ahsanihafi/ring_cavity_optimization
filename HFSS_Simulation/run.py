import sys
sys.path.append("C:/Users/Hafi-san/Documents/data_generator/lower_vertex0")
#sys.path.append(r"D:\app\ansys\v221\Win64")
#sys.path.append(r"D:\app\ansys\v221\Win64\PythonFiles\DesktopPlugin")

import ScriptEnv
import polyline as pol
import calculator as calc
from vertex0 import vertices

class Point:
    def __init__(self, px, py, pz):
        self.px = px
        self.py = py
        self.pz = pz

#step: 
#0 pastikan syspath sesuai dengan lokasi code
#1 ganti vertex_i
#2 ganti n_awal
#3 ganti range kalau ada yang terputus
#4 ganti nomor closeproject kalau terputus

def main():
    n_awal = 0 #i*1000
    for i in range(1000):
        vertex = vertices[i]
        # Initialize Ansys HFSS
        ScriptEnv.Initialize("Ansoft.ElectronicsDesktop")
        oDesktop.RestoreWindow()
        oProject = oDesktop.NewProject("run")
        oProject.InsertDesign("HFSS", "HFSSDesign1", "Eigenmode", "")
        oDesign = oProject.SetActiveDesign("HFSSDesign1")
        oModule = oDesign.GetModule("AnalysisSetup")
        oEditor = oDesign.SetActiveEditor("3D Modeler")

        # Call the create_polyline function
        pol.create_polyline1(oEditor)
        pol.create_polyline2(oEditor,vertex)
        pol.extrusion(oEditor)
        pol.assignMaterial(oEditor)
        pol.assignPEC(oDesign)
        calc.calcEigen(oModule, oDesign, i+n_awal)
        oDesktop.CloseProject("run15")

if __name__ == "__main__":
    main()