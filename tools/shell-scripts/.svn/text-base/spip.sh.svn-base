
#Releases from http://files.spip.org/spip/archives/
#releases before 1.9 have varying directory structures under the zip; post 1.9 seems consistent
cd downloads

#The unpacking logic here works only on releases after 1.9; everything before that should already exist and not be re-unpacked
for file in *.zip; 
do
  #Ugly regex that turns any of the various SPIP download file naming conventions into something we can recognize as a standard version number.
  newname=`echo $file | sed -e 's/\(SPIP-\)*\([vV]\)*\([[:alnum:].-]*\)\(.zip\)/\3/;y/-/./'`
  newname="spip_$newname"
  if [ ! -d ../$newname ]
  then
    echo "Unpacking $file as $newname"
    unzip -q $file
    mv spip ../$newname
  fi
done

cd ..



#NOTES BELOW

#unpacking logic for zips pre-1.7
#mkdir ../`basename $1 .zip`
#unzip $1 -d ../`basename $1 .zip`

#unpacking logic for zips 1.7 >= X < 1.9
#unzip $1 -d ..

#unpacking logic for zips 1.7 >= X < 1.9
#for i in SPIP-v1-8*; 
#do
#  if [ ! -d ../`basename $i .zip` ]
#  then
#    echo "Unpacking $i"
#    unzip -q $i -d ..
#  fi
#done

#logic for vers > 1.9
#for i in SPIP-v2*; 
#do
#  echo "Unpacking $i -> ../`basename $i .zip`"
#  unzip -q $i
#  mv spip ../`basename $i .zip`
#done


