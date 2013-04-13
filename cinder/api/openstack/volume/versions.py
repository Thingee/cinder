from cinder.api import versions
from cinder.openstack.common import log as logging


LOG = logging.getLogger(__name__)


class Versions(versions.Versions):
    def __init__(self):
        LOG.warn('cinder.api.openstack.volume.versions.Versions is deprecated '
                 'Please use cinder.api.versions.Versions instead.')
        super(Versions, self).__init__()
