from feditest import test
from feditest.protocols.webfinger import WebFingerClient, WebFingerServer


@test
def parameter_ordering(
        client: WebFingerClient,
        server: WebFingerServer
) -> None:
    pass # FIXME not such an important test
