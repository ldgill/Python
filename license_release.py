#!/usr/bin/env python3
import os
import re
import argparse
from pathlib import Path

# The main callback
def main():
    parser = argparse.ArgumentParser(description='Replaces Temporary License Files with the Official Kelvin License ')
    parser.add_argument('--source_dir', help='The directory to recursively start search from', default='../../')
    parser.add_argument('--license_file', help ='Official Kelvin License', default="KelvinLicense.txt")
    args = parser.parse_args()
    
    regex = '\s*[/][*][*]\s*(?:Auto-generated on [{] now [}][.]  Do NOT modify by hand, changes will be overwritten next time message are generated[.]\s* [*]\s*)?[*]\s*Some Kelvin specific source code header describing the use and what license\s*[*]*\s*it might be released under[.]\s*[*]*\s*[*][/]\s*'
    with open(args.license_file, "r") as license_file:
        license = license_file.read()
    
    exclude = ['build']
    includes = ['[.][.][/][.][.][/]kelvin[-]core[/]cpp[/]common[/]', '[.][.][/][.][.][/]kelvin[-]data[-]model[/]generated[/]']

    for dirpath, subdir, filenames in os.walk(args.source_dir):
        subdir[:] = [d for d in subdir if d not in exclude]
        for filename in filenames: 
            try:
                #print(os.path.join(dirpath, filename))
                filepath = os.path.join(dirpath, filename)
                with open(filepath, 'r', encoding='utf-8') as file:
                    data = file.read()
                    for i in includes:
                        if re.findall(i,filepath):
                            if filename.endswith(".h") or filename.endswith(".hpp"):
                                if not filename.endswith(".pb.h"):
                                    if not re.findall(regex, data):
                                        with open(filepath, 'w') as adding: 
                                                adding.write(license  + "\n\n" + data)
                                        print("ADDED LICENSE TO %s", filepath)
                    if re.findall(regex, data):
                        new_content = re.sub(regex, license + "\n\n", data)
                        with open(filepath, 'w') as modified:
                            modified.write(new_content)
                        print('MODIFIED %s' % filepath)

            except:
                pass
   
if __name__ == '__main__':
  main()