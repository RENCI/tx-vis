import json
import os
import re
import sys
from oslash import Left, Right
from .clinical_feature import mapping
from tx.functional.utils import monad_utils, case, identity

m = monad_utils(Right)

sequence = m.sequence

def add_status_code(v):
    if type(v) is tuple:
        return v
    else:
        return v, 500


def add_variable(v):
    def add_variable_to_value(val):
        return {**val, "patientVariableType": v}
    return add_variable_to_value
    

# Function that returns patient's demographic and clinical feature data
def lookupClinicalsFromData(patient_id, timestamp, clinical_feature_variables_and_data):
    clinical_feature_variables = clinical_feature_variables_and_data["patientVariables"]
    data = clinical_feature_variables_and_data["data"]
    
    mapper = sequence(map(lambda x: lookupClinicalFromRecord(patient_id, data, x, timestamp), clinical_feature_variables))
    return case(mapper)(add_status_code)(identity)


def lookupClinicalFromRecord(patient_id, data, v, timestamp):
    clinical = v["clinicalFeatureVariable"]
    unit = v.get("units")
    filter_data, feature, unit2 = mapping.get(clinical)
    if unit is None:
        unit = unit2
    if feature is None:
        return Left((f"cannot find mapping for {clinical}", 400))
    else:
        return filter_data(patient_id, data).bind(lambda records: feature(records, unit, timestamp)).map(add_variable(v))
    

