import sys
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

doc = DocumentManager.Instance.CurrentDBDocument
fec = FilteredElementCollector(doc).OfClass(IndependentTag)
OUT = fec.ToElements()
