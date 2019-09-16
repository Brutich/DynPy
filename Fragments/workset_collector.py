import clr
clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import *
import Autodesk

clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager

doc = UnwrapElement(IN[0])
worksetTable = doc.GetWorksetTable()

ws_coll = FilteredWorksetCollector(doc)
ws_kindes = [ws.Kind for ws in ws_coll]
ws_names = [ws.Name for ws in ws_coll]
ws_ids = [ws.Id for ws in ws_coll]

OUT = ws_kindes, ws_names, ws_ids
