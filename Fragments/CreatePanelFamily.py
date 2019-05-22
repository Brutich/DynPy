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

uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application

templateName = 'Metric Detail Item'
famTemplatePath = app.FamilyTemplatePath
templateFullName = r'C:\ProgramData\Autodesk\RVT 2019\Family Templates\English\Metric Detail Item.rft' # Path.Combine(famTemplatePath, templateName + ".rft")

famDoc = app.NewFamilyDocument(templateFullName)

saveOpt = SaveAsOptions()
saveOpt.OverwriteExistingFile = True

famDoc.SaveAs(r'D:\TEMP\00_Test\test.rfa', saveOpt)

OUT = famDoc
