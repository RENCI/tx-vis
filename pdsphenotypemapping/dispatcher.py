import json
import os
import re
from .clinical_feature import mapping


# Function that returns patient's demographic and clinical feature data
def lookupClinical(patient_id, clinical, timestamp, data_provider_plugin_interface):
    if clinical in mapping:
        return mapping[clinical](patient_id, timestamp, data_provider_plugin_interface)
    else:
        return "invalid input", 405
    
