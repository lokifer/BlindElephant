
#releases from http://download.moodle.org/stableXX/ where XX is > 13 and useful XX > 15

cd downloads

for i in *.zip; 
do
  if [ ! -d ../`basename $i .zip` ]
  then
    echo "Unpacking $i"
    unzip -q $i
    mv moodle ../`basename $i .zip`
  fi
done

cd ..