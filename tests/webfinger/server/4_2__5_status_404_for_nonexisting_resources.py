from hamcrest import assert_that, equal_to

from feditest import step
from feditest.protocols.web.traffic import HttpResponse
from feditest.protocols.webfinger import WebFingerClient, WebFingerServer

@step
def status_404_for_nonexisting_resources(
        client: WebFingerClient,
        server: WebFingerServer
) -> None:
    test_id = server.obtain_non_existing_account_identifier()

    webfinger_uri = client.construct_webfinger_uri_for(test_id)

    response : HttpResponse = client.http_get(webfinger_uri).response
    assert_that(response.http_status, equal_to(404))
