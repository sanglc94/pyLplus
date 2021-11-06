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
try:
    picks = uidoc.Selection.PickObjects(ObjectType.Element, CustomISelectionFilter("Autodesk.Revit.DB.AnnotationSymbol"), "Select Elements")
    listele = List[Element]()
    for n in picks:
        listele.Add(doc.GetElement(n.ElementId))
    locations = FilteredElementCollector(doc).OfClass(BasePoint)
    for locationPoint in locations:
        basePoint = locationPoint
        if (basePoint.IsShared == True):
            
            # Select XYZ of Survey Point

            svLoc = basePoint.Location
            projectSurvpntX = basePoint.get_Parameter(BuiltInParameter.BASEPOINT_EASTWEST_PARAM).AsDouble()
            projectSurvpntY = basePoint.get_Parameter(BuiltInParameter.BASEPOINT_NORTHSOUTH_PARAM).AsDouble()
            projectSurvpntZ = basePoint.get_Parameter(BuiltInParameter.BASEPOINT_ELEVATION_PARAM).AsDouble()
            #print(svLoc.Point)
            
        else:
            # Select XYZ of Project Base Point (Origin) and Angle to True North
            origin = basePoint.Location
            projectOriginX = basePoint.get_Parameter(BuiltInParameter.BASEPOINT_EASTWEST_PARAM).AsDouble()
            projectOriginY = basePoint.get_Parameter(BuiltInParameter.BASEPOINT_NORTHSOUTH_PARAM).AsDouble()
            projectOriginZ = basePoint.get_Parameter(BuiltInParameter.BASEPOINT_ELEVATION_PARAM).AsDouble()
            angleton = basePoint.get_Parameter(BuiltInParameter.BASEPOINT_ANGLETON_PARAM).AsDouble()
            #print (origin)
            # Create axis for rotate element
            axis = Line.CreateBound(XYZ(projectSurvpntX,projectSurvpntY,projectSurvpntZ), XYZ(projectSurvpntX,projectSurvpntY,projectSurvpntZ+10))

    t = Transaction(doc, "Set Parameters")
    t.Start()
    if len(listele) >= 1:
        for ele in listele:
            # Get Element Type ID
            eletypeid = ele.GetTypeId()
            # Get Eleement Type
            eletype = doc.GetElement(eletypeid)
            # filter family name of element
            if eletypeid in annotationtypeIdList:
                if "Coordinate-Point" in eletype.FamilyName:
                #if "X-Y" not in ele.Name or "Coordinate-Point" in ele.Name:
                #familyName = eletype.FamilyName()
                #print(familyName)
                #if elename in familyName:
                    # select parameter of element
                    param_X = ele.LookupParameter("X")
                    param_Y = ele.LookupParameter("Y")
                    #rotate element with Angle to True North
                    ElementTransformUtils.RotateElement(doc, ele.Id,axis,(math.pi * 2) - angleton)
                    # select new element location point
                    newpoint = ele.Location.Point
                    newpoint_X = newpoint.X
                    newpoint_Y = newpoint.Y
                    # return Coordinate location of element
                    value_X = newpoint_Y + projectOriginY
                    value_Y = newpoint_X + projectOriginX
                    # Set Element Parameter
                    param_X.Set(UnitUtils.ConvertFromInternalUnits(value_X, DisplayUnitType.DUT_METERS))
                    param_Y.Set(UnitUtils.ConvertFromInternalUnits(value_Y, DisplayUnitType.DUT_METERS))
                    # reRotate element
                    ElementTransformUtils.RotateElement(doc, ele.Id,axis,angleton)



    else:
        Alert('Have no selected elements. Please Retry', title="Alert", header="Notification:")
    t.Commit()
except:
    TaskDialog.Show("Notification", "Cancelled")









