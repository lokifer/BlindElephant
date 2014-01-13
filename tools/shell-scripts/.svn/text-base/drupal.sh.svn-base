#drupal
#http://ftp.drupal.org/files/projects/

cd downloads

for i in *.tar.gz; 
do 
  if [ ! -d ../`basename $i .tar.gz` ]
  then
    echo "Unpacking $i"
    tar -zxf $i;
    mv `basename $i .tar.gz` ..
  fi
done

cd ..