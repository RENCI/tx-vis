import pdsphenotypemapping.dispatcher
import os

def mappingClinical(patient_id, timestamp, data_provider_plugin_id, body):
    return pdsphenotypemapping.dispatcher.lookupClinicals(patient_id, timestamp, data_provider_plugin_id, body)

def mappingClinicalFromData(timestamp, body):
    return pdsphenotypemapping.dispatcher.lookupClinicalsFromData(timestamp, body)


