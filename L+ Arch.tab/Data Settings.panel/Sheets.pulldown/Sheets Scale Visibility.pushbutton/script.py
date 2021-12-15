__doc__ = 'Python for revit api'
__author__ = 'L+ Arch'
from Autodesk.Revit.DB import Transaction, FilteredElementCollector,BuiltInCategory,TransactionGroup
from Autodesk.Revit.UI import UIDocument, Selection

uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document

titleblock_col = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_TitleBlocks).WhereElementIsNotElementType().ToElements()

tg = TransactionGroup(doc, "Sheets Scale Setting")
tg.Start()
t1 = Transaction(doc, "Scale Text Setting")
t1.Start()
for tb in titleblock_col:
    param = tb.LookupParameter("Scale")
    paramVisibility = tb.LookupParameter("Scale Visibility")
    viewSheetId = tb.OwnerViewId
    viewSheet = doc.GetElement(viewSheetId)
    paramText = viewSheet.LookupParameter("Scale Text")
    allViewsport = viewSheet.GetAllViewports()
    if allViewsport:
        firstViewportId = allViewsport[0]
        firstViewport = doc.GetElement(firstViewportId)
        viewId = firstViewport.ViewId
        firstView = doc.GetElement(viewId)
        scale = firstView.Scale
        if paramText != None:
            paramText.Set("1 : " + str(scale))

t1.Commit()
        
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
tg.Assimilate()