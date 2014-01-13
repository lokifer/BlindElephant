#wordpress-plugins
#plugins at http://wordpress.org/extend/plugins/

#should be run from wordpress-plugins/
for pluginname in $(find * -maxdepth 0 -type d);
do
  cd $pluginname/downloads
  for i in *.zip; 
  do
    #only extract zip if corresponding folder doesn't exist
    if [ ! -d ../`basename $i .zip` ]
    then
      echo unpacking wordpress plugin $i
      unzip -q $i -d `basename $i .zip`;
      mv `basename $i .zip`/$pluginname/* `basename $i .zip`;
      rmdir `basename $i .zip`/$pluginname;
      mv `basename $i .zip` ..;
    fi
  done;
  cd ../..
done
