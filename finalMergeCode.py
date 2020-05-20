import pandas as pd
import xlrd
import os
import shutil
import sys
from pandas import ExcelWriter
from pandas import ExcelFile

# When there are multiple files inside the required files(ex finace,sex etc), for those cases special merge will be called.
def special_merge(dirpath, dirnames, filenames, to_find):

    # to find the path of either to_find='domains' or 'urls'
    find_path = dirpath + "\\" + to_find

    # creating the file if it doesn't exists
    if(not(os.path.isfile(find_path))):
        # Creates a new file 
        with open(find_path, 'w') as fp: 
            pass
    else:
        # to avoid overwriting
        os.remove(find_path)
        # Creates a new file 
        with open(find_path, 'w') as fp: 
            pass

    # To fetch the domains(or urls) of all the folders and save it in one file
    for i in range(len(dirnames)):

        path = dirpath+"\\"+dirnames[i]+"\\" +to_find 

        if(os.path.isfile(path)):
            f = open(path)
            string_full=f.read()
            f.close()
        else:
            string_full=""

        with open(find_path, "a+") as file_object:
            # Append text at the end of file
            file_object.write(string_full)
    
    # return the path of newly created, merged file
    return find_path
    
# Fucntion to get the path of the given file (req_name) in main_dir
# to_find = domains or urls
def getFilePath(req_name, main_dir, to_find):

    dirName = "Output\\" + main_dir

    # to explore in the given directory name:
    for (dirpath, dirnames, filenames) in os.walk(dirName):
        if(req_name in dirnames):
            # to explore the particular folder of the directory
            for(dirpath, dirnames, filenames) in os.walk(dirpath+"\\"+req_name):
                if(len(dirnames)>0):
                    # run special_merge func for multiple files in the given folder 
                    return special_merge(dirpath, dirnames, filenames,to_find)
                elif(to_find in filenames):
                    # else simple return the path of domains or urls
                    return (dirpath+"\\" + to_find) 
                else:
                    return "invalid_path"


    
def merge_code(path1, path2, path3, output_name, code_01):

    # to check valid path
    if(os.path.isfile(path1)):
        f1 = open(path1)
        string1=f1.read()
        f1.close()
    else:
        string1=""
    if(os.path.isfile(path2)):
        f2 = open(path2)
        string2=f2.read()
        f2.close()
    else:
        string2=""
    if(os.path.isfile(path3)):
        f3 = open(path3)
        string3=f3.read()
        f3.close()
    else:
        string3=""
    
    # to extract the strins line wise and create a list
    string4=string1.splitlines()
    string5=string2.splitlines()
    string6=string3.splitlines()
    
    # Additional filter condition for urls
    if(code_01 == 1):
        result = ''
        for i in string4:
            result += ((i.split('/')[0])+'\n')
        string4 = result.splitlines()

        result = ''
        for i in string5:
            result += ((i.split('/')[0])+'\n')
        string5 = result.splitlines()

        result = ''
        for i in string6:
            result += ((i.split('/')[0])+'\n')
        string6 = result.splitlines()

    # push the string lists to sets
    set1 = set(string4)
    set2 = set(string5)
    set3 = set(string6)

    # Union of the above 3 sets
    set_after_merge = set1.union(set2)
    final_set=set3.union(set_after_merge)
    
    print("Merging files...")

    set1.clear()
    set2.clear()
    set3.clear()
    s = '\n'
    MYDIR = ("Result_domains")
    
    result_path = MYDIR + "\\" + output_name
    print("Saving... file to "+result_path)

    # Create a new directory with the name output_name
    with open(result_path, 'a+') as f:
        f.write(s.join(final_set))
        f.write('\n')
    


def main():

    dirName = "Output"
    
    df = pd.read_excel("Master-CF-Categories.xlsx", "Sheet1")
    # Column headings: Index(['Master Name', 'ShallaList', 'Capitole', 'MESD List'], dtype='object')

    MYDIR = ("Result_domains")
    CHECK_FOLDER = os.path.isdir(MYDIR)

    # If folder doesn't exist, then create it.
    if not CHECK_FOLDER:
        os.makedirs(MYDIR)
    else:
        # to avoid overwriting, delete the pre-existing folder
        shutil.rmtree(MYDIR)
        os.makedirs(MYDIR)

    # To iterate over the given excel sheet
    for i in df.index:
       
        output_name = ''
        extracted1_name = ''
        extracted2_name = ''
        extracted3_name = ''

        # to read valid data from excel sheet
        if(not(pd.isnull(df['Master Name'][i]))):
            output_name = df['Master Name'][i]
        if(not(pd.isnull(df['ShallaList'][i]))):
            extracted1_name = (df['ShallaList'][i])
        if(not(pd.isnull(df['Capitole'][i]))):
            extracted2_name = (df['Capitole'][i])
        if(not(pd.isnull(df['MESD List'][i]))):
            extracted3_name = (df['MESD List'][i])

        if(extracted1_name != ''):
            # To get the valid path using getFilePath function from extracted1\\BL
            path1 = getFilePath(extracted1_name, 'extracted1\\BL', 'domains')
            path1_urls = getFilePath(extracted1_name, 'extracted1\\BL', 'urls')
        else: 
            path1 = 'invalid_path1'
            path1_urls = 'invalid_path1'

        
        if(extracted2_name!=''):
            # To get the valid path using getFilePath function extracted2\\blacklists
            path2 = getFilePath(extracted2_name, 'extracted2\\blacklists', 'domains')
            path2_urls = getFilePath(extracted2_name, 'extracted2\\blacklists', 'urls')
        else:
            path2='invalid_path2'
            path2_urls='invalid_path2' 

        
        if(extracted3_name!=''):
            # To get the valid path using getFilePath function extracted3\\blacklists
            path3 = getFilePath(extracted3_name, 'extracted3\\blacklists','domains')
            path3_urls = getFilePath(extracted3_name, 'extracted3\\blacklists','urls')
        else:
            path3 = 'invalid_path3'
            path3_urls = 'invalid_path3' 

        # To run the merge_Code func for domains
        merge_code(path1, path2, path3, output_name, 0)

        # To run the merge_Code func for urls
        merge_code(path1_urls, path2_urls, path3_urls, output_name, 1)

        print("Saved file extracted1:" + extracted1_name +", extracted2:"+ extracted2_name+", extracted3:" +extracted3_name + " to Results/"+output_name)
        print('---------------------------------------------------------------')

    print("**************Successfully Completed Saving "+ str(len(df.index))+" files to Results folder! ****************************")

try:
    if __name__ == '__main__':
        main()

except:
    print("Main file not found!!! ->  404")