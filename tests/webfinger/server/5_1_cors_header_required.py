from feditest import InteropLevel, SpecLevel, assert_that, test
from feditest.protocols.webfinger import WebFingerServer
from feditest.protocols.webfinger.diag import WebFingerDiagClient


@test
def cors_header_required(
        client: WebFingerDiagClient,
        server: WebFingerServer
) -> None:
    """
    The server must provide a valid value for HTTP Header "Access-Control-Allow-Origin".
    """
    test_id = server.obtain_account_identifier()

    pair = client.diag_perform_webfinger_query(test_id).http_request_response_pair

    assert_that(
            'access-control-allow-origin' in pair.response.response_headers,
            f'Missing CORS header.\nAccessed URI: "{ pair.request.uri.get_uri() }".\nNot present: "access-control-allow-origin".',
            spec_level=SpecLevel.MUST,
            interop_level=InteropLevel.PROBLEM)
    # FIXME not checking for a correct value. How?
