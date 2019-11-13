import json
import os
import re
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

# Function that returns patient's demographic and clinical feature data
def lookupClinicals(patient_id, timestamp, data_provider_plugin_id, clinical_feature_variables_and_units):
    mapper = sequence(map(lambda x: lookupClinical(patient_id, x["clinical_feature_variable"], x.get("unit"), timestamp, data_provider_plugin_id), clinical_feature_variables_and_units))
    return case(mapper)(add_status_code)(identity)


def lookupClinical(patient_id, clinical, unit, timestamp, data_provider_plugin_id):
    feature = mapping.get(clinical)
    if feature is None:
        return Left((f"cannot find mapping for {clinical}", 405))
    else:
        return mapping[clinical](patient_id, unit, timestamp, data_provider_plugin_id)
    
