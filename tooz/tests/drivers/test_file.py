# -*- coding: utf-8 -*-

# Copyright 2016 Cloudbase Solutions Srl
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import mock
from testtools import testcase

from tooz import coordination
from tooz import tests


class TestFileDriver(testcase.TestCase):
    _FAKE_MEMBER_ID = tests.get_random_uuid()

    def test_base_dir(self):
        file_path = '/fake/file/path'
        url = 'file://%s' % file_path

        coord = coordination.get_coordinator(url, self._FAKE_MEMBER_ID)
        self.assertEqual(file_path, coord._dir)

    @mock.patch('os.path.normpath', lambda x: x.replace('/', '\\'))
    @mock.patch('sys.platform', 'win32')
    def test_base_dir_win32(self):
        coord = coordination.get_coordinator(
            'file:///C:/path/', self._FAKE_MEMBER_ID)
        self.assertEqual('C:\\path\\', coord._dir)

        coord = coordination.get_coordinator(
            'file:////share_addr/share_path/', self._FAKE_MEMBER_ID)
        self.assertEqual('\\\\share_addr\\share_path\\', coord._dir)

        # Administrative shares should be handled properly.
        coord = coordination.get_coordinator(
            'file:////c$/path/', self._FAKE_MEMBER_ID)
        self.assertEqual('\\\\c$\\path\\', coord._dir)
