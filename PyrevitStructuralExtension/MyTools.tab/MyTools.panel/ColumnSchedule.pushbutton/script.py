from Autodesk.Revit.DB import *
from pyrevit import DB, revit
import math

doc = __revit__.ActiveUIDocument.Document

active_view = doc.ActiveView

all_schedule_cols = []

#calculate character worth for alphanumeric sorting
def characterworth(string):
    val = 0.0
    counter = 1.0
    for x in string:
        val = val + ord(x)/counter*x.isdigit() + ord(x)/(255*counter)*x.isalpha()
        counter = counter * 10
    return val

class ScheduleColumn:
    def __init__(self,name):
        self.name = name
        self.number = characterworth(name)
        self.columns = []
        self.boundingbox = None

#get every column family
collector_columns = DB.FilteredElementCollector(doc).OfCategory(DB.BuiltInCategory.OST_StructuralColumns).WhereElementIsNotElementType()

# Filter out non-concrete families
all_concrete_cols = []
for column in collector_columns:
    if "Concrete" in doc.GetElement(column.GetTypeId()).Family.Name:
        all_concrete_cols.append(column)

# Get guid (for faster searching) to get column mark no
guid_columnmarkno = all_concrete_cols[0].LookupParameter("Column Mark No").GUID

unique_marks = set([col.get_Parameter(guid_columnmarkno).AsString() for col in all_concrete_cols])

# Create column objects
for i in unique_marks:
    all_schedule_cols.append(ScheduleColumn(i))

for k in all_schedule_cols:
    for j in all_concrete_cols:
        if k.name == j.get_Parameter(guid_columnmarkno).AsString():
            k.columns.append(j)

# Create bounding box and expand to all columns
def getboundingboxlimits(allcols):  
    bb_primary = allcols[0].GetBoundingBox()
    min_x = bb_primary.Min.X
    min_y = bb_primary.Min.Y
    min_z = bb_primary.Min.Z
    max_x = bb_primary.Max.X
    max_y = bb_primary.Max.Y
    max_z = bb_primary.Max.Z

    for elem in allcols:
        bb_max = elem.GetBoundingBox().Max
        max_x = max(bb_max.X,max_x)
        max_y = max(bb_max.Y,max_y)
        max_z = max(bb_max.Z,max_z)
        bb_min = elem.GetBoundingBox().Min
        min_x = min(bb_min.X,min_x)
        min_y = min(bb_min.Y,min_y)
        min_z = min(bb_min.Z,min_z)
    
    bb_max = XYZ(max_x,max_y,max_z)
    bb_min = XYZ(min_x,min_y,min_z)
    bb_primary.Max = bb_max
    bb_primary.Min = bb_min
    return bb_primary

# get column angle
def angle_column(_col):
    xval = _col.GetTransform().BasisX.X
    yval = _col.GetTransform().BasisX.Y
    rot = round(math.atan2(yval,xval)*180/math.pi,0)
    if rot > 90:
        rot = rot-90
    elif rot <= -90:
        rot = rot + 180
    elif rot < 0:
        rot = rot + 90
    return rot

# get mode angle of columns
def angle_mode(_colcol):
    angles = []
    for i in _colcol.columns:
        if "Rectangular" in doc.GetElement(i.GetTypeId()).Family.Name:
            angles.append(angle_column(i))
    if angles == []:
        modeangle = 0
    else:
        modeangle = max(set(angles), key=angles.count)
    return modeangle

# Get geometry with default options
def getangledgeometry(_colcol):
    originaltransform = _colcol.columns[0].GetTransform()
    rotatedtransform = originaltransform.CreateRotation(originaltransform.BasisZ,angle_mode(_colcol))

    transformedgeometry = []

    for i in _colcol.columns:
        temp_geom = i.get_Geometry(Options())
        temp_rotated = temp_geom.GetTransformed(rotatedtransform)
        transformedgeometry.append(temp_rotated)
    
    bb_rotated = getboundingboxlimits(transformedgeometry)
    bbox_min = bb_rotated.Min
    print(bbox_min)
    bbox_min = originaltransform.Inverse.OfPoint(bbox_min)
    bbox_max = bb_rotated.Max
    print(bbox_max)
    bbox_max = originaltransform.Inverse.OfPoint(bbox_max)

    section_box = DB.BoundingBoxXYZ()
    section_box.Transform = rotatedtransform
    section_box.Min = bbox_min
    section_box.Max = bbox_max

    return section_box

getangledgeometry(all_schedule_cols[0])

# t = Transaction(doc, 'cropping view')
# t.Start()

# active_view.SetSectionBox(getangledgeometry(all_schedule_cols[0]))

# t.Commit()


# def get_section_viewfamily():
#     return revit.doc.GetDefaultElementTypeId(
#         DB.ElementTypeGroup.ViewTypeSection
#         )


# section_type = get_section_viewfamily()

# DB.ViewSection.CreateSection(revit.doc, section_type, getangledgeometry(all_schedule_cols[0]))