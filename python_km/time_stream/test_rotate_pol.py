"""Unit tests for rotate_pol.py"""

import unittest

import scipy as sp
import numpy.ma as ma

import kiyopy.custom_exceptions as ce
from time_stream import rotate_pol
from core import data_block, fitsGBT

test_file = 'testfile_GBTfits.fits'

class TestRotate(unittest.TestCase) :
    
    def setUp(self) :
        Reader = fitsGBT.Reader(test_file, feedback=0)
        self.Data = Reader.read(1,0)

    def test_runs(self) :
        rotate_pol.rotate(self.Data, (1,))
        self.Data.verify()

    def test_dims(self) :
        dims = self.Data.dims
        rotate_pol.rotate(self.Data, (1,))
        dims = dims[:1] + (1,) + dims[2:]
        self.assertEqual(self.Data.dims, dims)
        

    def tearDown(self) :
        del self.Data

if __name__ == '__main__' :
    unittest.main()
