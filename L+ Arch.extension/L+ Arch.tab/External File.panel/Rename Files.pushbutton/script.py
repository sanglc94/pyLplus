from Autodesk.Revit.DB import Transaction,FilteredElementCollector,BuiltInCategory,TransactionGroup
from pyrevit import forms
from rpw.ui.forms import TextInput,SelectFromList
import os
from os import walk
import traceback


# ---------------------------
uidoc = __revit__.ActiveUIDocument
doc = uidoc.Document

allFile = []
filePath = forms.pick_folder(title="Select Folder", owner=None)

if filePath:
    try:
        #value = TextInput('Files Type (exp: .dwg, .pdf,...):', default=".pdf")
        value = SelectFromList('Files Type:', {'CAD' : ".dwg", 'PDF':".pdf"})

        allFile = os.listdir(filePath)
        
        for file in allFile:
            
            if value in file and "Sheet -" in file:

                currentFileName = filePath + "\\" + file
                #print(currentFileName)
                index = file.find("Sheet -")
                leng = len("Sheet -") + index
                newName =  ''.join([file[i] for i in range(len(file)) if i > leng]) 
                #print (newNames)
                    
                
        
                newFileName = filePath + "\\" + newName
                if newFileName != currentFileName:
                    os.rename(currentFileName, newFileName)
    except:
        errorReport = traceback.format_exc()

