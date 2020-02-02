
import unittest
from unittest.case import TestCase
import io
import fltools

class TestInput(TestCase):
    
    def test_comments(self):
        fp = io.BytesIO(
b'''/**
 * This is a comment
 */
tok1
tok2
'''
            )

        input = fltools.FilelistParser.Input(None, 0, fp)
        
        for tok in input:
            print("tok=" + str(tok))
            
#         tok = input.readtok()
#         print("tok=" + str(tok))
#         tok = input.readtok()
#         print("tok=" + str(tok))
#         tok = input.readtok()
#         print("tok=" + str(tok))
        