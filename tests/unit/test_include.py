#****************************************************************************
#* test_include.py
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
import fltools as ft
from .test_base import TestBase

class TestInclude(TestBase):


    def test_resolve_cwd(self):
        self.addFile("root.F", """
        file1.txt
        file2.txt
        """)
        self.addFile("file1.txt", """
        file1.txt
        """)
        self.addFile("file2.txt", """
        file2.txt
        """)

        parser = ft.FilelistParser()
        tokens = parser.parse(
            os.path.join(self.testdir, "root.F"),
            self.testdir
        )

        print("tokens: %s" % str(tokens))

        self.assertEqual(
            os.path.normpath(os.path.join(self.testdir, "file1.txt")),
            tokens[0].resolve())

        self.assertEqual(
            os.path.normpath(os.path.join(self.testdir, "file2.txt")),
            tokens[1].resolve())

    def test_resolve_cwd_subfilelist(self):
        self.addFile("root.F", """
        -f ./subdir/filelist.f
        """)
        self.addFile("subdir/filelist.f", """
        file1.txt
        file2.txt
        """)
        self.addFile("file1.txt", """
        file1.txt
        """)
        self.addFile("file2.txt", """
        file2.txt
        """)

        parser = ft.FilelistParser()
        tokens = parser.parse(
            os.path.join(self.testdir, "root.F"),
            self.testdir
        )

        self.assertEqual(len(tokens), 2)

        self.assertEqual(
            os.path.normpath(os.path.join(self.testdir, "file1.txt")),
            tokens[0].resolve())

        self.assertEqual(
            os.path.normpath(os.path.join(self.testdir, "file2.txt")),
            tokens[1].resolve())

    def test_resolve_rel_subfilelist(self):
        self.addFile("root.F", """
        -F ./subdir/filelist.f
        """)
        self.addFile("subdir/filelist.f", """
        file1.txt
        file2.txt
        """)
        self.addFile("subdir/file1.txt", """
        file1.txt
        """)
        self.addFile("subdir/file2.txt", """
        file2.txt
        """)

        parser = ft.FilelistParser()
        tokens = parser.parse(
            os.path.join(self.testdir, "root.F"),
            self.testdir
        )

        self.assertEqual(len(tokens), 2)

        self.assertEqual(
            os.path.normpath(os.path.join(self.testdir, "subdir/file1.txt")),
            tokens[0].resolve())
        self.assertEqual(
            os.path.normpath(os.path.join(self.testdir, "subdir/filelist.f")),
            os.path.normpath(tokens[0].filename))

        self.assertEqual(
            os.path.normpath(os.path.join(self.testdir, "subdir/file2.txt")),
            tokens[1].resolve())
        self.assertEqual(
            os.path.normpath(os.path.join(self.testdir, "subdir/filelist.f")),
            os.path.normpath(tokens[1].filename))

    def test_duplicate_include_same_level(self):
        self.addFile("root.F", """
        -F ./subdir/filelist.f
        -F ./subdir/filelist.f
        """)
        self.addFile("subdir/filelist.f", """
        file1.txt
        file2.txt
        """)
        self.addFile("subdir/file1.txt", """
        file1.txt
        """)
        self.addFile("subdir/file2.txt", """
        file2.txt
        """)

        parser = ft.FilelistParser()
        tokens = parser.parse(
            os.path.join(self.testdir, "root.F"),
            self.testdir
        )

        self.assertEqual(len(tokens), 2)

        self.assertEqual(
            os.path.normpath(os.path.join(self.testdir, "subdir/file1.txt")),
            tokens[0].resolve())
        self.assertEqual(
            os.path.normpath(os.path.join(self.testdir, "subdir/filelist.f")),
            os.path.normpath(tokens[0].filename))

        self.assertEqual(
            os.path.normpath(os.path.join(self.testdir, "subdir/file2.txt")),
            tokens[1].resolve())
        self.assertEqual(
            os.path.normpath(os.path.join(self.testdir, "subdir/filelist.f")),
            os.path.normpath(tokens[1].filename))