#!/bin/bash

# clean up the repo
find -name "*.raw" ${DIR_PROJECT_ROOT}/submodules/simbricks/images | xargs rm
rm -rf ${DIR_PROJECT_ROOT}/experiments/simbricks/out

# build image
docker build --tag kaufijonas/nexdsim:sosp25_ae --file ${DIR_PROJECT_ROOT}/docker/Dockerfile ${DIR_PROJECT_ROOT}
