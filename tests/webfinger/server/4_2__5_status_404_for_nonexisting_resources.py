from hamcrest import any_of, equal_to, greater_than_or_equal_to, less_than

from feditest import AssertionFailure, InteropLevel, SpecLevel, assert_that, test
from feditest.protocols.web.diag import HttpResponse
from feditest.protocols.webfinger import WebFingerServer
from feditest.protocols.webfinger.diag import WebFingerDiagClient
from feditest.protocols.webfinger.utils import construct_webfinger_uri_for


@test
def status_404_for_nonexisting_resources(
        client: WebFingerDiagClient,
        server: WebFingerServer
) -> None:
    """
    The server responds with 404 when the resource parameter identifies a non-existent resource.
    """
    test_id = server.obtain_non_existing_account_identifier()

    webfinger_uri = construct_webfinger_uri_for(test_id)
    http_response = client.http_get(webfinger_uri).response

    if not http_response:
        raise AssertionFailure(SpecLevel.MUST, InteropLevel.PROBLEM, "No response")

    assert_that(
            http_response.http_status,
			any_of(
                greater_than_or_equal_to(300),
                less_than(200)),
            f'HTTP status { http_response.http_status }.\nAccessed URI: "{ webfinger_uri }".',
            spec_level=SpecLevel.MUST,
            interop_level=InteropLevel.PROBLEM)

    assert_that(
            http_response.http_status,
            equal_to(404),
            f'Not HTTP status 404.\nAccessed URI: "{ webfinger_uri }".',
            spec_level=SpecLevel.MUST,
            interop_level=InteropLevel.UNAFFECTED)
