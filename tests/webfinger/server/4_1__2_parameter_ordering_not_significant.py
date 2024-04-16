from feditest import step
from feditest.protocols.webfinger import WebFingerClient, WebFingerServer

@step
def parameter_ordering(
        client: WebFingerClient,
        server: WebFingerServer
) -> None:
    pass # FIXME not such an important test
