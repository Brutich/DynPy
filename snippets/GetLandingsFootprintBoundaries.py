import sys
import clr

# Import ToProtoType(bool) extension method
clr.AddReference("RevitNodes")
import Revit
clr.ImportExtensions(Revit.GeometryConversion)
clr.ImportExtensions(Revit.Elements)


def get_footprint(landing):
	return [x.ToProtoType(False) for x in landing.GetFootprintBoundary()]

landings = UnwrapElement(IN[0])

OUT = [get_footprint(l) for l in landings]
