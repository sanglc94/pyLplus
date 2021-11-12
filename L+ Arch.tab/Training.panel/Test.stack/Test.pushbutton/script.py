__doc__ = 'Python for revit api'
__author__ = 'L+ Arch'

from Autodesk.Revit.DB import Transaction, BuiltInParameterGroup,IFamilyLoadOptions,FamilySource,Element,ParameterSet,FilteredElementCollector,FamilyInstance,BuiltInCategory
from Autodesk.Revit.UI.Selection.Selection import PickObject 
from Autodesk.Revit.UI.Selection import ObjectType,ISelectionFilter
from pyrevit import forms
from System.Collections.Generic import List

# Get UIDocument
uidoc = __revit__.ActiveUIDocument

# Get Document 
doc = uidoc.Document

# Get Application
app = doc.Application

famIns_col = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Doors).WhereElementIsElementType().ToElements()

for a in famIns_col:
    typeId = a.GetTypeId()
    eleType = doc.GetElement(typeId)
    #if a.get_BoundingBox(doc.ActiveView) != None:
    #    print(a.get_BoundingBox(doc.ActiveView).Max)
    #print(Element.Name.__get__(a))
    print(a.LookupParameter("Width").AsDouble())
    