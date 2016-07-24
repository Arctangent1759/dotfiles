#/bin/bash
for i in `ls | grep -v install.sh`; do
  $i/install.sh
done
