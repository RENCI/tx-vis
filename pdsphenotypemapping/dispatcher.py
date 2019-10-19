import json
import os
import re
from .clinical_feature import mapping


# Function that returns patient's demographic and clinical feature data
def lookupClinical(patient_id, clinical, timestamp):
    if clinical in mapping:
        return mapping[clinical](patient_id, timestamp)
    else:
        return 405, "invalid input"
    
