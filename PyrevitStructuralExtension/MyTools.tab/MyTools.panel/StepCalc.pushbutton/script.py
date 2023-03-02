from pyrevit import revit, DB

doc = __revit__.ActiveUIDocument.Document

def get_parameter_value_by_name(element, parameterName):
	return element.LookupParameter(parameterName).AsValueString()

selection = revit.get_selection()

slaba_ssl = float(get_parameter_value_by_name(selection[0],"Elevation at Top"))
slaba_thk = float(get_parameter_value_by_name(selection[0],"Thickness"))
slabb_ssl = float(get_parameter_value_by_name(selection[1],"Elevation at Top"))
slabb_thk = float(get_parameter_value_by_name(selection[1],"Thickness"))

if slaba_ssl > slabb_ssl:
	overalldepth = slaba_ssl - slabb_ssl + slabb_thk
	totopsoffit = overalldepth - slaba_thk
	totoplower = slaba_ssl - slabb_ssl
else:
	overalldepth = slabb_ssl - slaba_ssl + slaba_thk
	totopsoffit = overalldepth - slabb_thk
	totoplower = slabb_ssl - slaba_ssl

print('{0}{1:>5.0f}'.format('Overall Depth:',overalldepth))
print('{0}{1:>5.0f}'.format('To Top Soffit:',totopsoffit))
print('{0}{1:>5.0f}'.format('To Top Lower:',totoplower))