__doc__ = 'Python for revit api'
__author__ = 'L+ Arch'

from Autodesk.Revit.DB import Transaction, BuiltInParameterGroup,IFamilyLoadOptions,FamilySource,Element
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

# Create a IFamilyLoadOptions
class FamilyOption(IFamilyLoadOptions):
    def OnFamilyFound(self, familyInUse, overwriteParameterValues): 
        overwriteParameterValues = False
        return True
    def OnSharedFamilyFound(self, sharedFamily, familyInUse, source, overwriteParameterValues):
        source = FamilySource.Family
        overwriteParameterValues = False
        return True

# Main Code       
try:
    # Select Elements
    picks = uidoc.Selection.PickObjects(ObjectType.Element, CustomISelectionFilter('Autodesk.Revit.DB.FamilyInstance'), "Select Elements")
    if picks:
        listEle = List[Element]()
        famName = []
        for n in picks:
            nel = doc.GetElement(n.ElementId)   #get element
            nTypeId = nel.GetTypeId()           #get type ID
            nType = doc.GetElement(nTypeId)     #get element type
            nFamName = nType.FamilyName         #get family name

            # filter duplicate family name
            if nFamName not in famName:
                famName.append(nFamName)
                listEle.Add(nel)

        for el in listEle:
        # Get Family from Element
            fam = el.Symbol.Family

            # Edit Family 
            docfamily = doc.EditFamily(fam)
            if None != docfamily and docfamily.IsFamilyDocument == True:
                familyManager = docfamily.FamilyManager

                # filter definition (shared parameters) available in the family 
                famParam = familyManager.GetParameters()    # get family parameter
                famDefName = []
                for f in famParam:
                    if f.IsShared:
                        famDefName.append(f.Definition.Name)    # create a list of parameters available in the family 
                
                # Select Shared Parameters already added in this Family
                selectedDef = forms.SelectFromList.show(famDefName, title = "Select Parameters", multiselect=True, button_name='Select')

                trans = Transaction(docfamily, "Remove Parameters")
                trans.Start()
                if selectedDef:
                    for e in famParam:
                        if e.Definition.Name in selectedDef:

                            # Remove Parameters
                            familyManager.RemoveParameter(e)
                        
                    # Reload Family
                    docfamily.LoadFamily(doc,FamilyOption())
                
                trans.Commit()
            docfamily.Close(False)
except:
    forms.alert('Cancelled')