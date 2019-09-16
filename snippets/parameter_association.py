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



elements = UnwrapElement(IN[0])
fam_doc = DocumentManager.Instance.CurrentDBDocument #elem.Document


if fam_doc.IsFamilyDocument:

	# Apply association
	TransactionManager.Instance.EnsureInTransaction(fam_doc)
	
	try:
		fam_parameter = fam_doc.FamilyManager.get_Parameter("FAM_Mark")
		fam_yes_no_parameter = fam_doc.FamilyManager.get_Parameter("FAM_YesNo")
	
		for elem in elements:
		
			elem_parameter = elem.GetParameters("FAM_Mark")[0]
			fam_doc.FamilyManager.AssociateElementParameterToFamilyParameter(elem_parameter, fam_parameter)
			
			elem_parameter = elem.GetParameters("FAM_YesNo")[0]
			fam_doc.FamilyManager.AssociateElementParameterToFamilyParameter(elem_parameter, fam_yes_no_parameter)
			
			visibilityParam = elem.get_Parameter(BuiltInParameter.GEOM_VISIBILITY_PARAM)
			visibilityParam.Set(49152) # Coarse False
	except:
		pass
		
	TransactionManager.Instance.TransactionTaskDone()

OUT = elements
