from hamcrest import any_of, equal_to, starts_with

from feditest import SkipTestException, hard_assert_that, test
from feditest.protocols.webfinger import WebFingerClient, WebFingerServer

RELS = [
    'http://webfinger.net/rel/profile-page',
    'something-else',
    'self'
]

@test
def parameter_ordering(
        client: WebFingerClient,
        server: WebFingerServer
) -> None:
    """
    Parameter ordering is not significant.
    """
    test_id = server.obtain_account_identifier()

    first_webfinger_response = None
    for i in range(0, len(RELS)):
        rels = RELS[i:] + RELS[0:i]
        webfinger_response = client.perform_webfinger_query(test_id, rels)

        hard_assert_that(webfinger_response.http_request_response_pair.response.http_status, equal_to(200), 'Not HTTP status 200')
        hard_assert_that(webfinger_response.http_request_response_pair.response.response_headers.get('content-type'),
            any_of(
                equal_to('application/jrd+json'),
                starts_with('application/jrd+json;')),
            'Not content of type JRD')

        if i == 0:
            first_webfinger_response = webfinger_response
        else:
            hard_assert_that(webfinger_response, equal_to(first_webfinger_response), f'Response {i} not same as 1st')

