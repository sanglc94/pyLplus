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

# Select Shared Parameter Group "Indentity Data" and Parameters // myExtDef = myGroup.Definitions.get_Item("Name of Parameter")
file = app.OpenSharedParameterFile()
if file:
    myGroups = file.Groups

    
    # create a dict Name of Groups, Shared Parameters
    dicta={}
    for a in myGroups:
        dicta[a.Name] = [b.Name for b in a.Definitions]


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


            # form select from list
            myExtDef = forms.SelectFromList.show(dicta, title = "Select Shared Parameters", multiselect=True, button_name='Select')
            if myExtDef != None:
                for b in dicta:
                    for a in myExtDef:
                        if a in dicta[b]:
                            groupName = b
                myGroup = myGroups.get_Item(groupName)
                if (myGroup != None):
                    ExtDef = myGroup.Definitions   
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
                            famDefName.append(f.Definition.Name)    # create a list of parameters available in the family 
                        trans = Transaction(docfamily, "Add Parameters")
                        trans.Start()
                        for e in ExtDef:
                            if e.Name in myExtDef and e.Name not in famDefName:

                            # Add Parameter
                                fp = familyManager.AddParameter(e,BuiltInParameterGroup.PG_DATA, False)
                            
                        # Reload Family
                        docfamily.LoadFamily(doc,FamilyOption())
                        
                        trans.Commit()
                    docfamily.Close(False)
    except:
        forms.alert('Cancelled')
else:
    forms.alert('Please open the shared parameter file before performing the operation!!!')