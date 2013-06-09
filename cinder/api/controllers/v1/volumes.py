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

import datetime

import pecan
from pecan import rest
from wsme import types as wtypes
import wsmeext.pecan as wsme_pecan

from cinder import volume


class _Base(wtypes.Base):

    @classmethod
    def from_db_model(cls, m):
        return cls(**m)


class Volume(_Base):
    id = wtypes.text
    name = wtypes.text
    ec2_id = int
    user_id = wtypes.text
    project_id = wtypes.text
    snapshot_id = wtypes.text
    host = wtypes.text
    size = int
    availability_zone = wtypes.text
    instance_uuid = wtypes.text
    mountpoint = wtypes.text
    attach_time = wtypes.text
    status = wtypes.text
    attach_status = wtypes.text
    scheduled_at = datetime.datetime
    launched_at = datetime.datetime
    terminated_at = datetime.datetime
    display_name = wtypes.text
    display_description = wtypes.text
    provider_location = wtypes.text
    provider_auth = wtypes.text
    volume_type_id = wtypes.text
    source_volid = wtypes.text


class VolumesController(rest.RestController):
    def __init__(self):
        self.volume_api = volume.API()

    @wsme_pecan.wsexpose(Volume)
    def get_one(self, id):
        vol = self.volume_api.get(pecan.request.context, id)
        return Volume.from_db_model(vol)
