from cinder.api.v1.router import APIRouter as v1_router
from cinder.openstack.common import log as logging

LOG = logging.getLogger(__name__)


class APIRouter(v1_router):
    def __init__(self, ext_mgr=None):
        LOG.warn('cinder.api.openstack.volume:APIRouter is deprecated. '
                 'Please use cinder.api.v1.router:APIRouter instead.')
        super(APIRouter, self).__init__(ext_mgr)
