#!/usr/bin/env bash
suricata_filepath="$1"
output_path="$2"

#merge first
cat ${suricata_filepath}/*.txt > ${suricata_filepath}/merged
mkdir -p ${output_path}
java -cp plugins/parsers/suricata SuricataToJSON ${suricata_filepath}/merged ${output_path}
rm ${suricata_filepath}/merged > /dev/null 2>&1
