#!/usr/bin/env bash

suricata_filepath="$1"
output_path="$2"

echo $suricata_filepath
echo $output_path

mkdir -p ${output_path}
java -cp plugins/parsers/suricata SuricataToJSON ${suricata_filepath}/fast.log ${output_path}
