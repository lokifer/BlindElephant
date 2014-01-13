
#releases from http://mirror.phil-taylor.com/ and Joomla.org

cd downloads

for i in *.zip; 
do
  if [ ! -d ../`basename $i .zip` ]
  then
    echo "Unpacking $i"
    unzip -q $i -d ../`basename $i .zip`; 
  fi
done

cd ..