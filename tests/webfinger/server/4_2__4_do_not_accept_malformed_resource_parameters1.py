from hamcrest import assert_that, equal_to
import urllib

from feditest import step
from feditest.protocols.web.traffic import HttpResponse
from feditest.protocols.webfinger import WebFingerClient, WebFingerServer

@step
def not_percent_encoded(
        client: WebFingerClient,
        server: WebFingerServer
) -> None:
    # We use the lower-level API from WebClient because we can't make the WebFingerClient do something invalid
    test_id : str = server.obtain_account_identifier()
    hostname : str = server.hostname

    malformed_webfinger_uri : str = f"https://{hostname}/.well-known/webfinger?resource={test_id}"

    response : HttpResponse = client.http_get(malformed_webfinger_uri).response
    assert_that(response.http_status, equal_to(400), 'Not HTTP status 400')
