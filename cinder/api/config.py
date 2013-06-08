# Server Specific Configurations
server = {
    'port': '8776',
    'host': '0.0.0.0'
}

# Pecan Application Configurations
app = {
    'root': 'cinder.api.controllers.root.RootController',
    'modules': ['cinder.api'],
    'static_root': '%(confdir)s/public',
    'template_path': '%(confdir)s/cinder/api/templates',
    'debug': False,
}

# Custom Configurations must be in Python dictionary format::
#
# foo = {'bar':'baz'}
#
# All configurations are accessible at::
# pecan.conf
