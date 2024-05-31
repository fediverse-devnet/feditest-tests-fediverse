from hamcrest import equal_to

from feditest import hard_assert_that, test
from feditest.protocols.webfinger import WebFingerClient, WebFingerServer
from feditest.protocols.webfinger.traffic import WebFingerQueryResponse


@test
def must_only_redirect_to_https(
        client: WebFingerClient,
        server: WebFingerServer
) -> None:
    """
    Test that if the server redirected, the final URL is an HTTPS URL.
    """
    test_id = server.obtain_account_identifier()

    response : WebFingerQueryResponse = client.perform_webfinger_query(test_id)
    hard_assert_that(
            response.http_request_response_pair.final_request.uri.scheme,
            equal_to('https'),
            f'Not https.\n'
            + 'Identifier: "{ test_id }" leads to'
            + f' final request URI { response.http_request_response_pair.final_request.uri.get_uri() }.')
