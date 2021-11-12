"""Remove selected revisions from selected sheets."""
from Autodesk.Revit.DB import Transaction,FilteredElementCollector,BuiltInCategory,TransactionGroup
from pyrevit import revit, DB
from pyrevit import forms
from pyrevit import script

uidoc = __revit__.ActiveUIDocument
doc = uidoc.Document


logger = script.get_logger()


revisions = forms.select_revisions(button_name='Select Revision',
                                   multiple=True)

logger.debug(revisions)

if revisions:
    sheets = forms.select_sheets(button_name='Remove Revisions',
                                 include_placeholder=True)
    if sheets:
        with revit.Transaction('Remove Revision from Sheets'):
            updated_sheets = revit.update.update_sheet_revisions(revisions,
                                                                 sheets,
                                                                 state=False)
        if updated_sheets:
            print('SELECTED REVISION REMOVED FROM THESE SHEETS:')
            print('-' * 100)
            cloudedsheets = []
            for s in sheets:
                if s in updated_sheets:
                    revit.report.print_sheet(s)
                else:
                    cloudedsheets.append(s)
        else:
            cloudedsheets = sheets

        if len(cloudedsheets) > 0:
            print('\n\nSELECTED REVISION IS CLOUDED ON THESE SHEETS '
                  'AND CAN NOT BE REMOVED.')
            print('-' * 100)

            for s in cloudedsheets:
                revit.report.print_sheet(s)

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
                    param1.Set(0)
                elif r.SequenceNumber == 2:
                    param2.Set(0)
                elif r.SequenceNumber == 3:
                    param3.Set(0)
                elif r.SequenceNumber == 4:
                    param4.Set(0)
                elif r.SequenceNumber == 5:
                    param5.Set(0)
t.Commit()
tg.Assimilate()