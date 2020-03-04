[![Build Status](https://travis-ci.com/RENCI/tx-vis.svg?branch=master)](https://travis-ci.com/RENCI/tx-vis)

# tx-vis convenience plugin

### What does this plug-in do?

It creates desired [vega-lite](https://vega.github.io/vega-lite/) specs for visualization on PDS dashboard. 
Currently, it is used by guidance plugin to create desired 
visualization on the dashboard, but is general enough to be used 
by any other PDS plugin as needed. 

### build docker image

```
docker build . -t <image>
```

### run docker image

example `docker-compose.yml`

`PDS_PORT`: pds backend port

`PDS_HOST`: pds backend host

`PDS_VERSION`: pds backend version

### run test

```
test/test.sh
```
