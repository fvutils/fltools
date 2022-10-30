#****************************************************************************
#* filelist_token.py
#*
#* Copyright 2022 Matthew Ballance and Contributors
#*
#* Licensed under the Apache License, Version 2.0 (the "License"); you may 
#* not use this file except in compliance with the License.  
#* You may obtain a copy of the License at:
#*
#*   http://www.apache.org/licenses/LICENSE-2.0
#*
#* Unless required by applicable law or agreed to in writing, software 
#* distributed under the License is distributed on an "AS IS" BASIS, 
#* WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.  
#* See the License for the specific language governing permissions and 
#* limitations under the License.
#*
#*
#* Created on Nov 23, 2019
#*
#* @author: ballance
#*
#****************************************************************************

import os
from typing import Dict
from .filelist_token import FilelistToken

class FilelistParser():
    
    class Input():
        def __init__(self, parser, filename, fp):
            self.parser = parser
            self.filename = filename
            self.fp = fp
            self.lineno = 1
            self.linepos = 1
            self.last_c = b''
            self.unget_c = b''
            pass
        
        def __iter__(self):
            return self
        
        def __next__(self):
            tok = self.readtok()
            
            if tok == None:
                raise StopIteration
            
            return FilelistToken(
                self.parser,
                self.filename,
                tok[0],
                tok[1],
                tok[2]
                )
            
            # 
            return self.read_tok()
        
        def readtok(self):
            ch=b''
            ch2=b''
            ret=""
            start_lineno = -1
            start_linepos = -1
            
            while True:
                ch = self.getch()
                if ch == b'':
                    break
                
                if (ch == b'/'):
                    ch2 = self.getch()
                    if ch2 == b'*':
                        cc1 = b''
                        cc2 = b''
                        
                        while True:
                            ch = self.getch()
                            if ch == b'':
                                break
                            cc2 = cc1
                            cc1 = ch
                            if cc1 == b'/' and cc2 == b'*':
                                break
                        continue
                    elif ch2 == b'/':
                        while True:
                            ch = self.getch()
                            if ch == b'' or ch == b'\n':
                                break
                        self.ungetch(ch)
                        continue
                    else:
                        self.ungetch(ch2)
                elif ch == b' ' or ch == b'\t' or ch == b'\n' or ch == b'\r':
                    while True:
                        ch = self.getch()
                        if ch == b'' or not (ch == b' ' or ch == b'\t' or ch == b'\n' or ch == b'\r'):
                            break
                    self.ungetch(ch)
                    continue
                else: # Actually a non-whitespace/non-comment character
                    start_lineno = self.lineno
                    start_linepos = self.linepos
                    break
                
            while ch != b'' and not (ch == b' ' or ch == b'\t' or ch == b'\n' or ch == b'\r'):
                ret += ch.decode("utf-8")
                ch = self.getch()
            self.ungetch(ch)
            
            if ret == "":
                return None
            else:
                return (ret, start_lineno, start_linepos)
        
        def getch(self):
            ch = b''
            if self.unget_c != b'':
                ch = self.unget_c
                self.unget_c = b''
            else:
                ch = self.fp.read(1)
                if self.last_c == b'\n':
                    self.linepos = 1
                    self.lineno += 1
                else:
                    self.linepos += 1
                    
                self.last_c = ch
                
            return ch
        
        def ungetch(self, c):
            self.unget_c = c
        
    def __init__(self):
        # Map of path to a stack of inclusion locations
        self.filename_m : Dict[str,'FilelistParser.FileInfo'] = {}
        self.input_s = []
        self.include_s = []
        self.token_l = []
        self.fail_on_error = False
        self.backtrace_on_error = False
        self.expand_env = True
        
    def set_fail_on_error(self, f):
        self.fail_on_error = f
        
    def set_backtrace_on_error(self, f):
        self.backtrace_on_error = f
        
    def set_expand_env(self, e):
        self.expand_env = e
        
    def error(self, msg):
        print("Error: " + msg)
        if self.fail_on_error:
            raise Exception(msg)
        
    def warning(self, msg):
        print("Warning: " + msg)

    def parse(self, path, relative_path_basedir):
        """
        Parse a filelist and return a flat list of tokens
        """
        if not os.path.exists(path):
            self.error("path \"" + path + "\" does not exist")
            return

        if len(self.input_s) == 0:
            # This is the first file, so add it to the map
            self.include_s.append(("command line", -1))

        self.filename_m[path] = FilelistParser.FileInfo(
            relative_path_basedir, 
            self.include_s.copy())
        
        try:
            fp = open(path, "rb")
        except Exception as e:
            self.error("failed to read file \"" + path + "\" (" + str(e) + ")")
            return
        
        input = FilelistParser.Input(self, path, fp)
        self.input_s.append(input)
        
        # Now, process content until we're done
        it = iter(input)
        while True:
            try:
                tok = next(it)
            except StopIteration:
                break
                pass
            
            if tok.img == "-f" or tok.img == "-F":
                inc_filename = tok.filename
                inc_lineno = tok.lineno
                is_caps_f = (tok.img == "-F")

                # Sub-inclusion
                try:
                    tok = next(it)
                except StopIteration:
                    # TODO: this is a missing filename
                    print("Error: no filename")
                    break
                    pass

                full_path = tok.resolve()
                print("full_path: %s" % full_path)

                self.include_s.append((inc_filename, inc_lineno))
                if full_path in self.filename_m.keys():
                    # TODO: multiple inclusion
                    # The include_s contains the full path of how
                    # we got here. The filename_m entry contains
                    # the full path of how the original file was 
                    # included
                    print("Error: multiple inclusion")
                    pass
                else:
                    if is_caps_f:
                        rel_basedir = os.path.dirname(full_path)
                    else:
                        rel_basedir = relative_path_basedir
                        
                    self.parse(full_path, rel_basedir)
                self.include_s.pop()
            else:
                self.token_l.append(tok)
        
        self.input_s.pop()

        return self.token_l

    def _resolve(self, src_filelist, path):
        if src_filelist not in self.filename_m.keys():
            raise Exception("Filelist %s was not previously processed" % src_filelist)
        
        return self.filename_m[src_filelist].resolve(path)

    class FileInfo(object):

        def __init__(self, relpath_resolve_base, inc_s):
            self.relpath_resolve_base = relpath_resolve_base
            self.inc_s = inc_s

        def resolve(self, path):
            if os.path.isabs(path):
                return os.path.normpath(path)
            else:
                return os.path.normpath(
                    os.path.join(self.relpath_resolve_base, path))

    
    