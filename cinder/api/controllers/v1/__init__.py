# Copyright (c) 2013 OpenStack, LLC.
#
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

import pecan

from cinder.api.controllers.v1 import volumes


class RouterController(object):
    volumes = volumes.VolumesController()

    def __init__(self, tenant_id):
        self.tenant_id = tenant_id


class V1Controller(object):
    @pecan.expose()
    def _lookup(self, tenant_id, *remainder):
        return RouterController(tenant_id), remainder
