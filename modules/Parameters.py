import adsk.core
import adsk.fusion
import adsk.cam

_app = adsk.core.Application.get()


def get_parameters_data(identifiers=None):
    pData = []
    parameters = []

    if (identifiers):
        for parameterName in identifiers:
            parameters.append(get_parameters([parameterName]))
    else:
        parameters = get_parameters()

    if (parameters):
        for parameter in parameters:
            pData.append(
                {
                    "name": parameter.name,
                    "expression": parameter.expression,
                    "value": parameter.value,
                    "unit": parameter.unit,
                    "comment": parameter.comment,
                    "attribute-group": get_parameter_attribute_value(parameter, "group", "group")
                }
            )

    return pData


def get_parameters(identifiers=None):
    parameters = []
    design = _app.activeProduct

    if (identifiers):
        for parameterName in identifiers:
            parameters.append(design.userParameters.itemByName(parameterName))
    else:
        parameters = design.userParameters

    if len(parameters) == 1:
        returnVal = parameters[0]
    elif len(parameters) == 0:
        returnVal = None
    else:
        returnVal = parameters

    return returnVal


def get_parameter_attribute(parameter, attrGroup, attrName):
    return parameter.attributes.itemByName(attrGroup, attrName)


def get_parameter_attribute_value(parameter, attrGroup, attrName):
    returnVal = None
    attr = get_parameter_attribute(parameter, attrGroup, attrName)

    if attr:
        returnVal = attr.value

    return returnVal


def set_parameter_attribute(parameter, attrGroup, attrName, attrValue):
    parameterAttr = get_parameter_attribute(parameter, attrGroup, attrName)

    if parameterAttr:
        parameterAttr.value = attrValue
    else:
        parameter.attributes.add(attrGroup, attrName, attrValue)


def set_parameters(parameterList):
    returnVal = "success"
    try:
        for pData in parameterList:
            parameter = get_parameters([pData['name']])

            if pData['field'].find('attribute-') == -1:
                setattr(parameter, pData['field'], pData['value'])
            else:
                attrInfo = pData['field'].split('-')[1]
                set_parameter_attribute(parameter, attrInfo, attrInfo, pData['value'])
    except:
        returnVal = "error"
    finally:
        return returnVal
