from cinder.api.middleware import sizelimit
from cinder.openstack.common import log as logging

LOG = logging.getLogger(__name__)


class RequestBodySizeLimiter(sizelimit.RequestBodySizeLimiter):
    def __init__(self, *args, **kwargs):
        LOG.warn('cinder.api.sizelimit:RequestBodySizeLimiter is deprecated. '
                 'Please use cinder.api.middleware.sizelimit:'
                 'RequestBodySizeLimiter instead')
        super(RequestBodySizeLimiter, self).__init__(*args, **kwargs)
