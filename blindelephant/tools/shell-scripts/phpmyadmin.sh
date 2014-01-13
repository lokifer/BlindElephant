
#phpmyadmin
#demo servers for testing: http://demo.phpmyadmin.net/

#Previously had problems with naming in historical versions. RELEASE_X_Y_Z instead of new phpMyAdmin-X.Y.Z.
#Looks like files going forward are well named. Strategy now is:
# - unpack all historical ones, account for their packing structure
# - rename all unpacked dirs according to new naming scheme
# - rename all old tar files according to new naming scheme; should be able convert unpacker script to new naming scheme at this point without trouble
# - Add new scripts and move forward
#
#Using rename to bring old files & dirs to new format:
# rename 'y/_/./' *.tar.gz
# rename 's/RELEASE./phpMyAdmin-/' *.tar.gz
#
#Completed successfully. 6/10/10

cd downloads
for file in *.tar.gz; 
do 
  if [ ! -d ../`basename $file .tar.gz` ]
  then
    echo unpacking `basename $file .tar.gz`
    tar -zxf $file;
    #move phpMyAdmin root dir up and rename it as version
    mv `basename $file .tar.gz` ..;
    #remove now-empty version folder in downloads dir
    rm -rf `basename $file .tar.gz`
  fi
done;


#JUST NOTES BELOW HERE

#Fetch historical versions via svn; Doesn't work; $Id$ vars aren't filled in. Need to check out using actualy VC tool
#-------------------------------
#http://phpmyadmin.svn.sourceforge.net/viewvc/phpmyadmin/tags/ 


#Fetch historical versions via git; doesn't work, same reason
#----------------------------------
#git clone git://phpmyadmin.git.sourceforge.net/gitroot/phpmyadmin/phpmyadmin -- also doesn't work, same problem
#for ver in `git tag -l`; 
#  do echo "$ver"
#done;
#
#for ver in `git tag -l`; 
#do 
#  git checkout -b $ver $ver
#done;
#
#to change to tag
#git checkout TAGNAME
