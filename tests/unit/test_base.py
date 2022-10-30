#****************************************************************************
#* test_base.py
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
import shutil
from unittest import TestCase


class TestBase(TestCase):

    def setUp(self) -> None:
        self.rundir = os.path.join(
            os.path.dirname(
                os.path.dirname(
                    os.path.abspath(__file__))), "rundir")
        self.testdir = os.path.join(self.rundir, "_".join(self.id().split(".")))
        if os.path.isdir(self.testdir):
            shutil.rmtree(self.testdir)
        os.makedirs(self.testdir)
        print("Testcase: %s" % self.id())
        return super().setUp()
    pass

    def tearDown(self) -> None:
        print("Testcase: %s" % self.id())
#        shutil.rmtree(self.testdir)
        return super().tearDown()

    def addFile(self, path, content):
        dirname = os.path.dirname(path)

        if dirname != "" and not os.path.isdir(os.path.join(self.testdir, dirname)):
            os.makedirs(os.path.join(self.testdir, dirname))

        with open(os.path.join(self.testdir, path), "w") as fp:
            fp.write(content)

        


