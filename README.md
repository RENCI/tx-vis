[![Build Status](https://travis-ci.com/RENCI/pdspi-mapper-example.svg?branch=master)](https://travis-ci.com/RENCI/pdspi-mapper-example)

# pds-phenotype-mapping-plugin

### What does this plug-in do?

Returns ALL patient variable values for a patient, assuming current time. Also returns how each variable was computed, what is the certainty of the computed value (certitude).
This is a POST and accepts the output JSON from https://github.com/RENCI/pds-config to get the units, and the FHIR output JSON from https://github.com/RENCI/pdspi-fhir-example to get the patient resource.

### build docker image

```
docker build . -t <image>
```

### run docker image

example `docker-compose.yml`

`PDS_PORT`: pds backend port

`PDS_HOST`: pds backend host


### run test

```
docker-compose -f docker-compose.yml -f test/docker-compose.yml -f test/pds-server/docker-compose.yml up --build -V --exit-code-from pdsphenotypemapping-test
```

### how to add new mapper

Steps to add new mapper:
1. Read the steps at the top of https://github.com/RENCI/pdspi-mapper-example/blob/master/pdsphenotypemapping/newfeature_addition.py
2. Follow the steps in the file above that shows addition of a new feature called 'oxygen_content' in order to understand the steps
3. Now, follow the same steps as above to add your own feature
4. Please remember to create a pull request including documentation for why you want the new feature(s) to be added (likely, because they are needed for a particular guidance plugin, so be sure to name the guidance plugin)

In the following, `any` is any json serializable type.

`pdsphenotypemapping/clinical_feature.py`

In the `mapping` dict, add your entry

Each entry is a triple of a function for retrieving data, a function for mapping data, and the default unit


The function for retrieving data should have the following signature:

```
str * # patient id
str -> # data provider plugin id 
Either any any # data for the function for mapping data
```

Utility functions for retrieving data

```
get_observation:
str * # patient_id
str -> # data provider plugin id
Either any [dict] # Left for error Right for no error. return an array of observation resources
```

```
get_condition:
str * # patient_id
str -> # data provider plugin id
Either any [dict] # Left for error Right for no error. return an array of condition resources
```

```
get_patient:
str * # patient_id
str -> # data provider plugin id
Either any dict # Left for error Right for no error. return an patient resource or None if patient doesn't exists
```

The function for mapping data should have the following signature:

```
any # data from the function for retrieving data
str * # unit to convert to, None if no unit or no conversion
str * # timestamp for getting the mapping
Either any dict # Left for error Right for no error. return a dict
```

Dict format:

```
{
  "value": <value>,
  "certitude": <certitude>, # 0 uncertain 1 somewhat certain 2 certain
  "calculation": <calculation> # string explanation
  "unit": <unit> # optional unit
  "timestamp": <timestamp>, # optional timestamp of the record in ISO 8601 format
}
```

The Either type is from the [OSlash](https://github.com/dbrattli/OSlash) library.

