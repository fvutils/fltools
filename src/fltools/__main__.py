'''
Created on Nov 23, 2019

@author: ballance
'''
from sys import stdout
from fltools.filelist_parser import FilelistParser
import sys
import os


def main():
    output=stdout
    
    i=1;
    while i < len(sys.argv):
        arg = sys.argv[i]
        # Stop looking for preprocessor options
        if arg == "--" or arg[0] != '-':
            break
        elif arg == "-o":
            i += 1
            output = open(sys.argv[i], "w")
        else:
            break;
        i += 1
        
    while i < len(sys.argv):
        arg = sys.argv[i]
        
        if arg == "-f" or arg == "-F":
            i += 1
            parser = FilelistParser()
            parser.parse(sys.argv[i], os.getcwd())
            
            for tok in parser.token_l:
                output.write(tok.get_img(True))
                output.write(" ")
        else:
            output.write(arg)
            output.write(" ")
        
        i += 1
        
    output.write("\n")
            
    if output is not stdout:
        output.close()
        
    pass

if __name__ == "__main__":
    main()