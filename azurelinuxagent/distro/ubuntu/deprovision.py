# Windows Azure Linux Agent
#
# Copyright 2014 Microsoft Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Requires Python 2.4+ and Openssl 1.0+
#

import os
import azurelinuxagent.logger as logger
import azurelinuxagent.utils.fileutil as fileutil
from azurelinuxagent.distro.default.deprovision import DeprovisionHandler, DeprovisionAction

def DeleteResolve():
    if os.path.realpath('/etc/resolv.conf') != '/run/resolvconf/resolv.conf':
        logger.Info("resolvconf is not configured. Removing /etc/resolv.conf")
        fileutil.RemoveFiles('/etc/resolv.conf')
    else:
        logger.Info("resolvconf is enabled; leaving /etc/resolv.conf intact")
        fileutil.RemoveFiles('/etc/resolvconf/resolv.conf.d/tail',
                             '/etc/resolvconf/resolv.conf.d/originial')


class UbuntuDeprovisionHandler(DeprovisionHandler):
    def setUp(self, deluser):
        warnings, actions = super(UbuntuDeprovisionHandler, self).setUp(deluser)
        warnings.append("WARNING! Nameserver configuration in "
                        "/etc/resolvconf/resolv.conf.d/{tail,originial} "
                        "will be deleted.")
        actions.append(DeprovisionAction(DeleteResolve))
        return warnings, actions

