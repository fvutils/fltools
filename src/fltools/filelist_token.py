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
from typing import Dict

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
            return FilelistToken._expand(self.img, self.parser.env)
        else:
            return self.img

    def resolve(self, expand_env=True):
        path = self.img

        if expand_env:
            path = FilelistToken._expand(path, self.parser.env)

        return self.parser._resolve(self.filename, path)

    @staticmethod                                            
    def _expand(expr: str, vars: Dict[str, str]) -> str:
        import re
        def repl(match):
            var = match.group(1) or match.group(2)
            return vars.get(var, match.group(0))
        # Match $VAR or ${VAR}
        pattern = r'\$([A-Za-z_][A-Za-z0-9_]*)|\$\{([A-Za-z_][A-Za-z0-9_]*)\}'
        return re.sub(pattern, repl, expr)
