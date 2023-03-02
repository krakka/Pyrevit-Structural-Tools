#!python3

import shapely as sp

uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document

selection = [doc.GetElement(x) for x in uidoc.Selection.GetElementIds()]

for x in selection:
    _curvarray = doc.GetElement(x.SketchId).Profile
    print(_curvarray)
    for y in _curvarray[0]:
        print(y)