#!/bin/bash -c

echo "Building Biocypher Docker image"

cd /usr/app/
shopt -s extglob
cp -r /src/!(dump|quality_control) .
shopt -u extglob

# remove the output from previous runs
rm -rf /usr/app/data/build2neo

cp config/biocypher_docker_config.yaml config/biocypher_config.yaml
poetry install
python3 scripts/open_targets_biocypher_run.py
chmod -R 777 biocypher-log
