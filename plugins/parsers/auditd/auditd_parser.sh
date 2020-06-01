#!/usr/bin/env bash
auditd_filepath="$1"
output_path="$2"

#merge first
cat ${auditd_filepath}/*.txt > ${auditd_filepath}/merged
mkdir -p ${output_path}
java -cp plugins/parsers/auditd AuditdToJSON ${auditd_filepath}/merged ${output_path}
rm ${auditd_filepath}/merged > /dev/null 2>&1