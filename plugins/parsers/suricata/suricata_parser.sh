#!/usr/bin/env bash

suricata_raw_dir="$1"
output_path="$2"

log_path="/var/log/suricata/"
dir="/home/kali/eceld/"

#echo "$log_path" "suricata_raw_dir"
cp -r "$log_path." "$suricata_raw_dir"
rm -r $log_path
mkdir $log_path
#cd $log_path
touch $log_path/fast.log
touch eve.json
touch stats.log
touch suricata.log

cd $dir

#merge first
cat ${suricata_raw_dir}/fast.log > ${suricata_raw_dir}/merged
mkdir -p ${suricata_raw_dir}
java -cp /home/kali/eceld-netsys/eceld/plugins/parsers/suricata SuricataToJSON ${suricata_raw_dir}/merged ${output_path}
rm ${suricata_raw_dir}/merged > /dev/null 2>&1

