from Autodesk.Revit.DB import *
from pyrevit import revit, DB

#get every column family
_linestyles = revit.query.get_line_styles(doc=revit.doc)

print(list(_linestyles[0].GraphicsStyleCategory.GetGraphicsStyle()))

# for _lines in _linestyles:
#     print(_lines)

