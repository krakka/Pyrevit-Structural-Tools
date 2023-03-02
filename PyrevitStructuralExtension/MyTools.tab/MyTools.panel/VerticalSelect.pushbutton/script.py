"""Select all columns with similar X,Y"""

from pyrevit import revit, DB

doc = __revit__.ActiveUIDocument.Document

def get_parameter_value_by_name(element, parameterName):
	return element.LookupParameter(parameterName).AsValueString()

def point_close(_pointA,_pointB):
    return abs(_pointA.X-_pointB.X) < 2 and abs(_pointA.Y-_pointB.Y) < 2

selection = revit.get_selection()

baselocation = selection[0].Location.Point

_collector = DB.FilteredElementCollector(doc).OfCategory(DB.BuiltInCategory.OST_StructuralColumns).WhereElementIsNotElementType()

selSet = []

for _col in _collector:
    if point_close(_col.Location.Point,baselocation):
        selSet.append(_col)

revit.get_selection().set_to(selSet)