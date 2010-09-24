"""Unit tests for data_block module."""

import unittest

import scipy as sp
import numpy.ma as ma

import data_block as db
import fitsGBT
import kiyopy.custom_exceptions as ce

ntimes = 5
npol = 4
ncal = 2
nfreq = 10
dims = (ntimes, npol, ncal, nfreq)

def standard_data_test(utest_case) :
    """Encapsulates a few tests on TestDB.data.

    These test should pass any time we expect the a data block to have valid
    data."""

    for ii in range(4) :
        utest_case.assertEqual(dims[ii], utest_case.TestDB.dims[ii])
    utest_case.assertTrue(utest_case.TestDB.data_set)
    dir_data = dir(utest_case.TestDB.data)
    utest_case.assertTrue(dir_data.count('mask'))


class TestDataSetup(unittest.TestCase) :
    
    def setUp(self) :
        self.testdata = sp.reshape(sp.arange(ntimes*npol*ncal*nfreq,
                                   dtype=float), (ntimes,npol,ncal,nfreq))
        
    def test_init_sets_data(self) :
        self.TestDB = db.DataBlock(self.testdata)
        standard_data_test(self)

    def test_init_no_data(self) :
        self.TestDB = db.DataBlock()
        self.assertTrue(not self.TestDB.data_set)
        self.TestDB.set_data(self.testdata)
        standard_data_test(self)

    def tearDown(self) :
        del self.TestDB
        del self.testdata

class TestFields(unittest.TestCase) :
    
    def setUp(self) :
        # make valid data
        self.testdata = sp.reshape(sp.arange(ntimes*npol*ncal*nfreq,
                                   dtype=float), (ntimes,npol,ncal,nfreq))
        self.TestDB = db.DataBlock(self.testdata)
        self.LST_test = sp.arange(ntimes)
        self.TestDB.set_field('LST', self.LST_test, ('time',))
        # Make sure that 'verify' passes on good data:
        self.TestDB.verify()

    def test_set_get_field(self) :
        stored_LST = self.TestDB.field['LST']
        # The obviouse tests.
        for ii in range(ntimes) :
            self.assertAlmostEqual(self.TestDB.field['LST'][ii], 
                                   stored_LST[ii])
        self.assertEqual(self.TestDB.field_axes['LST'][0], 'time')
        # Test that it's checking for a valid axis.
        self.assertRaises(ValueError, self.TestDB.set_field, 'abc', 5, 
                          ('not_a_axis',))
        # Test that we've copied dereferenced data into the DataBlock
        self.LST_test[0] = -100.
        self.assertEqual(self.TestDB.field['LST'][0], stored_LST[0])

    def test_verify_keys_match1(self) :
        self.TestDB.field['stuff'] = range(5)
        self.assertRaises(ce.DataError, self.TestDB.verify)
        
    def test_verify_keys_match2(self) :
        """Oppotsite case of the last test."""
        self.TestDB.field_axes['stuff'] = ('time',)
        self.assertRaises(ce.DataError, self.TestDB.verify)

    def test_verify_valid_axes(self) :
        self.TestDB.field_axes['LST'] = ('not_an_axis',)
        self.assertRaises(ValueError, self.TestDB.verify)

    def test_multiD_field(self) :
        self.assertRaises(NotImplementedError, self.TestDB.set_field, 'afield', 
                          sp.ones((npol,ncal)), ('pol', 'cal'))

    def test_zeroD_fields(self) :
        self.TestDB.set_field('SCAN', 113)
        self.TestDB.verify()
        self.assertEqual(self.TestDB.field['SCAN'], 113)
        self.assertEqual(len(self.TestDB.field_axes['SCAN']), 0)

    def test_verify_field_shape(self) :
        self.TestDB.set_field('CRVAL4', [-5,-6,-7,-8,-9], 'pol')
        self.assertRaises(ce.DataError, self.TestDB.verify)
        
        

    def tearDown(self) :
        del self.TestDB
        del self.testdata
        del self.LST_test
        
        




        
        



if __name__ == '__main__' :
    unittest.main()
