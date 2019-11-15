# pds-phenotype-mapping-plugin

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
`pdsphenotypemapping/clinical_feature.py`

in the `mapping` dict, add your entry

the function should have the following signature:

```
str * # patient_id 
str * # unit to convert to, None if no unit or no conversion
str * # timestamp for getting the mapping
str -> # data provider plugin id
Either dict dict # Left for error Right for no error. return a dict
```
dict format:
```
{
  "value": <value>,
  "code": <code> # optional FHIR CodeableConcept
  "quantity": <quantity>, # optional FHIR Quantity
  "certitude": <certitude>, # 0 uncertain 1 somewhat certain 2 certain
  "timestamp": <timestamp>, # optional timestamp of the record
  "calculation": <calculation> # string explanation
}
```



The Either type is from the [OSlash](https://github.com/dbrattli/OSlash) library.

utility functions:

```
get_observation:
str * # patient_id
str -> # data provider plugin id
Either dict [dict] # Left for error Right for no error. return an array of observation resources
```

```
get_condition:
str * # patient_id
str -> # data provider plugin id
Either dict [dict] # Left for error Right for no error. return an array of condition resources
```

```
get_patient:
str * # patient_id
str -> # data provider plugin id
Either dict dict # Left for error Right for no error. return an patient resource or None if patient doesn't exists
```
