#movabletype

cd downloads

for i in *.zip; 
do
  #movabletype has a bad habit of having different release names between the zipfile and the folder, so certain files will continue to be unpacked everytime
  #if it ever starts to take too long this can be revisited 
  if [ ! -d ../`basename $i .zip` ]
  then
    echo "Unpacking" $i
    unzip -nq "$i" -d ..;
  fi 
done

cd ..