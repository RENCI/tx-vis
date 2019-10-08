import pdsphenotypemapping.dispatcher
import os

def low_level_mapping(body):
    return pdsphenotypemapping.dispatcher.lookupFHIR(os.path.join(os.environ["INPUT_ROOT"], body.get("input_dir", "")), body["patient_id"], body["codes"])

def mapping(body):
    return pdsphenotypemapping.dispatcher.lookupClicinal(os.path.join(os.environ["INPUT_ROOT"], body.get("input_dir", "")), body["patient_id"], body["clinical"])


