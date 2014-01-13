#wordpress

cd downloads

for i in *.zip; 
do
  #only if unpacked dir doesn't already exist
  if [ ! -d ../`basename $i .zip` ]
  then
    echo unpacking $i
    unzip -q $i -d `basename $i .zip`; 
    mv `basename $i .zip`/wordpress/* `basename $i .zip`;
    rm -rf `basename $i .zip`/wordpress
    mv `basename $i .zip` ..
  fi
done

cd ..