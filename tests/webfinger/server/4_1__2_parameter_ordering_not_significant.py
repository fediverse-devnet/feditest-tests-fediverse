from feditest import AssertionFailure, InteropLevel, SpecLevel, assert_that, test
from feditest.protocols import SkipTestException
from feditest.protocols.web import WebClient
from feditest.protocols.webfinger import WebFingerClient, WebFingerServer
from feditest.protocols.webfinger.traffic import ClaimedJrd
from feditest.protocols.webfinger.utils import none_except, recursive_equal_to, wf_error
from hamcrest import none

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
        webfinger_response = client.perform_webfinger_query(test_id, rels=rels)

        if webfinger_response.exc:
            raise AssertionFailure(
                    spec_level=SpecLevel.MUST,
                    interop_level=InteropLevel.PROBLEM,
                    msg=wf_error(webfinger_response))

        if i == 0:
            first_webfinger_response = webfinger_response
        else:
            assert_that(
                    webfinger_response.jrd, recursive_equal_to(first_webfinger_response.jrd),
                    f'Response {i} not same.\n'
                    + f'Accessed URIs: "{ webfinger_response.http_request_response_pair.request.uri.get_uri() }"'
                    + f' vs "{ first_webfinger_response.http_request_response_pair.request.uri.get_uri() }".',
                    spec_level=SpecLevel.MUST,
                    interop_level=InteropLevel.PROBLEM)
