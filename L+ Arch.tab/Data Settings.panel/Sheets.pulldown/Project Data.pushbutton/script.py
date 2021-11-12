__doc__ = 'Python for revit api'
__author__ = 'L+ Arch'
from Autodesk.Revit.DB import (Transaction, FilteredElementCollector,BuiltInParameter, BuiltInCategory, Definition, Line, XYZ,
                                Element, View, ElementId, FamilyInstance, BasePoint, UnitUtils, DisplayUnitType, Transform,FamilySymbol,
                                FillPatternElement, Color, OverrideGraphicSettings, ViewSheet,TransactionGroup)
from Autodesk.Revit.UI import UIDocument, Selection,TaskDialog
from Autodesk.Revit.UI.Selection.Selection import PickObject 
from Autodesk.Revit.UI.Selection import ObjectType
import random
from rpw.ui.forms import FlexForm, Label, Separator, Button, Alert, TextBox

# Get UIDocument
uidoc = __revit__.ActiveUIDocument

# Get Document 
doc = uidoc.Document

from rpw.ui.forms import (FlexForm, Label, ComboBox, TextBox, TextBox,
                          Separator, Button, CheckBox)


components = [Label('Project Code:'),
            TextBox('textbox1'),
            Label('Project Stage:'),
            TextBox('textbox2'),
            Separator(),
            Button('Select'), 
            Button('Cancel')]
form = FlexForm('Project Data', components)
form.show()
result = form.values



sheets_collector=FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Sheets).WhereElementIsNotElementType().ToElements()
#titleblocks = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_TitleBlocks).WhereElementIsElementType().OfClass(FamilySymbol)
titleblocks = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_TitleBlocks).WhereElementIsNotElementType().ToElements()

tg = TransactionGroup(doc, "Update and Delete")
tg.Start()
t = Transaction(doc, "Set Parameters")
t.Start()
if result:
    for sheet in sheets_collector:
        project_code = sheet.LookupParameter("Project Code")
        project_stage = sheet.LookupParameter("Project Stage")
        project_code.Set(result['textbox1'])
        project_stage.Set(result['textbox2'])
        papersize = sheet.LookupParameter("Paper Size")
        
        for titleblock in titleblocks:
            if titleblock.OwnerViewId == sheet.Id:
                if "A0" in Element.Name.__get__(titleblock):
                    papersize.Set("A0")
                elif "A1" in Element.Name.__get__(titleblock):
                    papersize.Set("A1")
                elif "A2" in Element.Name.__get__(titleblock):
                    papersize.Set("A2")
                elif "A3" in Element.Name.__get__(titleblock):
                    papersize.Set("A3")
                elif "A4" in Element.Name.__get__(titleblock):
                    papersize.Set("A4")


t.Commit()
tg.Assimilate()

