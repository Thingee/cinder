# Copyright 2014 OpenStack Foundation.
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


from cinder.brick import executor
from cinder import exception
from cinder.openstack.common import log as logging
from cinder.openstack.common import processutils as putils

LOG = logging.getLogger(__name__)


class TargetAdmin(executor.Executor):
    """Base vHost target admin class."""

    def __init__(self, cmd, root_helper, execute):
        super(TargetAdmin, self).__init__(root_helper, execute=execute)
        self._cmd = cmd

    def create_target(self, name, path):
        raise NotImplementedError()

    def remove_target(self, name, path):
        raise NotImplementedError()


class LioAdm(TargetAdmin):
    def __init__(self, root_helper, execute=putils.execute):
        super(LioAdm, self).__init__('cinder-rtstool', root_helper, execute)

        self._verify_rtstool()

    def _verify_rtstool(self):
        try:
            self._execute('cinder-rtstool', 'verify')
        except (OSError, putils.ProcessExecutionError):
            LOG.error(_('cinder-rtstool is not installed correctly'))
            raise

    def create_target(self, name, path):
        try:
            command_args = ['cinder-rtstool', 'create_vhost', name, path]
            (name, _) = self._execute(*command_args, run_as_root=True)
        except putils.ProcessExecutionError as e:
            LOG.error(_("Failed to create vhost target for volume"))
            LOG.error("%s" % e)

            raise exception.VhostTargetCreateFailed(name=name)
        return name

    def remove_target(self, name):
            try:
                self._execute('cinder-rtstool', 'delete', name,
                              run_as_root=True)
            except putils.ProcessExecutionError as e:
                LOG.error(_("Failed to remove vhost target"))
                LOG.error("%s" % e)
                raise exception.VhostTargetRemoveFailed(name=name)
