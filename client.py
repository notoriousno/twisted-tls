import treq
from twisted.internet import defer, ssl, task
from twisted.web import client, iweb
from zope.interface import implementer


@implementer(iweb.IPolicyForHTTPS)
class OneTrust(object):
    """
    Custom Policy class that's regularly used in tutorials
    """

    def __init__(self, root_cert):
        self.root = root_cert

    def creatorForNetloc(self, host, port):
        return ssl.optionsForClientTLS(host.decode('ascii'), self.root)


@task.react
@defer.inlineCallbacks
def custom_trust(_reactor):
    # get root cert from pem file
    with open('keys/server.crt') as cert_file:
        trust_root = yield ssl.Certificate.loadPEM(cert_file.read())

    # ready made browser-like policy
    policy = client.BrowserLikePolicyForHTTPS(trustRoot=trust_root)

    # using custom policy class
    #policy = OneTrust(trust_root)

    agent = client.Agent(_reactor, policy)
    treqish = treq.client.HTTPClient(agent)

    response = yield treqish.get('https://localhost:8000')
    content = yield response.content()
    print(content)
