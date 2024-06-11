from hamcrest import equal_to

from feditest import InteropLevel, SpecLevel, assert_that, test
from feditest.protocols.web.traffic import HttpResponse
from feditest.protocols.webfinger import WebFingerClient, WebFingerServer

@test
def status_404_for_nonexisting_resources(
        client: WebFingerClient,
        server: WebFingerServer
) -> None:
    """
    The server responds with 404 when the resource parameter identifies a non-existent resource.
    """
    test_id = server.obtain_non_existing_account_identifier()

    webfinger_uri = client.construct_webfinger_uri_for(test_id)

    response : HttpResponse = client.http_get(webfinger_uri).response
    assert_that(
            response.http_status,
            equal_to(404),
            f'Not HTTP status 404.\nAccessed URI: "{ webfinger_uri }".',
            spec_Level=SpecLevel.MUST,
            interop_level=InteropLevel.UNAFFECTED)
