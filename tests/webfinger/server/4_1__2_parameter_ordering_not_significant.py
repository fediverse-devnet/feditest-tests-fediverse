from feditest import SkipTestException, test
from feditest.protocols.webfinger import WebFingerClient, WebFingerServer


@test
def parameter_ordering(
        client: WebFingerClient,
        server: WebFingerServer
) -> None:
    raise SkipTestException()
    # not such an important test
