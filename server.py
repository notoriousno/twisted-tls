import sys

from twisted.internet import endpoints, reactor, ssl
from twisted.web import server, resource
from twisted.python import log
from twisted.python.modules import getModule


class Echo(resource.Resource):
    isLeaf = True

    def render_GET(self, request):
        return u'Hello World'.encode('ascii')


def old_way():
    """
    Server using older Twisted syntax
    """
    # cert obj from key and cert files
    certificate = ssl.DefaultOpenSSLContextFactory('keys/server.key', 'keys/server.crt')

    # read cert file and then create obj
    #with open('./keys/server.pem') as f:
    #    certData = f.read()
    #certificate = ssl.PrivateCertificate.loadPEM(certData).options()

    factory = server.Site(Echo())
    reactor.listenSSL(8000, factory, certificate, interface='0.0.0.0')


def newer_way():
    """
    Server using new syntax
    """
    # create certificate and server seperatly
    #certificate = ssl.DefaultOpenSSLContextFactory('keys/server.key', 'keys/server.crt')
    #https_server = endpoints.SSL4ServerEndpoint(reactor, 8000, certificate, interface='0.0.0.0')

    # create SSL server from string
    https_server = endpoints.serverFromString(reactor, 'ssl:8000:interface=0.0.0.0:certKey=keys/server.crt:privateKey=keys/server.key')

    # start server
    site = server.Site(Echo())
    https_server.listen(site)


if __name__ == '__main__':
    log.startLogging(sys.stdout)
    old_way()
    #newer_way()
    reactor.run()
