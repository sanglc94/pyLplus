from Autodesk.Revit.DB import (FilteredElementCollector,PropertyLine,XYZ,BasePoint,BuiltInParameter,ElementTransformUtils,
                                Options,Transaction,FamilySymbol,BuiltInCategory,UnitUtils,Element,DisplayUnitType,Line)
from Autodesk.Revit.UI import UIDocument, Selection,TaskDialog
from Autodesk.Revit.UI.Selection.Selection import PickObject 
from Autodesk.Revit.UI.Selection import ObjectType,ISelectionFilter
import math
from rpw.ui.forms import Alert
from System.Collections.Generic import List

uidoc = __revit__.ActiveUIDocument
doc = uidoc.Document

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
try:        
# Pick elements
    picks = uidoc.Selection.PickObjects(ObjectType.Element, CustomISelectionFilter("Autodesk.Revit.DB.PropertyLine"),"Select Property Line")
    col = List[Element]()
    for n in picks:
        col.Add(doc.GetElement(n.ElementId))


    options = Options()
    options.View = doc.ActiveView
    options.IncludeNonVisibleObjects = True

    pointList = []
    #col = FilteredElementCollector(doc, doc.ActiveView.Id).OfClass(PropertyLine).ToElements()
    eleCol = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_GenericAnnotation).OfClass(FamilySymbol)#WhereElementIsElementType().ToElementIds()
    for c in col:
        geos = c.Geometry[options]
        for g in geos:
            geoI = g.GetInstanceGeometry()
            for a in geoI:
                pointList.append(a.GetEndPoint(0))
                #pointList.append(a.GetEndPoint(1))
    #print (pointList[0])
    pointListL = []

    for e in pointList:

        if e.ToString() not in pointListL.ToString():
            pointListL.append(e)


    t = Transaction(doc)
    t.Start( "Place Elements")
    listAnno = []
    for a in pointListL:
        for e in eleCol:
            eleTypeId = e.GetTypeId()
            if "Coordinate-Point_Site" in e.FamilyName:
                
                if not e.IsActive:
                    e.Activate()
                ele = doc.Create.NewFamilyInstance(a, e, doc.ActiveView)
                listAnno.append(ele)
                
    t.Commit()
    listEle = List[Element]()
    for n in listAnno:
        listEle.Add(doc.GetElement(n.Id))



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

    t.Start("Set Parameters")
    if len(listEle) >= 1:
        for ele in listEle:
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
        Alert('Have no Property Line in Current View. Please Retry', title="Alert", header="Notification:")
    t.Commit()
except:
    TaskDialog.Show("Notification", "Cancelled")