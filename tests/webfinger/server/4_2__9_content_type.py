from hamcrest import any_of, equal_to, is_not, starts_with

from feditest import InteropLevel, SpecLevel, assert_that, test
from feditest.protocols.web.diag import HttpResponse
from feditest.protocols.webfinger import WebFingerServer
from feditest.protocols.webfinger.diag import WebFingerDiagClient
from feditest.protocols.webfinger.utils import construct_webfinger_uri_for


@test
def returns_jrd_in_response_to_https(
        client: WebFingerDiagClient,
        server: WebFingerServer
) -> None:
    """
    Test that a query over HTTPS produces a JRD.
    """
    test_id = server.obtain_account_identifier()

    correct_webfinger_uri = construct_webfinger_uri_for(test_id)
    assert(correct_webfinger_uri.startswith('https://')) # This is a server-side test, we are not testing the client

    correct_https_response : HttpResponse = client.http_get(correct_webfinger_uri).response
    assert_that(
            correct_https_response.http_status,
            equal_to(200),
            f'Not HTTP status 200.\nAccessed URI: "{ correct_webfinger_uri }".',
            spec_level=SpecLevel.MUST,
            interop_level=InteropLevel.PROBLEM)

    assert_that(
            correct_https_response.response_headers.get('content-type'),
            any_of(
                    equal_to('application/jrd+json'),
                    starts_with('application/jrd+json;'),
                    starts_with('application/xml')),
            f'Wrong content type.\nAccessed URI: "{ correct_webfinger_uri }".',
            spec_level=SpecLevel.MUST,
            interop_level=InteropLevel.PROBLEM)

    assert_that(
            correct_https_response.response_headers.get('content-type'),
            any_of(
                    equal_to('application/jrd+json'),
                    starts_with('application/jrd+json;')),
            f'Wrong content type.\nAccessed URI: "{ correct_webfinger_uri }".',
            spec_level=SpecLevel.MUST,
            interop_level=InteropLevel.DEGRADED)
