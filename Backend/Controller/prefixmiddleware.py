'''
(c) Global Biofoundries Alliance 2020

Licensed under the MIT License.

To view a copy of this license, visit <http://opensource.org/licenses/MIT/>.
'''
# pylint: disable=too-few-public-methods


class PrefixMiddleWare():
    '''Applies a url prefix to a flask application's routes.'''

    def __init__(self, app, prefix=''):
        self.app = app
        self.prefix = prefix

    def __call__(self, environ, start_response):
        if environ['PATH_INFO'].startswith(self.prefix):
            environ['PATH_INFO'] = environ['PATH_INFO'][len(self.prefix):]
            environ['SCRIPT_NAME'] = self.prefix
            return self.app(environ, start_response)

        # else:  # exclude requests without the prefix
        start_response('404', [('Content-Type', 'text/plain')])
        return ['The page requested does not exist'.encode()]
