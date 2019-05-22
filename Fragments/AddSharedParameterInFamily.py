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


class FamilyOption(IFamilyLoadOptions):
	def OnFamilyFound(self, familyInUse, overwriteParameterValues):
		overwriteParameterValues = True
		return True
		
	def OnSharedFamilyFound(self, sharedFamily, familyInUse, FamilySource, overwriteParameterValues):
		overwriteParameterValues = True
		return True


def addParameter(fam, edef):
	
	docFamily = doc.EditFamily(fam)
	familyManager = docFamily.FamilyManager	
	

	
	TransactionManager.Instance.EnsureInTransaction(docFamily)
	try:
		familyManager.AddParameter(eDef, BuiltInParameterGroup.PG_IDENTITY_DATA, True)
	except:
		pass
	TransactionManager.Instance.TransactionTaskDone()
	
	#collector = FilteredElementCollector(docFamily).OfCategory(BuiltInCategory.OST_DetailComponents)
	#elements = collector.ToElements()
	
	docFamily.LoadFamily(doc, FamilyOption())
	#docFamily.Close()
	
	
	tr = Transaction(doc, "SubTransactionUses")
	tr.Start()	
	doc.Regenerate()
	
	tr.Commit()

	#docFamily.Close()	
	#doc.Regenerate()

	
	return True
	

family = UnwrapElement(IN[0])

doc = DocumentManager.Instance.CurrentDBDocument
uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application

defFile = app.OpenSharedParameterFile()
myGroups = defFile.Groups
myGroup = myGroups.get_Item("APEX_Families") # Parameters Group
myDefinitions = myGroup.Definitions
eDef = myDefinitions.get_Item("FAM_YesNo")# as ExternalDefinition


result = addParameter(family, eDef)


OUT = result
