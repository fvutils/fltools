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
#* Created on:
#*     Author: 
#*
#****************************************************************************
import os

class FilelistToken(object):
    """
    Contains data on a single token from a filelist
    """

    def __init__(self,
                parser,
                filename,
                img, 
                lineno,
                linepos):
        self.parser   = parser
        self.img      = img
        self.filename = filename
        self.lineno   = lineno
        self.linepos  = linepos
            
    def get_img(self, expand_env=False):
        if expand_env:
            return FilelistToken._expand(self.img)
        else:
            return self.img

    def resolve(self, expand_env=True):
        path = self.img

        if expand_env:
            path = FilelistToken._expand(path)

        return self.parser._resolve(self.filename, path)

    @staticmethod           
    def _expand(str):
        i=0
        ret = ""
        while i < len(str):
            d_idx = str.find('$', i)
            if d_idx != -1:
                ret += str[i:d_idx]
                if str[d_idx+1] == '{':
                    c_idx = str.find('}', d_idx+2)
                    if c_idx != -1:
                        key = str[d_idx+2:c_idx]
                        if key in os.environ:
                            ret += os.environ[key]
                        i = c_idx+1
                    else:
                        ret += str[d_idx+1]
                        i = d_idx+2
                else:
                    ret += str[i+1]
                    i += 1
            else:
                ret += str[i:]
                break
        return ret

