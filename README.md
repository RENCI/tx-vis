# pds-phenotype-mapping-plugin


### run test

#### manually

```
virtualenv -p python3 venv
source venc/bin/activate
```

```
cd test
PYTHONPATH=.. pytest
```

#### compose
```
docker-compuse -f docker-compose.yml -f test/docker-compose.yml up --build -V --exit-code-from pdsphenotypemapping-test
```