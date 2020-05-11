#Program for extracting all items of a file and putting in a folder called output.
import tarfile as tf
import os
def extract_tar(name):
    print("Extracting Started of {}".format(name))
    a = tf.open(name)
    output_name = "./Output/extracted" + os.path.splitext(name)[0]
    a.extractall(output_name)
    a.close()
    print("Extracting Finished")

print("imported extract_modules_successfully")