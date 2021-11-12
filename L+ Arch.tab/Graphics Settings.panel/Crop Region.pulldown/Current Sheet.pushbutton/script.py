__doc__ = 'Python for revit api'
__author__ = 'L+ Arch'
from Autodesk.Revit.DB import Transaction,TransactionGroup, FilteredElementCollector, BuiltInCategory, ViewSheet, Color, OverrideGraphicSettings,LinePatternElement
from Autodesk.Revit.UI import TaskDialog
import random
from rpw.ui.forms import FlexForm, Label, Separator, Button, TextBox,ComboBox, Alert
from rpw import ui
from pyrevit import forms
import math

# Get UIDocument
uidoc = __revit__.ActiveUIDocument

# Get Document 
doc = uidoc.Document

linepat_col = FilteredElementCollector(doc).OfClass(LinePatternElement)
viewsheet_col = FilteredElementCollector(doc).OfClass(ViewSheet)
view_col = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Views).WhereElementIsNotElementType().ToElements()
viewport_col = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Viewports).WhereElementIsNotElementType().ToElements()
#boundary = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_CropBoundary).WhereElementIsNotElementType().ToElements()
#for bound in boundary:
    #print(bound.Id)

# Create Form for select line pattern
def id_sym(ele):
    ele_typeId = ele.GetTypeId()
    return ele_typeId.ToString()

lkey_name = set(map(id_sym,linepat_col))
dicta = {}
linepat = None

for key_id in lkey_name:
    dicta[key_id] = [ele.Name for ele in linepat_col if ele.GetTypeId().ToString() == key_id]
    components = [Label('Line Pattern:'),
            ComboBox('combobox0', dicta[key_id], default = "AR_Dash_6-3mm"),
            Label('Line Weight:'),
            ComboBox('combobox1', {'1':1,'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9}, default = '4'),
            Separator(),
            Button('Select')]
form = FlexForm('Override Graphics Settings', components)
form.show()
result = form.values
linecolor = Color(0,0,0)
if result:
    color = forms.ask_for_color()
    
    if color:
        def hex_to_rgb(value):
            value = value.lstrip('#')
            lv = len(value)
            return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))
        joined_string = "-".join(map(str,hex_to_rgb(color)))
        # Split color number
        color_split = joined_string.split("-")
        linecolor = Color(int(color_split[1]), int(color_split[2]), int(color_split[3]))
    linepattern = result['combobox0']
    # take override information
    for a in linepat_col:
        if a.Name == linepattern:
            linepatId = a.Id
            
    linewei = int(result['combobox1'])



gSettings = OverrideGraphicSettings()
activeview = doc.ActiveView
# select sheet with sheet number key
viewsheet_select = []
for viewsheet in viewsheet_col:
    if viewsheet.Id == activeview.Id:
        viewsheet_select.append(viewsheet)

viewsheetid =  [viewsheet.Id for viewsheet in viewsheet_select]
#print(viewsheetid)

for viewport in viewport_col:
#    print(viewport.OwnerViewId)
    #for a in viewsheet_select:
        if viewport.OwnerViewId in viewsheetid:
            viewid = viewport.ViewId
            view = doc.GetElement(viewid)
            viewtypeid = view.GetTypeId()
            viewtype = doc.GetElement(viewtypeid)
            viewFamilyName = viewtype.FamilyName.ToString()
            if viewFamilyName != "Drafting View":
                tGroup = TransactionGroup(doc, "Temp to find crop box element")
                tGroup.Start()
                t1 = Transaction(doc,"Select CropBoundary")
                t1.Start()
                view.CropBoxVisible = False
                t1.Commit()
            
                shownElems = FilteredElementCollector(doc, view.Id).ToElementIds()
                t1.Start()
                view.CropBoxVisible = True
                t1.Commit()
                cropBoxElement = FilteredElementCollector(doc, view.Id).Excluding(shownElems).FirstElement()
                tGroup.RollBack()
                if cropBoxElement != None:
                    cropid = cropBoxElement.Id
                    t = Transaction(doc, "Override Graphic Settings")
                    t.Start()
                    view.SetElementOverrides(cropid,gSettings.SetProjectionLinePatternId(linepatId))
                    view.SetElementOverrides(cropid,gSettings.SetProjectionLineWeight(linewei))
                    view.SetElementOverrides(cropid,gSettings.SetProjectionLineColor(linecolor))
                    t.Commit()






