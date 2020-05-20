
import requests
# function for downloading tar files.
def download_tar(url,name):
    print("Downloading Started")
    r = requests.get(url, allow_redirects=True)
    print("Successfully Downloaded")
    open(name, 'wb').write(r.content)


#Program for extracting all items of a file and putting in a folder called Output/extracted .
import tarfile as tf
import os

# function for extarcting files from all three zip files.. 
def extract_tar(name):
    print("Extracting Started of {}".format(name))
    a = tf.open(name)
    output_name = "./Output/extracted" + os.path.splitext(name)[0]
    a.extractall(output_name)
    a.close()
    print("Extracting Finished")




def main():

    download_tar("http://www.shallalist.de/Downloads/shallalist.tar.gz","1.tar")
    download_tar("http://dsi.ut-capitole.fr/blacklists/download/blacklists.tar.gz","2.tar")
    download_tar("http://squidguard.mesd.k12.or.us/blacklists.tgz","3.tar")
    extract_tar("1.tar")
    extract_tar("2.tar")
    extract_tar("3.tar")

#try and except for exception handling..    
try:
 if __name__ == '__main__':
    main()
except:
    print("An Erorr occured")