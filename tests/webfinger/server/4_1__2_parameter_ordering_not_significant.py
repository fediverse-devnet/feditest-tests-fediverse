from hamcrest import any_of, equal_to, starts_with

from feditest import hard_assert_that, test
from feditest.protocols.web import WebClient
from feditest.protocols.webfinger import WebFingerClient, WebFingerServer
from feditest.protocols.webfinger.traffic import ClaimedJrd
from feditest.protocols.webfinger.utils import none_except, recursive_equal_to, wf_error

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
        hard_assert_that(
                webfinger_response.exc,
                none_except(WebClient.WrongContentTypeError, ClaimedJrd.InvalidMediaTypeError, ClaimedJrd.InvalidRelError),
                wf_error(webfinger_response))

        if i == 0:
            first_webfinger_response = webfinger_response
        else:
            hard_assert_that(
                    webfinger_response.jrd, recursive_equal_to(first_webfinger_response.jrd),
                    f'Response {i} not same.\n'
                    + f'Accessed URIs: "{ webfinger_response.http_request_response_pair.request.uri.get_uri() }"'
                    + f' vs "{ first_webfinger_response.http_request_response_pair.request.uri.get_uri() }".')