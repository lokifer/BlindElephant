
#phpnuke
# from http://www.oldapps.com/PHP-Nuke.php

cd downloads

for i in *.zip; 
do 
  if [ ! -d ../`basename $i .zip` ]
  then
    echo unpacking $i
    unzip -q $i -d `basename $i .zip`; 
    cd `basename $i .zip`; 
    ls | grep -v html | xargs /bin/rm -rf; 
    mv html/* .; 
    rm -rf html; 
    cd ..;
    mv `basename $i .zip` ..
  fi
done

cd ..