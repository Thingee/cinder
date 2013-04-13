from cinder.api.middleware import auth
from cinder.openstack.common import log as logging


LOG = logging.getLogger(__name__)


class CinderKeystoneContext(auth.CinderKeystoneContext):
    def __init__(self, application):
        LOG.warn('cinder.api.auth:CinderKeystoneContext is deprecated. Please '
                 'use cinder.api.middleware.auth:CinderKeystoneContext '
                 'instead.')
        super(CinderKeystoneContext, self).__init__(application)


def pipeline_factory(loader, global_conf, **local_conf):
    LOG.warn('cinder.api.auth:pipeline_factory is deprecated. Please use '
             'cinder.api.middleware.pipeline_factory instead.')
    auth.pipeline_factory(loader, global_conf, **local_conf)
