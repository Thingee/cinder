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
import wsme
from wsme import types as wtypes
import wsmeext.pecan as wsme_pecan

from cinder.db.sqlalchemy import models
from cinder import exception
from cinder.openstack.common import log as logging
from cinder.openstack.common import uuidutils
from cinder import volume as vol
from cinder.volume import volume_types


LOG = logging.getLogger(__name__)


class _Base(wtypes.Base):

    @classmethod
    def from_db_model(cls, m):
        # NOTE (thingee): Unfortunately some methods in the model are returning
        # dicts and others aren't. This will be fixed later when we introduce
        # an abstract storage layer.
        if isinstance(m, dict):
            return cls(**m)
        return cls(**(m.__dict__))

    def as_dict(self, db_model):
        return dict((k, getattr(self, k))
                    for k in db_model.__dict__
                    if hasattr(self, k) and
                    getattr(self, k) != wsme.Unset)


class Volume(_Base):
    id = wtypes.text
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
    metadata = {wtypes.text: wtypes.text}


class VolumeSummary(_Base):
    id = wtypes.text
    display_name = wtypes.text


class VolumesController(rest.RestController):

    _custom_actions = {
        'details': ['GET'],
    }

    def __init__(self):
        self.volume_api = vol.API()
        super(VolumesController, self).__init__()

    @wsme_pecan.wsexpose(Volume, wtypes.text)
    def get_one(self, id):
        context = pecan.request.environ['cinder.context']
        try:
            volume = self.volume_api.get(context, id)
        except exception.NotFound:
            pecan.abort(404)
        return Volume.from_db_model(volume)

    @wsme_pecan.wsexpose([VolumeSummary])
    def get_all(self):
        context = pecan.request.environ['cinder.context']
        volumes = self.volume_api.get_all(context)
        return [Volume.from_db_model(m)
                for m in volumes]

    @wsme_pecan.wsexpose([Volume])
    def details(self):
        context = pecan.request.environ['cinder.context']
        volumes = self.volume_api.get_all(context)
        return [Volume.from_db_model(m)
                for m in volumes]

    @wsme.validate(Volume)
    @wsme_pecan.wsexpose(Volume, wtypes.text, body=Volume)
    def put(self, id, volume):
        context = pecan.request.environ['cinder.context']
        volume_body = volume.as_dict(models.Volume)
        try:
            volume = self.volume_api.get(context, id)
        except exception.NotFound:
            pecan.abort(404)
        volume.update(volume_body)
        return Volume.from_db_model(volume)

    @wsme_pecan.wsexpose(Volume, wtypes.text, status_code=202)
    def delete(self, id):
        context = pecan.request.environ['cinder.context']
        try:
            volume = self.volume_api.get(context, id)
        except exception.NotFound:
            pecan.abort(404)
        self.volume_api.delete(context, volume)

    @wsme.validate(Volume)
    @wsme_pecan.wsexpose(Volume, Volume)
    def post(self, volume):
        """Creates a new volume."""

        context = pecan.request.environ['cinder.context']

        kwargs = {}
        if volume.metadata is not wsme.Unset:
            kwargs['metadata'] = volume.metadata

        volume = volume.as_dict(models.Volume)

        req_volume_type = volume.get('volume_type', None)
        if req_volume_type:
            if not uuidutils.is_uuid_like(req_volume_type):
                try:
                    kwargs['volume_type'] = (
                        volume_types.get_volume_type_by_name(
                            context, req_volume_type)
                    )
                except exception.VolumeTypeNotFound:
                    explanation = 'Volume type not found.'
                    pecan.abort(404, detail=explanation)
            else:
                try:
                    kwargs['volume_type'] = volume_types.get_volume_type(
                        context, req_volume_type)
                except exception.VolumeTypeNotFound:
                    explanation = 'Volume type not found.'
                    pecan.abort(404, detail=explanation)

        snapshot_id = volume.get('snapshot_id')
        if snapshot_id is not None:
            kwargs['snapshot'] = self.volume_api.get_snapshot(context,
                                                              snapshot_id)
        else:
            kwargs['snapshot'] = None

        source_volid = volume.get('source_volid')
        if source_volid is not None:
            kwargs['source_volume'] = self.volume_api.get_volume(context,
                                                                 source_volid)
        else:
            kwargs['source_volume'] = None

        size = volume.get('size', None)
        if size is None and kwargs['snapshot'] is not None:
            size = kwargs['snapshot']['volume_size']
        elif size is None and kwargs['source_volume'] is not None:
            size = kwargs['source_volume']['size']

        kwargs['availability_zone'] = volume.get('availability_zone', None)

        new_volume = self.volume_api.create(context,
                                            size,
                                            volume.get('display_name'),
                                            volume.get('display_description'),
                                            **kwargs)
        return Volume.from_db_model(new_volume)
