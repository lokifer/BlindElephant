#liferay
# get portal-x.x.x.war from sourceforge

cd downloads

for i in *.war; 
do
  if [ ! -d ../`basename $i .war` ]
  then
    echo "Unpacking $i"
    unzip -q $i html/* -d ../`basename $i .war`;
  fi
done

cd ..