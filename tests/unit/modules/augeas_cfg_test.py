# -*- coding: utf-8 -*-
'''
    :codeauthor: :email:`Jayesh Kariya <jayeshk@saltstack.com>`
'''

# Import Salt Testing Libs
from salttesting import TestCase, skipIf
from salttesting.mock import (
    MagicMock,
    patch,
    NO_MOCK,
    NO_MOCK_REASON
)
# Make sure augeas python interface is installed
HAS_AUGEAS = False
try:
    from augeas import Augeas as _Augeas
    HAS_AUGEAS = True
except ImportError:
    pass

# Import Salt Libs
from salt.modules import augeas_cfg
from salt.exceptions import SaltInvocationError


@skipIf(NO_MOCK, NO_MOCK_REASON)
class AugeasCfgTestCase(TestCase):
    '''
    Test cases for salt.modules.augeas_cfg
    '''
    # 'execute' function tests: 3

    def test_execute(self):
        '''
        Test if it execute Augeas commands
        '''
        self.assertEqual(augeas_cfg.execute(), {'retval': True})

    def test_execute_io_error(self):
        '''
        Test if it execute Augeas commands
        '''
        ret = {'error': 'Command  is not supported (yet)', 'retval': False}
        self.assertEqual(augeas_cfg.execute(None, None, [" "]), ret)

    def test_execute_value_error(self):
        '''
        Test if it execute Augeas commands
        '''
        ret = {'retval': False,
               'error':
        'Invalid formatted command, see debug log for details: '}
        self.assertEqual(augeas_cfg.execute(None, None, ["set "]), ret)

    # 'get' function tests: 1

    def test_get(self):
        '''
        Test if it get a value for a specific augeas path
        '''
        mock = MagicMock(side_effect=RuntimeError('error'))
        with patch.object(_Augeas, 'match', mock):
            self.assertEqual(augeas_cfg.get('/etc/hosts'),
                             {'error': 'error'})

        mock = MagicMock(return_value=True)
        with patch.object(_Augeas, 'match', mock):
            self.assertEqual(augeas_cfg.get('/etc/hosts'),
                             {'/etc/hosts': None})

    # 'setvalue' function tests: 4

    def test_setvalue(self):
        '''
        Test if it set a value for a specific augeas path
        '''
        self.assertEqual(augeas_cfg.setvalue('prefix=/etc/hosts'),
                         {'retval': True})

    def test_setvalue_io_error(self):
        '''
        Test if it set a value for a specific augeas path
        '''
        mock = MagicMock(side_effect=IOError(''))
        with patch.object(_Augeas, 'save', mock):
            self.assertEqual(augeas_cfg.setvalue('prefix=/files/etc/'),
                             {'retval': False, 'error': ''})

    def test_setvalue_uneven_path(self):
        '''
        Test if it set a value for a specific augeas path
        '''
        mock = MagicMock(side_effect=RuntimeError('error'))
        with patch.object(_Augeas, 'match', mock):
            self.assertRaises(SaltInvocationError, augeas_cfg.setvalue,
                              ['/files/etc/hosts/1/canonical', 'localhost'])

    def test_setvalue_one_prefix(self):
        '''
        Test if it set a value for a specific augeas path
        '''
        self.assertRaises(SaltInvocationError, augeas_cfg.setvalue,
                          'prefix=/files', '10.18.1.1', 'prefix=/etc', 'test')

    # 'match' function tests: 2

    def test_match(self):
        '''
        Test if it matches for path expression
        '''
        self.assertEqual(augeas_cfg.match('/etc/service', 'ssh'), {})

    def test_match_runtime_error(self):
        '''
        Test if it matches for path expression
        '''
        mock = MagicMock(side_effect=RuntimeError('error'))
        with patch.object(_Augeas, 'match', mock):
            self.assertEqual(augeas_cfg.match('/etc/service-name', 'ssh'), {})

    # 'remove' function tests: 2

    def test_remove(self):
        '''
        Test if it removes for path expression
        '''
        self.assertEqual(augeas_cfg.remove('/etc/service'),
                         {'count': 0, 'retval': True})

    def test_remove_io_runtime_error(self):
        '''
        Test if it removes for path expression
        '''
        mock = MagicMock(side_effect=RuntimeError('error'))
        with patch.object(_Augeas, 'save', mock):
            self.assertEqual(augeas_cfg.remove('/etc/service-name'),
                             {'count': 0, 'error': 'error', 'retval': False})

    # 'ls' function tests: 1

    def test_ls(self):
        '''
        Test if it list the direct children of a node
        '''
        self.assertEqual(augeas_cfg.ls('/etc/passwd'), {})

    # 'tree' function tests: 1

    def test_tree(self):
        '''
        Test if it returns recursively the complete tree of a node
        '''
        self.assertEqual(augeas_cfg.tree('/etc/'), {'/etc': None})


if __name__ == '__main__':
    from integration import run_tests
    run_tests(AugeasCfgTestCase, needs_daemon=False)
