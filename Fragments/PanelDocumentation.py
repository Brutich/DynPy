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


"""
My Exeption
"""
class PanelError(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
 		return repr(self.value)

def Error(message):
	messagePop = TaskDialog("Panels")
	messagePop.MainContent = message
	messagePop.Show()
	raise PanelError(message)
	
	
"""
Geting and grouping elements on the viewSheet
"""	

class ReferenceSheetData:
	def __init__(self, viewSheet, s):
		
		doc = viewSheet.Document
		
		referenceSheet = viewSheet
    	
    	# Prepare sheet
		guideGridParam = referenceSheet.get_Parameter(BuiltInParameter.SHEET_GUIDE_GRID)
		if guideGridParam.AsElementId() != ElementId.InvalidElementId:
			guideGridParam.Set(ElementId.InvalidElementId)
			doc.Regenerate()
		
		viewports = referenceSheet.GetAllViewports()
		elementsOnReferenceSheetFilter = FilteredElementCollector(doc, referenceSheet.Id)
		allElements = elementsOnReferenceSheetFilter.ToElements()
		
		mainLegendViewport = []
		sourceViewports = []
		sourceScheduleInstances = []
		sourceOtherElems = []
		for elem in allElements:
			if elem.Category.Name == 'Viewports':
				if legendNameCont in elem.get_Parameter(BuiltInParameter.VIEWPORT_VIEW_NAME).AsString():
					mainLegendViewport.append(elem)
				else:
					sourceViewports.append(elem)
			elif elem.Category.Name == "Schedule Graphics":
				sourceScheduleInstances.append(elem)
			else:
				sourceOtherElems.append(elem)
		
		if mainLegendViewport:
			mainLegendViewport = mainLegendViewport[0]
		else:
			Error("Чертеж панели на листе не найден")


		self.mainLegendViewport = mainLegendViewport
		self.sourceViewports = sourceViewports
		self.sourceScheduleInstances = sourceScheduleInstances
		self.sourceOtherElems = sourceOtherElems
		
		self.Source = referenceSheet
		self.suffix = s


"""
Check Input Data
"""
def CheckInputData(document, mainLegendViewport):
	stop = False
	listOfFamilyTypeMarks = [pt.GetParameters("FAM_Mark")[0].AsString() for pt in panelTypes]
	sourceViewLegend = document.GetElement(mainLegendViewport.ViewId)
	elementsOnSourcelegend = FilteredElementCollector(document, sourceViewLegend.Id).ToElements()
	for elem in elementsOnSourcelegend:
		mark = ''
		try:
			familyType = document.GetElement(elem.GetTypeId())
			mark = familyType.GetParameters("FAM_Mark")[0].AsString()
		except Exception:
			pass

		if mark in listOfFamilyTypeMarks:
			i = listOfFamilyTypeMarks.index(mark)
			famName = panelTypes[i].FamilyName
			if mark == '':
				Error("Значение параметра FAM_Mark семейства {f} отсутствует.".format(
					f = famName))	
			Error("Значение параметра FAM_Mark семейства {f} совпадает со значением у типа на опорном листе.".format(
				f = famName))
		elif len(set(listOfFamilyTypeMarks)) != len(listOfFamilyTypeMarks):	# Check duplicates
			Error("Значение свойства FAM_Mark\nдолжно быть уникально у всех выбранных Типов")
				
	return stop
	
	
"""
Schedules Copying
"""
def duplicateSchedule(panelMark, sourceScheduleInstance, suffix):

	scheduleId = sourceScheduleInstance.ScheduleId
	scheduleView = document.GetElement(scheduleId)
	newScheduleViewId = scheduleView.Duplicate(ViewDuplicateOption.Duplicate)
	newScheduleView = document.GetElement(newScheduleViewId)
	definition = newScheduleView.Definition
	filterModel = definition.GetFilter(0) 	# Family Model
	filterMark = definition.GetFilter(1)	# Panel Mark

	filterMark.SetValue(panelMark)
	definition.SetFilter(1, filterMark)
	
	if suffix != '':
		suffix = '_' + suffix
	name = '50_AmountOf{model}_{m}{s}'.format(
		model = filterModel.GetStringValue(),
		m = panelMark,
		s = suffix)
	newScheduleView.Name = name
	
	return newScheduleView
	
	
"""	
Copy legend on the sheet
"""
def copyLegendViewPort(toSheet, legendViewPort):
	newvport = Viewport.Create(
		document,
		toSheet.Id, legendViewPort.ViewId,
		legendViewPort.GetBoxCenter())
	return newvport	
	

"""
Creating Sheet by Panel Family type
"""
def SheetByPanelType(panelType, referenceSheetData):
	# Get parameters value
	try:
		panelMark = panelType.get_Parameter(System.Guid('ea138a7f-0852-464f-8d90-1bae4d29223d')).AsString()	#FAM_Mark
		panelIndex = panelType.get_Parameter(System.Guid('9c122fc4-b2c8-4a95-aabd-2fd003f22dd2')).AsString() #FAM_Index
	except Exception:
		Error("В семействе {f} отсутствует параметр FAM_Mark либо FAM_Index"
			.format(f = panelType.FamilyName))
		
	if (not panelMark) or (not panelIndex):
		Error('Упс! У панели {f} заполнены не все параметры'.format(f = panelType.FamilyName))
	
	# Create empty sheet
	newSheet = ViewSheet.Create(document, ElementId.InvalidElementId)
	
	# Set sheet parameters
	number = albumPart + '_' + panelMark
	suffix = referenceSheetData.suffix
	if suffix == '':
		name = 'Панель {i} ({m}). Раскладка кирпича со стороны фасада'.format(i = panelIndex, m = panelMark)
	else:
		name = 'Панель {i} ({m}). Раскладка кирпича в форме'.format(i = panelIndex, m = panelMark)
		number += '_а'
	
	newSheet.Name = name
	newSheetNumber = newSheet.get_Parameter(BuiltInParameter.SHEET_NUMBER)
	newSheetNumber.Set(number)
	
	infSort01 = newSheet.GetParameters("INF_Sort01")[0]
	infSort01.Set(albumPart)
	infVolume = newSheet.GetParameters("INF_Volume")[0]
	infVolume.Set(albumVolume)
	
	# Copy elements from source viewsheet to new viewsheet
	ids = List[ElementId]()
	[ids.Add(elem.Id) for elem in referenceSheetData.sourceOtherElems]
	copyPasteOptions = CopyPasteOptions()
	ElementTransformUtils.CopyElements(referenceSheetData.Source, ids, newSheet, None, copyPasteOptions)
	
	# Duplicate legend and place on new sheet
	soursLegendViewPort = referenceSheetData.mainLegendViewport
	sourceViewLegend = document.GetElement(soursLegendViewPort.ViewId)	
	viewLegendId = sourceViewLegend.Duplicate(ViewDuplicateOption.WithDetailing)
	
	# Rename view Legend
	if suffix != '':
		suffix = '_' + suffix
	document.GetElement(viewLegendId).Name = '50_AS_Panel_' + panelMark + suffix
	
	# Get all element IDs on legend
	elementsOnlegend = FilteredElementCollector(document, viewLegendId).ToElements()
	
	# Replace panel type 
	for elem in elementsOnlegend:
		try:
			familyType = document.GetElement(elem.GetTypeId())
			if familyType.get_Parameter(BuiltInParameter.ALL_MODEL_MODEL).AsString() == 'Panel':
				panel = elem
				panel.ChangeTypeId(panelType.Id)
				break
		except Exception:
			pass
			
	# Plase legend on the sheet
	newvport = Viewport.Create(
		document,
		newSheet.Id,
		viewLegendId,
		soursLegendViewPort.GetBoxCenter())
	
	# Schedules copying and placing on the new sheet
	for schedule in referenceSheetData.sourceScheduleInstances:
		newShedule = duplicateSchedule(panelMark, schedule, suffix)
		ScheduleSheetInstance.Create(document, newSheet.Id, newShedule.Id, schedule.Point)
		
	# Copy other legendViewports
	[copyLegendViewPort(newSheet, vp) for vp in referenceSheetData.sourceViewports]
		
	return newSheet
	

# Inputs
panelTypes = UnwrapElement(IN[2])
referenceSheetBackside = UnwrapElement(IN[1])
referenceSheetFace = UnwrapElement(IN[0])

legendNameCont = 'Панель' # Title on sheet must contains
document = referenceSheetFace.Document


# Checking the INF_Sort01 and INF_Volume property
def getSheetParameterValue(viewSheet, paramGuid):
	guid = System.Guid(paramGuid)
	sharedParam = SharedParameterElement.Lookup(document, guid)
	parameterName = sharedParam.Name
	try:
		paramValue = referenceSheetFace.get_Parameter(guid).AsString()
		if paramValue:
			pass
		else:
			paramValue = ""
		return paramValue
		
	except Exception:
		Error("У листов отсутствует параметр {pName}".format(pName = parameterName))


albumPart = getSheetParameterValue(referenceSheetFace, '36dea022-21ec-4277-a2b7-4b9769bf63f5') # INF_Sort01
albumVolume = getSheetParameterValue(referenceSheetFace, 'dad9deed-e60f-4a41-92f7-863b7ccdd3f7') # INF_Volume


TransactionManager.Instance.EnsureInTransaction(document)

dataSheetFace = ReferenceSheetData(referenceSheetFace, '')
dataSheetBackface = ReferenceSheetData(referenceSheetBackside, 'Backface')


# Checking inputs
isBadInputs = CheckInputData(document, dataSheetBackface.mainLegendViewport)
if (not isBadInputs):
	isBadInputs = CheckInputData(document, dataSheetFace.mainLegendViewport)


# Creating sheets
createdSheets = None
if (not isBadInputs):
	createdSheets = []
	for panelType in panelTypes:
		createdSheets.append(SheetByPanelType(panelType, dataSheetFace))
		createdSheets.append(SheetByPanelType(panelType, dataSheetBackface))
		
TransactionManager.Instance.TransactionTaskDone()

OUT = createdSheets
