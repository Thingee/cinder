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

from oslo.config import cfg
from pecan import hooks
import webob.exc

from cinder import context
from cinder import flags
from cinder.openstack.common import log as logging

use_forwarded_for_opt = cfg.BoolOpt(
    'use_forwarded_for',
    default=False,
    help='Treat X-Forwarded-For as the canonical remote address. '
         'Only enable this if you have a sanitizing proxy.')

FLAGS = flags.FLAGS
FLAGS.register_opt(use_forwarded_for_opt)
LOG = logging.getLogger(__name__)


class ConfigHook(hooks.PecanHook):
    """Attach the config object to the request for controllers"""

    def before(self, state):
        state.request.cfg = cfg.CONF


class KeystoneContextHook(hooks.PecanHook):
    """Make a request context from keystone headers"""

    def before(self, state):
        request = state.request
        headers = request.headers

        user_id = headers.get('X_USER')
        user_id = headers.get('X_USER_ID', user_id)
        if user_id is None:
            LOG.debug("Neither X_USER_ID nor X_USER found in request")
            return webob.exc.HTTPUnauthorized()
        # get the roles
        roles = [r.strip() for r in headers.get('X_ROLE', '').split(',')]
        if 'X_TENANT_ID' in headers:
            # This is the new header since Keystone went to ID/Name
            project_id = headers['X_TENANT_ID']
        else:
            # This is for legacy compatibility
            project_id = headers['X_TENANT']

        # Get the auth token
        auth_token = headers.get('X_AUTH_TOKEN',
                                 headers.get('X_STORAGE_TOKEN'))

        # Build a context, including the auth_token...
        remote_address = request.remote_addr
        if FLAGS.use_forwarded_for:
            remote_address = headers.get('X-Forwarded-For', remote_address)
        ctx = context.RequestContext(user_id,
                                     project_id,
                                     roles=roles,
                                     auth_token=auth_token,
                                     remote_address=remote_address)

        request.environ['cinder.context'] = ctx
