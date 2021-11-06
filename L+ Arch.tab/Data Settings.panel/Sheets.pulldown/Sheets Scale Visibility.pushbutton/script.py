__doc__ = 'Python for revit api'
__author__ = 'L+ Arch'
from Autodesk.Revit.DB import Transaction, FilteredElementCollector,BuiltInCategory
from Autodesk.Revit.UI import UIDocument, Selection

uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document

titleblock_col = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_TitleBlocks).WhereElementIsNotElementType().ToElements()

t = Transaction(doc, "Scale Visibility")
t.Start()

for tb in titleblock_col:
    param = tb.LookupParameter("Scale")
    paramVisibility = tb.LookupParameter("Scale Visibility")
    if paramVisibility != None:
        if param.AsString() != "As indicated":
            paramVisibility.Set(1)
        else:
            paramVisibility.Set(0)

t.Commit()