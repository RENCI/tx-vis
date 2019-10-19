from dateutil.parser import *
from datetime import datetime, timezone


def strtots(st):
    return parse(st).timestamp()
    

def strtodate(st):
    return parse(st)


def tstostr(ts):
    dt = datetime.utcfromtimestamp(ts)
    dt2 = dt.replace(tzinfo=timezone.utc)
    return dt2.isoformat()
    

def bundle(records):
    return {
        "resourceType": "Bundle",
        "entry": list(map(lambda record: {
            "resource": record
        }, records))
    }


def unbundle(bundle):
    return list(map(lambda a : a["resource"], bundle.get("entry", [])))


