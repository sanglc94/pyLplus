__doc__ = 'Python for revit api'
__author__ = 'L+ Arch'
from Autodesk.Revit.DB import (Transaction, FilteredElementCollector,BuiltInParameter, BuiltInCategory, Definition, Line, XYZ,
                                Element, View, ElementId, FamilyInstance, BasePoint, UnitUtils, DisplayUnitType, Transform,
                                FillPatternElement, Color, OverrideGraphicSettings, ElementTransformUtils)
from Autodesk.Revit.UI import UIDocument, Selection,TaskDialog
from Autodesk.Revit.UI.Selection.Selection import PickObject 
from Autodesk.Revit.UI.Selection import ObjectType,ISelectionFilter
import random
from rpw.ui.forms import FlexForm, Label, Separator, Button, Alert, TextBox
from rpw import ui
import math
from System.Collections.Generic import List

# Get UIDocument
uidoc = __revit__.ActiveUIDocument

# Get Document 
doc = uidoc.Document

annotation_col = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_GenericAnnotation).WhereElementIsElementType().ToElementIds()
annotationtypeIdList = []
for anno in annotation_col:
    annotationtypeIdList.append(anno)


class CustomISelectionFilter(ISelectionFilter):
    def __init__(self, nom_categorie):
        self.nom_categorie = nom_categorie
    def AllowElement(self, e):
        if e.GetType().FullName == self.nom_categorie:
            return True
        else:
            return False
    def AllowReference(self, ref, point):
        return True
        
# Pick elements
#listele = uidoc.Selection.PickElementsByRectangle("Selection by Rectangle")
#listele = ui.Pick.pick_by_rectangle("Selection by Rectangle")
picks = uidoc.Selection.PickObjects(ObjectType.Element,"Select Element")
listele = List[Element]()
for n in picks:
    listele.Add(doc.GetElement(n.ElementId))
for ele in listele:
    print(ele.GetType().FullName)