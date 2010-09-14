import glob
import pkgutil
from cStringIO import StringIO
from ConfigParser import SafeConfigParser, NoSectionError, NoOptionError

class Config(object):
    """A ConfigParser wrapper to support defaults when calling instance
    methods, and also tied to a single section"""

    SECTION = 'scrapyd'

    def __init__(self, values=None):
        if values is None:
            sources = self._getsources()
            default_config = pkgutil.get_data(__package__, 'default_scrapyd.conf')
            self.cp = SafeConfigParser()
            self.cp.readfp(StringIO(default_config))
            self.cp.read(sources)
        else:
            self.cp = SafeConfigParser(values)
            self.cp.add_section(self.SECTION)

    def _getsources(self):
        sources = ['/etc/scrapyd/scrapyd.conf', r'c:\scrapyd\scrapyd.conf']
        sources += sorted(glob.glob('/etc/scrapyd/conf.d/*'))
        sources += ['scrapyd.conf']
        return sources

    def _getany(self, method, option, default):
        try:
            return method(self.SECTION, option)
        except (NoSectionError, NoOptionError):
            if default is not None:
                return default
            raise

    def get(self, option, default=None):
        return self._getany(self.cp.get, option, default)

    def getint(self, option, default=None):
        return self._getany(self.cp.getint, option, default)

    def getfloat(self, option, default=None):
        return self._getany(self.cp.getfloat, option, default)

    def getboolean(self, option, default=None):
        return self._getany(self.cp.getboolean, option, default)
