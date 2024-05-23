from hamcrest import assert_that, equal_to
import urllib

from feditest import test
from feditest.protocols.web.traffic import HttpResponse
from feditest.protocols.webfinger import WebFingerClient, WebFingerServer

@test
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


@test
def requires_valid_resource_uri(
        client: WebFingerClient,
        server: WebFingerServer
) -> None:
    # We use the lower-level API from WebClient because we can't make the WebFingerClient do something invalid
    test_id : str = server.obtain_account_identifier()
    hostname : str = server.hostname

    test_id_no_scheme = test_id.replace("acct:", "")
    malformed_webfinger_uri : str = f"https://{hostname}/.well-known/webfinger?resource={test_id_no_scheme}"

    response : HttpResponse = client.http_get(malformed_webfinger_uri).response
    assert_that(response.http_status, equal_to(400), 'Not HTTP status 400')


@test
def double_equals(
        client: WebFingerClient,
        server: WebFingerServer
) -> None:
    # We use the lower-level API from WebClient because we can't make the WebFingerClient do something invalid

    test_id = server.obtain_account_identifier()
    hostname : str = server.hostname

    malformed_webfinger_uri = f"https://{hostname}/.well-known/webfinger?resource=={urllib.parse.quote(test_id)}"

    response : HttpResponse = client.http_get(malformed_webfinger_uri).response
    assert_that(response.http_status, equal_to(400), 'Not HTTP status 400')
