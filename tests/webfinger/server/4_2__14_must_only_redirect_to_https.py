from hamcrest import assert_that, equal_to

from feditest import step
from feditest.protocols.webfinger import WebFingerClient, WebFingerServer
from feditest.protocols.webfinger.traffic import WebFingerQueryResponse


@step
def must_only_redirect_to_https(
        client: WebFingerClient,
        server: WebFingerServer
) -> None:
    test_id = server.obtain_account_identifier()

    response : WebFingerQueryResponse = client.perform_webfinger_query(test_id)
    assert_that(response.http_request_response_pair.final_request.uri.scheme, equal_to('https'))
