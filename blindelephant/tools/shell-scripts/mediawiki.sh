#mediawiki
#http://download.wikimedia.org/mediawiki/

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