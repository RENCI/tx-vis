    

def bundle(records):
    return {
        "resourceType": "Bundle",
        "entry": list(map(lambda record: {
            "resource": record
        }, records))
    }


def unbundle(bundle):
    return list(map(lambda a : a["resource"], bundle.get("entry", [])))


