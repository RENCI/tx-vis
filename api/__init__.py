import pdsphenotypemapping.dispatcher
import os

def mappingClinicalFromData(patient_id, timestamp, body):
    return pdsphenotypemapping.dispatcher.lookupClinicalsFromData(patient_id, timestamp, body)


