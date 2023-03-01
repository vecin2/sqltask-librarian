#!/bin/bash

#This script documents differences found between oracle and sqlserver:

# Oracle's CURRENT_DATE can be enter as current_date, which is compatible also in sql server
grep -irl SYSDATE prj_config | xargs sed -i 's/SYSDATE/CURRENT_DATE/g'
grep -irl sysdate prj_config | xargs sed -i 's/sysdate/CURRENT_DATE/g'


