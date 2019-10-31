import json
import os
import re
from oslash import Left, Right
from .clinical_feature import mapping


# Function that returns patient's demographic and clinical feature data
def lookupClinical(patient_id, clinical, timestamp, data_provider_plugin_interface):
    if clinical in mapping:
        mapper = mapping[clinical](patient_id, timestamp, data_provider_plugin_interface)
        if isinstance(mapper, Left):
            return mapper.value, 500
        else:
            return mapper.value
    else:
        return "invalid input", 405
    
