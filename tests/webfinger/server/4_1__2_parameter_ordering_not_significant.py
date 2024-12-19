from typing import cast

from hamcrest import empty

from feditest import InteropLevel, SpecLevel, assert_that, test
from feditest.protocols.webfinger import WebFingerServer
from feditest.protocols.webfinger.diag import ClaimedJrd, WebFingerDiagClient, WebFingerQueryDiagResponse
from feditest.protocols.webfinger.utils import no_exception_other_than, recursive_equal_to, wf_error

RELS = [
    'http://webfinger.net/rel/profile-page',
    'something-else',
    'self'
]

IGNORED_EXCEPTIONS = [ WebFingerDiagClient.WrongContentTypeError, ClaimedJrd.InvalidMediaTypeError, ClaimedJrd.InvalidRelError ]
""" These exceptions are not to be reported in this test as they are covered elsewhere."""


@test
def parameter_ordering(
        client: WebFingerDiagClient,
        server: WebFingerServer
) -> None:
    """
    Parameter ordering is not significant.
    """
    test_id = server.obtain_account_identifier()

    first_webfinger_response = None
    for i in range(0, len(RELS)):
        rels = RELS[i:] + RELS[0:i]
        webfinger_response = client.diag_perform_webfinger_query(test_id, rels=rels)
        assert_that(
            webfinger_response.exceptions,
            no_exception_other_than(IGNORED_EXCEPTIONS),
            wf_error(webfinger_response),
            spec_level=SpecLevel.MUST,
            interop_level=InteropLevel.PROBLEM)

        if i == 0:
            first_webfinger_response = webfinger_response
        else:
            first_webfinger_response_not_none = cast(WebFingerQueryDiagResponse, first_webfinger_response)
            assert_that(
                    webfinger_response.jrd, recursive_equal_to(first_webfinger_response_not_none.jrd),
                    f'Response {i} not same.\n'
                    + f'Accessed URIs: "{ webfinger_response.http_request_response_pair.request.parsed_uri.uri }"'
                    + f' vs "{ first_webfinger_response_not_none.http_request_response_pair.request.parsed_uri.uri }".',
                    spec_level=SpecLevel.MUST,
                    interop_level=InteropLevel.PROBLEM)
