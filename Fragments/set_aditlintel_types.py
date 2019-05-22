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

clr.AddReference('DSCoreNodes')
import DSCore
#from DSCore import *


class Lintel:
	""" Represent lintel family instance data"""
	count_in_project = 1
	
	def __init__(self, lintelInstance):
		self.lintelInstance = lintelInstance
		self.mark = lintelInstance.LookupParameter('FAM_Mark').AsString()
		
	def __convert_value_to_boolean(self, parameter_name):
		value = self.lintelInstance.LookupParameter(parameter_name).AsString()
		if value.lower() == 'true':
			return True
		return False
		
	def length(self):
		return self.lintelInstance.LookupParameter('LIN_Length').AsDouble()
		
	def width(self):
		return self.lintelInstance.LookupParameter('LIN_CoreBoundaryWidth').AsDouble()
		
	def is_supportbracket_oneside(self):
		return self.__convert_value_to_boolean('LIN_SupportBracket_OneSide')
		
	def is_supportbracket_twosides(self):
		return self.__convert_value_to_boolean('LIN_SupportBracket_TwoSides')
		
	def set_count(self, n):
		self.count_in_project = n
		return self


# Globals	
doc = DocumentManager.Instance.CurrentDBDocument
uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application

# Find unique lintels
mRule = FilterStringRule(
	ParameterValueProvider(ElementId(BuiltInParameter.ALL_MODEL_MODEL)),
	FilterStringEquals(),
	"Lintel",
	True
	)
mFilter = ElementParameterFilter(mRule)

collector = (
	FilteredElementCollector(doc).
	OfCategory(BuiltInCategory.OST_GenericModel).
	OfClass(FamilyInstance).
	WherePasses(mFilter)
	)
 
lintels = [Lintel(l) for l in collector.ToElements()]
keys = [l.mark for l in lintels]
groups = DSCore.List.GroupByKey(lintels, keys)['groups']

unique_lintels = [group[0].set_count(len(group)) for group in groups if group[0].mark]

# Selected lintel Types
"""
"""

OUT = [l.lintelInstance for l in unique_lintels]
