import json
import os
import re
from oslash import Left, Right
from .clinical_feature import mapping
import functools

append = lambda l: lambda a : l + [a]

pure = lambda a: Right(a)

fmap = lambda f: lambda a: pure(f) * a

liftA2 = lambda f: lambda a, b: fmap(f)(a) * b 

sequence = lambda ms: functools.reduce(liftA2(append), ms, Right([]))


# Function that returns patient's demographic and clinical feature data
def lookupClinicals(patient_id, timestamp, data_provider_plugin_id, clinical_feature_variables_and_units):
    mapper = sequence(map(lambda x: lookupClinical(patient_id, x["clinical_feature_variable"], x.get("unit"), timestamp, data_provider_plugin_id), clinical_feature_variables_and_units))
    if isinstance(mapper, Left):
        v = mapper.value
        if type(v) is tuple:
            return v
        else:
            return v, 500
    else:
        return mapper.value


def lookupClinical(patient_id, clinical, unit, timestamp, data_provider_plugin_id):
    feature = mapping.get(clinical)
    if feature is None:
        return Left((f"cannot find mapping for {clinical}", 405))
    else:
        return mapping[clinical](patient_id, unit, timestamp, data_provider_plugin_id)
    
