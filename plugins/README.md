# Suricata ECELD Integration
To integrate suricata with eceld copy the collectors/suricata files to the eceld-netsys/eceld/plugins directory. Copy the parsers/surciata files
to the same directory. Re-install eceld by going to the eceld-netsys/eceld directory and 
run the following command:

```
sudo ./install.sh
```

The suricata.rules file detects if a user accesses websites 
such as Facebook, Google, Youtube, Netflix, etc. Copy the suricata.rules file to the following directory:

```
/etc/suricata/rules/
```

The raw/suricata folder contains all the logs that suricata captured. 
The eve.json file shows all the alerts. You should now be able to run suricata from eceld. 

## Missing Items
- The suricata.JSON file is generated, but nothing is inside the file. 
- The suricata.lua file is missing. We need to first fix the bug where the suricata.JSON file does not contain any information.


