#releases from http://sourceforge.net/projects/tep/files/

cd downloads

for i in *.zip; 
do
  if [ ! -d ../`basename $i .zip` ]
  then
    echo "Unpacking $i"
    unzip -q $i
    mv `basename $i .zip` ..
  fi
done

cd ..