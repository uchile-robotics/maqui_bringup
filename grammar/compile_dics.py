#!/usr/bin/env python
# -*- coding: utf-8 -*-
import qi
import os
import argparse
import sys
from os import listdir
from os.path import isfile, join
""""
- You can compile all the dics in a folder or specified just one.

How To Use:

python compile_dics.py 
    --path=[folder inside of /grammar that you want to copile] 
    --filename=[ name of the diccionary to compile (if is non specified it will compile all dics in the folder)] 
    --language=[Language]

- Example: 
    
    Compile the dictionary confirmation on the folder restaurant:
        
        python compile_dics.py --path=/restaurant --filename=confirmation.lcf

    Compile all dictionarys in folder restaurant
        
        python compile_dics.py --path=/restaurant 
-

"""
def compile_dics(session, path="", filename= "", language="English"):
    if path == "":
        return 

    path_root = "/home/nao/grammar"
    path = path_root + path

    speech = session.service("ALSpeechRecognition")

    files = listdir(path)

    if filename!="":
        if filename in files:
            filenames = [filename]
        else:
            print("Not {0} in  {1}!! \n Bye ".format(filename, path))
            return
    
    else:
        filenames = [f for f in files if isfile(join(path, f)) and f[-3:]=="bnf"]
    path = path+"/"
    # for file1 in filenames:
    print(" \n ### The following dictionarys will be compiled: \n")
    
    for _file in filenames:
        x = ""
        if _file[:-4]+".lcf" in files:
            x = "  (overwrite) !!!!!!"
        print(_file +  x +"\n" )

    a = raw_input("Compile? 1 (compile all) -- 2( no overwrite) -- 0 (no compile) ")
    
    a = int(a)
    if a == 1:

        compile_filenames = filenames

    elif a == 2:
        for _file in filenames:
            compile_filenames = []
            if not _file[:-4]+".lcf" in files:
                compile_filenames.append(_file)

    elif a==3:
        print "Ok, no dictionarys"
        return    
    
    else: 
        print "error input "
        return    

    print "Ok"
    
    for _file in compile_filenames:
        bnf = path + _file
        lcf = path + _file[:-4] + ".lcf"
        try:
            speech.compile(bnf,lcf,language)
            print(bnf + " [Compiled]")
        except Exception, e:
            print(bnf + " [Error]")
            print("Error compiling " + bnf)
            print(e)
            continue
    return



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", type=str, default="/basic/",
                        help="path to the bnf files")

    parser.add_argument("--filename", type=str, default="",
                        help="a specific bnf file contained in the path")


    parser.add_argument("--language", type=str, default="English",
                        help="Language of the dictionary")
    args = parser.parse_args()

    connection_url="tcp://" + os.environ["robot_ip"] + ":" + os.environ["robot_port"]
    try:
        
        # Initialize qi framework.
        app = qi.Application(["Maqui Robot", "--qi-url=" + connection_url])        
    except RuntimeError:
        print ("Can't connect to Naoqi at ip \"" + os.environ["robot_ip"] + "\" on port " + os.environ["robot_port"] +".\n"
                "Please check your script arguments. Run with -h option for help.")
        sys.exit(1)
    app.start()
    session = app.session

    compile_dics(session, args.path, args.filename, args.language)
