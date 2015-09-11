""" murls (Mutable URL Strings): a concise and expressive way to manipulate URLs. """

from collections import UserString


class Url(UserString):
    """ The base class for Mutable URL Strings. """

    _template = ('{schema}://'
                 '{username}{colon1}{password}{at}'
                 '{host}{colon2}{port}'
                 '{forward_slash}{path}'
                 '{question_mark}{query}'
                 '{hash}{fragment}')

    _keys = {'schema', 'username', 'password', 'host', 'path', 'query', 'fragment', 'port'}

    def __init__(self, url=''):
        super(Url, self).__init__(url)

        self._parts = {'schema': str(),
                       'host': str(),
                       'path': tuple(),
                       'query': dict(),
                       'fragment': str(),
                       'username': str(),
                       'password': str(),
                       'port': int()}

    def __iter__(self):
        for key, value in self._parts.items():
            yield (key, value)

    def host(self, host):
        self._parts['host'] = host
        self.data = self._build()
        return self

    def schema(self, schema=None):
        self._parts['schema'] = schema
        self.data = self._build()
        return self

    def port(self, port=None):
        self._parts['port'] = port
        self.data = self._build()
        return self

    def username(self, username=None):
        if not username:
            self._parts['password'] = None
        self._parts['username'] = username
        self.data = self._build()
        return self

    def password(self, password=None):
        self._parts['password'] = password
        self.data = self._build()
        return self

    def fragment(self, fragment=None):
        self._parts['fragment'] = fragment
        self.data = self._build()
        return self

    def path(self, *path):
        if path[0] is not None:
            self._parts['path'] = path
        else:
            self._parts['path'] = None
        self.data = self._build()
        return self

    def query(self, *args, **kwargs):
        if kwargs:
            self._query.update(kwargs)
            self._parts['query'] = {k: v for k, v in self._query.items() if v is not None}
        elif args[0] is None:
            self._parts['query'] = None
        self.data = self._build()
        return self

    @property
    def _strings(self):
        return {
            'schema': self._parts['schema'],
            'username': self._username if self._username else '',
            'colon1': ':' if self._password else '',
            'password': self._password if self._password else '',
            'host': self._host if self._host else '',
            'colon2': ':' if self._port else '',
            'port': str(self._port) if self._port else '',
            'forward_slash': '/' if self._path or self._fragment else '',
            'path': '/'.join(map(str, self._path)) if self._path else '',
            'question_mark': '?' if self._query else '',
            'query': '&'.join([str(k) + '=' + str(v) for k, v in self._query.items()]) if self._query else '',
            'hash': '#' if self._fragment else '',
            'fragment': self._fragment if self._fragment else '',
            'at': '@' if self._username else ''
        }

    def get(self, key):
        return self._parts[key]

    @property
    def strings(self):
        return {k: v for k, v in self._strings.items() if k in self._keys}

    @property
    def parts(self):
        return {k: v for k, v in self._parts.items() if k in self._keys}

    def _build(self):
        return self._template.format(**self._strings)

    @property
    def _schema(self):
        return self._parts['schema']

    @property
    def _username(self):
        return self._parts['username']

    @property
    def _password(self):
        return self._parts['password']

    @property
    def _host(self):
        return self._parts['host']

    @property
    def _port(self):
        return self._parts['port']

    @property
    def _path(self):
        return self._parts['path']

    @property
    def _query(self):
        return self._parts['query']

    @property
    def _fragment(self):
        return self._parts['fragment']


class Http(Url):
    def __init__(self, site):
        super(Http, self).__init__('')
        self._parts['schema'] = 'http'
        self._parts['host'] = site
        self.data = self._build()


class Https(Url):
    def __init__(self, site):
        super(Https, self).__init__('')
        self._parts['schema'] = 'https'
        self._parts['host'] = site
        self.data = self._build()


def http(site):
    return Http(site)


def https(site):
    return Https(site)


if __name__ == '__main__':
    pass
