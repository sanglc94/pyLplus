from Autodesk.Revit.DB import ExternalFileUtils, ModelPathUtils
from Autodesk.Revit.UI import Selection
from Autodesk.Revit.UI.Selection.Selection import PickObject 
from Autodesk.Revit.UI.Selection import ObjectType,ISelectionFilter
from pyrevit import forms, revit
import os


uidoc = __revit__.ActiveUIDocument
doc = uidoc.Document

# Create a ISelectionFilter
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
#Select Link CAD
    pick = uidoc.Selection.PickObject(ObjectType.Element, CustomISelectionFilter('Autodesk.Revit.DB.ImportInstance'), "Select one CAD Link")
    eleid = pick.ElementId
    el = doc.GetElement(eleid)
    #Choose File Path
    if el != None:
        cadLink = revit.doc.GetElement(el.GetTypeId())
        cadRef = ExternalFileUtils.GetExternalFileReference(revit.doc, cadLink.Id)
        fpath = ModelPathUtils.ConvertModelPathToUserVisiblePath(cadRef.GetAbsolutePath())
    else:
        forms.alert('One CAD link instance must be selected')

    # Open Link CAD
    os.startfile(fpath)
except:
    forms.alert('Cancelled')
