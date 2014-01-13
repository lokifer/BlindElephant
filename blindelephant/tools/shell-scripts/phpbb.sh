#phpbb

cd downloads

for i in phpbb*.zip; 
do 
  if [ ! -d ../`basename $i .zip` ]
  then
    echo "Unpacking $i"
    unzip -q $i -d `basename $i .zip`; 
    mv `basename $i .zip`/phpBB2/* `basename $i .zip`;
    mv `basename $i .zip` ..
  fi
done

for i in phpBB*.zip; 
  do
  if [ ! -d ../`basename $i .zip` ]
  then
    echo "Unpacking $i"
    unzip -q $i -d `basename $i .zip`; 
    mv `basename $i .zip`/phpBB3/* `basename $i .zip`;
    mv `basename $i .zip` ..  
  fi
done

cd ..