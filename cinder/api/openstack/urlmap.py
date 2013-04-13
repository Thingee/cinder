from cinder.api import urlmap
from cinder.openstack.common import log as logging


LOG = logging.getLogger(__name__)


def urlmap_factory(loader, global_conf, **local_conf):
    LOG.warn('cinder.api.openstack.urlmap:urlmap_factory is deprecated. '
             'Please use cinder.api.urlmap:urlmap_factory instead.')
    urlmap.urlmap_factory(loader, global_conf, **local_conf)
