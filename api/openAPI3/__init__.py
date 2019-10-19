import pdsphenotypemapping.dispatcher
import os

def mappingClinical(patient_id, clinical_feature_variable, timestamp):
    return pdsphenotypemapping.dispatcher.lookupClinical(patient_id, clinical_feature_variable, timestamp)


