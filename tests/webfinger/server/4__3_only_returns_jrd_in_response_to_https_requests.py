import ssl

import httpx
from feditest import AssertionFailure, InteropLevel, SpecLevel, assert_that, test
from feditest.protocols.web.traffic import HttpRequest, HttpResponse
from feditest.protocols.webfinger import WebFingerClient, WebFingerServer
from hamcrest import any_of, equal_to, is_not, starts_with


@test
def does_not_return_jrd_in_response_to_http(
        client: WebFingerClient,
        server: WebFingerServer
) -> None:
    """
    Test that a query over HTTP does not produce a JRD.
    """
    test_id = server.obtain_account_identifier()

    correct_webfinger_uri = client.construct_webfinger_uri_for(test_id)
    assert_that(
            correct_webfinger_uri,
            starts_with('https://'),
            f'Incorrect WebFinger URI.',
            spec_level=SpecLevel.MUST,
            interop_level=InteropLevel.PROBLEM)

    http_webfinger_uri = correct_webfinger_uri.replace('https:', 'http:')
    assert(http_webfinger_uri.startswith('http://'))

    http_response : HttpResponse = client.http_get(http_webfinger_uri, follow_redirects=False).response
    assert_that(
            http_response.http_status,
            is_not(equal_to(200)),
            f'HTTP status 200.\nAccessed URI: "{ http_webfinger_uri }".',
            spec_level=SpecLevel.MUST,
            interop_level=InteropLevel.UNAFFECTED) # if a server also responds to http, nothing bad happens
    assert_that(
            http_response.response_headers.get('content-type'),
            is_not(any_of(
                    equal_to('application/jrd+json'),
                    starts_with('application/jrd+json;'))),
            f'Returns JRD content.\nAccessed URI: "{ http_webfinger_uri }".',
            spec_level=SpecLevel.MUST,
            interop_level=InteropLevel.UNAFFECTED) # if a server also responds to http, nothing bad happens


@test
def uses_valid_https_certificate(client: WebFingerClient, server: WebFingerServer):
    account_id = server.obtain_account_identifier()
    webfinger_request = client.construct_webfinger_uri_for(account_id)
    try:
        client.http_get(webfinger_request, verify=True)
    except httpx.ConnectError as ex:
        # Unpack the cause of the exception
        cause = ex
        while cause := getattr(cause, "__cause__", None):
            if isinstance(cause, ssl.SSLCertVerificationError):
                raise AssertionFailure(
                    SpecLevel.MUST,
                    InteropLevel.PROBLEM,
                    'Must use a valid HTTPS certificate.\n'
                    f'Accessed URI: "{ webfinger_request }".',
                )

