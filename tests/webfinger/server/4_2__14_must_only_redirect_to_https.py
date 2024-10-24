from feditest import InteropLevel, SpecLevel, assert_that, test
from feditest.protocols.webfinger import WebFingerServer
from feditest.protocols.webfinger.diag import WebFingerDiagClient, WebFingerQueryDiagResponse
from hamcrest import equal_to


@test
def must_only_redirect_to_https(
        client: WebFingerDiagClient,
        server: WebFingerServer
) -> None:
    """
    Test that if the server redirected, the final URL is an HTTPS URL.
    """
    test_id = server.obtain_account_identifier()

    response : WebFingerQueryDiagResponse = client.diag_perform_webfinger_query(test_id)
    assert_that(
            response.http_request_response_pair.final_request.parsed_uri.scheme,
            equal_to('https'),
            f'Not https.\n'
            + 'Identifier: "{ test_id }" leads to'
            + f' final request URI { response.http_request_response_pair.final_request.parsed_uri.uri }.',
            spec_level=SpecLevel.MUST,
            interop_level=InteropLevel.PROBLEM)
