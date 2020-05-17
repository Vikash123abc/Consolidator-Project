import pandas as pd
import xlrd
import os
import shutil
import sys
from pandas import ExcelWriter
from pandas import ExcelFile

def special_merge(dirpath, dirnames, filenames):

    domains_path = dirpath + "\domains"
    if(not(os.path.isfile(domains_path))):
        # Creates a new file 
        with open(domains_path, 'w') as fp: 
            pass
    else:
        os.remove(domains_path)
        # Creates a new file 
        with open(domains_path, 'w') as fp: 
            pass

    # result_string = ''
    for i in range(len(dirnames)):
        path = dirpath+"\\"+dirnames[i]+"\domains"

        if(os.path.isfile(path)):
            f10 = open(path)
            string10=f10.read()
            f10.close()
        else:
            string10=""

        # string11 = string10.splitlines()
        with open(domains_path, "a+") as file_object:
            # Append text at the end of file
            file_object.write(string10)
    
    return domains_path
    

def getFilePath(req_name, main_dir):

    # print("req_name is " + req_name)
    # print("main_dir is " + main_dir)

    dirName = "Output\\" + main_dir
    # dirName  = "Output"

    for (dirpath, dirnames, filenames) in os.walk(dirName):
        if(req_name in dirnames):
            for(dirpath, dirnames, filenames) in os.walk(dirpath+"\\"+req_name):
                # print((dirpath)) #string
                # print((dirnames)) # folder list
                # print((filenames)) # file list
                if(len(dirnames)>0):
                    return special_merge(dirpath, dirnames, filenames)
                elif('domains' in filenames):
                    # print("Domains found in \"" + req_name + "\" Directory in \""+ main_dir +"! at path: ")
                    # print(dirpath+"\domains----------------------------")
                    return (dirpath+"\domains") 


    
def merge_code(path1, path2, path3, output_name):
    
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
    
    string4=string1.splitlines()
    string5=string2.splitlines()
    string6=string3.splitlines()

    set1 = set(string4)
    set2 = set(string5)
    set3 = set(string6)

    set_after_merge = set1.union(set2)
    final_set=set3.union(set_after_merge)

    print("Merging files...")

    set1.clear()
    set2.clear()
    set3.clear()
    s = '\n '
    MYDIR = ("Result_domains")
    
    result_path = MYDIR + "\\" + output_name
    print("Saving... file to "+result_path)
    with open(result_path, 'a+') as f:
        f.write(s.join(final_set))

    


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
        shutil.rmtree(MYDIR)
        os.makedirs(MYDIR)

    for i in df.index:
       
        output_name = ''
        extracted1_name = ''
        extracted2_name = ''
        extracted3_name = ''

        if(not(pd.isnull(df['Master Name'][i]))):
            output_name = df['Master Name'][i]
        if(not(pd.isnull(df['ShallaList'][i]))):
            extracted1_name = (df['ShallaList'][i])
        if(not(pd.isnull(df['Capitole'][i]))):
            extracted2_name = (df['Capitole'][i])
        if(not(pd.isnull(df['MESD List'][i]))):
            extracted3_name = (df['MESD List'][i])

        if(extracted1_name != ''):
            path1 = getFilePath(extracted1_name, 'extracted1\\BL')
        else: 
            path1 = 'invalid_path1'
        
        if(extracted2_name!=''):
            path2 = getFilePath(extracted2_name, 'extracted2\\blacklists')
        else:
            path2='invalid_path2' 
        
        if(extracted3_name!=''):
            path3 = getFilePath(extracted3_name, 'extracted3\\blacklists')
        else:
            path3 = 'invalid_path3' 

        merge_code(path1, path2, path3, output_name)
        print("Saved file extracted1:" + extracted1_name +", extracted2:"+ extracted2_name+", extracted3:" +extracted3_name + " to Results/"+output_name)
        print('---------------------------------------------------------------')

    print("**************Successfully Completed Saving "+ str(len(df.index))+" files to Results folder! ****************************")


if __name__ == '__main__':
    main()