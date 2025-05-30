import sys
#sys.path.append("C:/Users/Hafi-san/Documents/Ansoft/2000data0")
sys.path.append("C:/Users/Hafi-san/Documents/data_generator/lower_vertex0")
#sys.path.append(r"D:\app\ansys\v221\Win64")
#sys.path.append(r"D:\app\ansys\v221\Win64\PythonFiles\DesktopPlugin")

import ScriptEnv
import polyline as pol
import calculator as calc
from vertex5 import vertices

class Point:
    def __init__(self, px, py, pz):
        self.px = px
        self.py = py
        self.pz = pz

#point1 = Point(20,-2,0)
#point2 = Point(-90,20,0)
#point3 = Point(10,-14,0)
#point4 = Point(20,-2,0)
#pointlist = [point1,point2,point3,point4]


def main():
    nomor = 369
    vertex = vertices[nomor]
    # Initialize Ansys HFSS
    ScriptEnv.Initialize("Ansoft.ElectronicsDesktop")
    oDesktop.RestoreWindow()
    oProject = oDesktop.NewProject("test")
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
    calc.calcEigen(oModule, oDesign, nomor)
    #oDesktop.CloseProject("Project5")

if __name__ == "__main__":
    main()