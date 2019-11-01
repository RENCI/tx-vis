import pdsphenotypemapping.dispatcher
import os

def mappingClinical(patient_id, clinical_feature_variable, timestamp, data_provider_plugin_id):
    return pdsphenotypemapping.dispatcher.lookupClinical(patient_id, clinical_feature_variable, timestamp, data_provider_plugin_id)


