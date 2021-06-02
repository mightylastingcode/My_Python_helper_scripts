
'''
MIT License

Copyright (c) 2021 Michael Li

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

'''
'''
Author : Michael C. Li
Date : 06/02/2021
Code Language : Python 3.x
Python Modules : all built-in modules

This script searches for all the esp32 idf projects in the directory tree root
path specified by you.   Then it perform full clean to remove all the build files
to reduce the project size for archive.  It will archive the whole directory 
tree into a tar file.

'''


# Write a script to traverse the directory tree.

# run in Linux terminal.  Not within VSC terminal.



import os
import time
import shutil
import re

projectPathList = []
# The project directory
pathname = "/home/michael/esp/projects_esp420/examples"

# open the terminal for usb drive to get the drive name.
usb = '/media/michael/BE7B-62F8'  # hardcoded

STATUS_OK = 0
STATUS_BAD = -1

def init_current_directory():
    # check the current directory
    print(f'Current Directory: {os.getcwd()}')

    # change to the project directory
    if os.path.exists(pathname):
        os.chdir(pathname)
    else:
        print(f"Can't change the directory.")    
    print(f'Current Directory: {os.getcwd()}')

def init_idf_tool():
    cmd = '. $HOME/esp/esp-idf/export.sh'
    status = os.system(cmd)    
    print(f'status ({cmd}): {status}')
    if status != 0:
        exit(cmd + " returns an error code!")

    cmd = 'idf.py --version'
    status = os.system(cmd)    
    print(f'status ({cmd}): {status}')
    if status != 0:
        exit(cmd + " returns an error code!")

def send_idf_command(cmd):
    # do a full clean to reduce the project tranfer size
    # cmd = 'idf.py fullclean'
    status = os.system(cmd)    
    print(f'status ({cmd}): {status}')
    if status != 0:
        # exit(cmd + " returns an error code!")
        return STATUS_BAD
    else:
        return STATUS_OK


# traverse the keys.
def traverse_dirs_os(pathname,space):
    global projectPathList
    print(f"\nPath:{pathname}")
    # for name in os.scandir(pathname):
    #     if name.is_file():
    #         print(space + name.name)
    for name in os.scandir(pathname):            
        if name.is_dir():              
            list1 = os.listdir(pathname + "/" + name.name)     
            try:
                elementIndex = list1.index('main')
                print(space + name.name + "(project)") # project name.
                projectPathList.append(pathname + "/" + name.name)
            except ValueError:                
                # print(space + name.name) # project name.
                traverse_dirs_os(pathname + "/" + name.name, space + space)



init_current_directory()
init_idf_tool()

print()
print("====================================================")
print("List all the files/subdir recursively with os lib.")   
traverse_dirs_os(".", "    ")

print()
print("====================================================")
print("Change the path string")   

for i in range(len(projectPathList)):
    # print(projectPathList[i])
    projectPathList[i] = re.sub('\.',pathname, projectPathList[i])
    print(projectPathList[i])

print()
print("====================================================")
print("Perform project full clean to reduce the projec size for copy. ") 
for ppath in projectPathList:
    # print (ppath)
    os.chdir(ppath)
    print(f'Current Directory: {os.getcwd()}')
    # do a full clean to reduce the project tranfer size
    cmd = 'idf.py fullclean'
    if send_idf_command(cmd) == STATUS_BAD:
        print("Error! Unable to perform full clean on this project.")

# go back to initial root directory
init_current_directory()
print(os.listdir())

print(pathname)
# match = re.search('/\w$',pathname) # NONE case
# match = re.search('\w+$',pathname) # started
match = re.search('[\w-]+$',pathname) # get-started
# match = re.search('/[\w-]+$',pathname) # /get-started
print(match)
# print(match.group(0))
if match != None:
    archive_name = match.group(0)
    print(archive_name)
else:
    exit("re.search for directory name failed.")
   
print(shutil.make_archive(archive_name,'tar'))
# copy the tar file to the usb drive
cmd = "cp " + archive_name + ".tar " + usb
status = os.system(cmd)    
print(f'status ({cmd}): {status}')
if status != 0:
    exit(cmd + " returns an error code!")

print("End of Program!")