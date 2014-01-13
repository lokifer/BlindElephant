#Drupal plugins

for pluginname in $(find * -maxdepth 0 -type d);
do
  cd $pluginname/downloads;
  for zipfile in *.tar.gz; 
  do 
    if [ ! -d ../`basename $zipfile .tar.gz` ]
    then
      echo "Unpacking drupal plugin $zipfile"
      tar -zxf $zipfile;
      rm -rf ../`basename $zipfile .tar.gz`
      mv $pluginname ../`basename $zipfile .tar.gz`;
    fi
  done;
  cd ../..;
done;