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

This script searches for all the source (.c) and header (.h) files in the directory
path specified by you.   Then it open all these files and convert the spaces
to tab for proper code indentation.   The number of spaces can be set flexibly by the 
you.

'''


import os
import time
import shutil
import re

# inputfilepath = "/home/michael/esp/esp_idf_v420_projects/projects_for_Vince/vsc_idf420_sense_safe/main/"
inputfilepath = "/home/michael/esp/esp_idf_v420_projects/projects_for_Vince/vsc_project_dummy_test/main/"
tempfilename = "temp.txt"

def init_current_directory(pathname):
    # check the current directory
    print(f'Current Directory: {os.getcwd()}')

    # change to the project directory
    if os.path.exists(pathname):
        os.chdir(pathname)
    else:
        print(f"Can't change the directory.")    
    print(f'Current Directory: {os.getcwd()}')	        

def convert_spaces_to_tab(infilename, outfilename,num_of_spaces):
    print(f'Convert from  {num_of_spaces} spaces to tab')
    searchpattern = "( {" + str(num_of_spaces) + "})"
    # print(searchpattern)
    with open(infilename, "r") as file_in, \
        open (outfilename, "w") as file_out:
        content = file_in.readlines()
        lineno = 1  # line number
        prevmlen = 0 # previous # of matched found.
        for line in content:
            # if lineno == 200:
            #     print(lineno)
            count = 0 # count how many substitues need to be made.
            matchlist = re.findall( searchpattern,line)  # Return all non-overlapping matches of pattern in string, as a list of strings.      
            curmlen = len(matchlist)
            if (curmlen > 0):
                match1stcode = re.search(r'\S',line)  # Search for the non space char
                if (match1stcode != None):
                    matchit = re.finditer( searchpattern,line)  # Return all non-overlapping matches of pattern in string, as a list of strings.                          
                    for element in matchit:
                        if (element.span(0)[0] < match1stcode.span(0)[0]):  # Is it before the first non-space char?
                            count += 1  
                if count > 0:
                    new_line = re.sub( searchpattern,'\t',line,count)    # specify how many substitutes to be made.        
                else:
                    new_line = line
            else:
                new_line = line
            file_out.write(new_line)
            prevmlen = curmlen          
            lineno += 1



# Main Code

# Initialization
init_current_directory(inputfilepath)

# Process all the source and header files.
for fname in os.scandir():
    if fname.is_file():
        match = re.search("\.[hc]$",fname.name)  # only .h or .c extension
        # print(match)
        if match != None:
            print(f'Processing {fname.name}')
            convert_spaces_to_tab(fname.name, tempfilename, 4)            
            shutil.copy(tempfilename,fname.name)
            


