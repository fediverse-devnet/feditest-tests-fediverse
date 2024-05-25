from hamcrest import any_of, equal_to, is_not, starts_with

from feditest import hard_assert_that, test, HardAssertionFailure
from feditest.protocols.webfinger import WebFingerClient, WebFingerServer
from feditest.protocols.webfinger.traffic import WebFingerQueryResponse

from feditest.protocols.webfinger.traffic import ClaimedJrd


@test
def returns_valid_jrd(
        client: WebFingerClient,
        server: WebFingerServer
) -> None:

    test_id = server.obtain_account_identifier()
    webfinger_response : WebFingerQueryResponse = client.perform_webfinger_query(test_id)
    http_response = webfinger_response.http_request_response_pair.response

    hard_assert_that(http_response.http_status, equal_to(200))
    hard_assert_that(http_response.response_headers.get('content-type'),
        any_of(
                equal_to('application/jrd+json'),
                starts_with('application/jrd+json;')))

    try:
        webfinger_response.jrd.validate()
    except ClaimedJrd.JrdError as ex:
        raise HardAssertionFailure(*ex.args[1:])