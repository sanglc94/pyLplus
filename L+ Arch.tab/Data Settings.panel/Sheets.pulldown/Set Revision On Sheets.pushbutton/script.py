"""Set selected revisions on selected sheets."""
from Autodesk.Revit.DB import Transaction,FilteredElementCollector,BuiltInCategory,TransactionGroup
from pyrevit import revit, DB
from pyrevit import forms

uidoc = __revit__.ActiveUIDocument
doc = uidoc.Document

revisions = forms.select_revisions(button_name='Select Revision',
                                   multiple=True)

if revisions:
    sheets = forms.select_sheets(button_name='Set Revision',
                                 include_placeholder=True)
    if sheets:
        with revit.Transaction('Set Revision on Sheets'):
            updated_sheets = revit.update.update_sheet_revisions(revisions,
                                                                 sheets)
        if updated_sheets:
            print('SELECTED REVISION ADDED TO THESE SHEETS:')
            print('-' * 100)
            for s in updated_sheets:
                snum = s.Parameter[DB.BuiltInParameter.SHEET_NUMBER]\
                        .AsString().rjust(10)
                sname = s.Parameter[DB.BuiltInParameter.SHEET_NAME]\
                         .AsString().ljust(50)
                print('NUMBER: {0}   NAME:{1}'.format(snum, sname))


tg = TransactionGroup(doc, "Update Parameters")
tg.Start()
t = Transaction(doc, "Set Parameters")
t.Start()
if revisions:
    if sheets:
        for s in sheets:
            param1 = s.LookupParameter("Issue_01")
            param2 = s.LookupParameter("Issue_02")
            param3 = s.LookupParameter("Issue_03")
            param4 = s.LookupParameter("Issue_04")
            param5 = s.LookupParameter("Issue_05")
            for r in revisions:
                if r.SequenceNumber == 1:
                    param1.Set(1)
                elif r.SequenceNumber == 2:
                    param2.Set(1)
                elif r.SequenceNumber == 3:
                    param3.Set(1)
                elif r.SequenceNumber == 4:
                    param4.Set(1)
                elif r.SequenceNumber == 5:
                    param5.Set(1)
t.Commit()
tg.Assimilate()