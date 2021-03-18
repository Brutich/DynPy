import clr
clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager

clr.AddReference("RevitAPI")
clr.AddReference("RevitAPIUI")
import Autodesk
from Autodesk.Revit.UI import *
from Autodesk.Revit.DB import *

from System.Collections.Generic import *

# Import ToDSType(bool) extension method
clr.AddReference('RevitNodes')
import Revit
clr.ImportExtensions(Revit.Elements)


uidoc = DocumentManager.Instance.CurrentUIDocument
ids = uidoc.Selection.GetElementIds()
elements = [uidoc.Document.GetElement(id).ToDSType(True) for id in ids]


OUT = elements
