#!/usr/bin/env python3
from hashlib import sha256
import os
import glob
import shutil

# Takes the path (as a string) to a SHA256SUMS file and a list of paths to
# local files. Returns true only if all files' checksums are present in the
# SHA256SUMS file and their checksums match
def integrity_is_ok(filename):
    print("checking integrity of :",filename)
    k = list()
    sha256_dict = dict()
    script_dir = os.path.split( os.path.realpath(__file__) )[0]
    sha256sums_file = script_dir + '/SHA256SUMS/sha256sums.csv'

    with open(sha256sums_file,'r') as f:
         lines = f.readlines()

    for i in lines:
         k = i.rstrip('\n').split(',')
         sha256_dict[k[0]] = k[1] 


    #Now get the sha256 value of the incoming file
    cksum = generateSHAValue(filename, dir='temp/')

    #Check if the previous sha256 value is the same   
    if sha256_dict[filename] == cksum:
        return True
    else:
        return False
         


def generateSHAValue(filename,dir):
    print("generating SHA256 value of :",filename)
    sha256sum = sha256()
    
    with open(dir+filename, 'rb' ) as fd:
            data_chunk = fd.read(1024)
            while data_chunk:
                sha256sum.update(data_chunk)
                data_chunk = fd.read(1024)

    checksum = sha256sum.hexdigest()
    
    return checksum

def write_sha256(filename):
    script_dir = os.path.split( os.path.realpath(__file__) )[0]
    sha256sums_file = script_dir + '/SHA256SUMS/sha256sums.csv'
    checksum = generateSHAValue(filename,dir='temp/')
    with open(sha256sums_file,'a+') as f:
       mystr = filename+","+checksum+"\n"
       f.write(mystr)  

    #then move the file from temp to images directory 
    shutil.move('temp/'+filename,'static/images/'+filename)

def check_image_exist(filename):
    image_dir = 'static/images/*.png'
    files = [os.path.basename(x) for x in glob.glob(image_dir)]

    if filename in files:
        return True
    else:
        return False

if __name__ == '__main__':

    script_dir = os.path.split( os.path.realpath(__file__) )[0]
    

    sha256sums_filepath = script_dir + '/SHA256SUMS'
    local_filepaths = [ script_dir + '/static/images' ]
    filename = 'abc.png'
    
    #write_sha256('int_hr.png')
    #print(integrity_is_ok('test.png'))
    
    #check if the file exists. If it does not exist then generate sha256 value and move to images dir
    if not check_image_exist(filename):
        print("i am False in check image")
        write_sha256(filename)
    else:
        #the file exists. Now check if the checksum matches. If not, then delete the old file
        #and move the new file from temp to images directory. Update with new checksum
        print("in else")
        if not integrity_is_ok(filename):
           write_sha256(filename)
        else: 
            #we can remove the file from temp
            os.remove('temp/'+filename)



