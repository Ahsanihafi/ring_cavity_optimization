def create_polyline1(oEditor):
    oEditor.CreatePolyline(
    [
        "NAME:PolylineParameters",
        "IsPolylineCovered:=", False,
        "IsPolylineClosed:=", False,
    [
        "NAME:PolylinePoints",
        [
            "NAME:PLPoint",
            "X:="   ,   "-25cm",
            "Y:="   ,   "0cm",
            "Z:="   ,   "165cm"
        ],
        [
            "NAME:PLPoint",
            "X:="   ,   "25cm",
            "Y:="   ,   "0cm",
            "Z:="   ,   "165cm"
        ]    
    ],
    [
        "NAME:PolylineSegments",
        [
            "NAME:PLSegment",
            "SegmentType:=" , "Line",
            "StartIndex:=" , 0,
            "NoOfPoints:=", 2
        ]
    ],
    [
        "NAME:PolylineXSection",
        "XSectionType:="    , "None",
        "XSectionOrient:="  , "Auto",
        "XSectionWidth:="   , "0cm",
        "XSectionTopWidth:=" , "0cm",
        "XSectionHeight:="  , "0cm",
        "XSectionNumSegments:=", "0",
        "XSectionBendType:=", "Corner",
    ]],
    [
        "NAME:Attributes",
        "Name:="    , "integral_line",
        "Flags:="   , "",
        "Color:="   , "(143 175 143)",
        "Transparency:="    , 0,
        "PartCoordinateSystem:=", "Global",
        "UDMId:="   , "",
        "MaterialValue:="   , "\"copper\"",
        "SurfaceMaterialValue:=" , "\"\"",
        "SolveInside:="     , False,
        "ShellElement:="    , False,
        "ShellElementThickness:="   , "0mm",
        "IsMaterialEditable:="  , True,
        "UseMaterialAppearance:=", False,
        "IsLightweight:="   , False
    ]
    )
def create_polyline2(oEditor, vertices):
    # Dynamically generate the "PolylinePoints"
    polyline_points = [["NAME:PLPoint", "X:=", v["X"], "Y:=", v["Y"], "Z:=", v["Z"]] for v in vertices]

    # Dynamically generate the "PolylineSegments"
    polyline_segments = [
        ["NAME:PLSegment", "SegmentType:=", "Line", "StartIndex:=", i, "NoOfPoints:=", 2]
        for i in range(len(vertices) - 1)
    ]
    # Close the polyline by connecting the last point to the first
    polyline_segments.append(
        ["NAME:PLSegment", "SegmentType:=", "Line", "StartIndex:=", len(vertices) - 1, "NoOfPoints:=", 2]
    )

    # Call oEditor.CreatePolyline
    oEditor.CreatePolyline(
        [
            "NAME:PolylineParameters",
            "IsPolylineCovered:=", True,
            "IsPolylineClosed:=", True,
            ["NAME:PolylinePoints"] + polyline_points,
            ["NAME:PolylineSegments"] + polyline_segments,
            [
                "NAME:PolylineXSection",
                "XSectionType:=", "None",
                "XSectionOrient:=", "Auto",
                "XSectionWidth:=", "0cm",
                "XSectionTopWidth:=", "0cm",
                "XSectionHeight:=", "0cm",
                "XSectionNumSegments:=", "0",
                "XSectionBendType:=", "Corner",
            ],
        ],
        [
            "NAME:Attributes",
            "Name:=", "PolyLine1",
            "Flags:=", "",
            "Color:=", "(143 175 143)",
            "Transparency:=", 0,
            "PartCoordinateSystem:=", "Global",
            "UDMId:=", "",
            "MaterialValue:=", "\"copper\"",
            "SurfaceMaterialValue:=", "\"\"",
            "SolveInside:=", False,
            "ShellElement:=", False,
            "ShellElementThickness:=", "0mm",
            "IsMaterialEditable:=", True,
            "UseMaterialAppearance:=", False,
            "IsLightweight:=", False,
        ],
    )

def extrusion(oEditor):
    oEditor.SweepAlongVector(
        [
            "NAME:Selections",
            "Selections:=", "PolyLine1",
            "NewPartsModelFlag:=", "Model"
        ],
        [
            "NAME:VectorSweepParameters",
            "DraftAngle:=", "0deg",
            "DraftType:=", "Round",
            "CheckFaceFaceIntersection:=", False,
            "SweepVectorX:=", "0cm",
            "SweepVectorY:=", "0cm",
            "SweepVectorZ:=", "330cm"
        ]
    )

def assignMaterial(oEditor):
    oEditor.AssignMaterial(
        [
            "NAME:Selections",
            "Selections:=", "PolyLine1"
        ],
        [
            "NAME:Attributes",
            "MaterialValue:=", "\"vacuum\"",
            "SolveInside:=", True
        ]
    )

def assignPEC(oDesign):
    oModule = oDesign.GetModule("BoundarySetup")
    oModule.AssignPerfectE(
        [
            "NAME:PerfectE1",
            "Objects:=", ["PolyLine1"],
            "InfGroundPlane:=", False
        ]
    )