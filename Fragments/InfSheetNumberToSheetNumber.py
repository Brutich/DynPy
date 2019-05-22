import clr
clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

clr.AddReference("RevitAPI")
clr.AddReference("RevitAPIUI")
import Autodesk
from Autodesk.Revit.UI import *
from Autodesk.Revit.DB import *

import System
from System.Collections.Generic import *

# Import ToDSType(bool) extension method
clr.AddReference("RevitNodes")
import Revit
clr.ImportExtensions(Revit.Elements)


document = DocumentManager.Instance.CurrentDBDocument
uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application


sheets = UnwrapElement(IN[0])

TransactionManager.Instance.EnsureInTransaction(document)
[s.get_Parameter(BuiltInParameter.SHEET_NUMBER).Set(s.LookupParameter('INF_SheetNumber').AsString()) for s in sheets]
TransactionManager.Instance.TransactionTaskDone()

OUT = 1
