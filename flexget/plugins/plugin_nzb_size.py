import logging
from flexget.plugin import *

log = logging.getLogger('nzb_size')


class NzbSize(object):

    """
    Provides entry size information when dealing with nzb files
    """

    @priority(200)
    def on_feed_modify(self, feed):
        """
        The downloaded file is accessible in modify event
        """
        from pynzb import nzb_parser

        for entry in feed.accepted:

            if entry.get('mime-type', None) not in [u'text/nzb', u'application/x-nzb'] or \
               not entry.get('filename', '').endswith('.nzb'):
                log.log(5, '%s does not seem to be nzb' % entry['title'])
                continue

            if 'file' not in entry:
                log.warning('%s does not have a to get size from' % entry['title'])
                continue

            filename = entry['file']
            log.debug('reading %s' % filename)
            xmldata = file(filename).read()

            try:
                nzbfiles = nzb_parser.parse(xmldata)
            except:
                log.debug('%s is not a valid nzb' % entry['title'])
                continue

            size = 0
            for nzbfile in nzbfiles:
                for segment in nzbfile.segments:
                    size += segment.bytes

            size_mb = size / 1024 / 1024
            log.debug('%s content size: %s MB' % (entry['title'], size_mb))
            entry['content_size'] = size_mb


register_plugin(NzbSize, 'nzb_size', builtin=True)
