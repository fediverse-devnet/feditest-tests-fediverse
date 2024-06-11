from hamcrest import any_of, equal_to, is_not, starts_with

from feditest import InteropLevel, SpecLevel, assert_that, test
from feditest.protocols.web.traffic import HttpResponse
from feditest.protocols.webfinger import WebFingerClient, WebFingerServer

@test
def returns_jrd_in_response_to_https(
        client: WebFingerClient,
        server: WebFingerServer
) -> None:
    """
    Test that a query over HTTPS produces a JRD.
    """
    test_id = server.obtain_account_identifier()

    correct_webfinger_uri = client.construct_webfinger_uri_for(test_id)
    assert_that(
            correct_webfinger_uri,
            starts_with('https://'),
            spec_Level=SpecLevel.MUST,
            interop_level=InteropLevel.PROBLEM)

    correct_https_response : HttpResponse = client.http_get(correct_webfinger_uri).response
    assert_that(
            correct_https_response.http_status,
            equal_to(200),
            f'Not HTTP status 200.\nAccessed URI: "{ correct_webfinger_uri }".',
            spec_Level=SpecLevel.MUST,
            interop_level=InteropLevel.PROBLEM)
    assert_that(
            correct_https_response.response_headers.get('content-type'),
            any_of(
                    equal_to('application/jrd+json'),
                    starts_with('application/jrd+json;')),
            f'Wrong content type.\nAccessed URI: "{ correct_webfinger_uri }".',
            spec_Level=SpecLevel.MUST,
            interop_level=InteropLevel.PROBLEM)
