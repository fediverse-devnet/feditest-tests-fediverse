from hamcrest import any_of, assert_that, calling, equal_to, greater_than_or_equal_to, is_not, starts_with, raises

from feditest import test
from feditest.protocols.web.traffic import HttpResponse
from feditest.protocols.webfinger import WebFingerClient, WebFingerServer
from feditest.protocols.webfinger.traffic import ClaimedJrd

def interpret_payload_as_jrd(payload: str):
    """
    Helper
    """
    jrd = ClaimedJrd(payload)
    jrd.validate()


@test
def requires_resource_uri(
        client: WebFingerClient,
        server: WebFingerServer
) -> None:
    test_id = server.obtain_account_identifier()

    correct_webfinger_uri = client.construct_webfinger_uri_for(test_id)
    q = correct_webfinger_uri.index('?resource=')
    assert_that(q, greater_than_or_equal_to(0))
    uri_without = correct_webfinger_uri[0:q]

    response_without : HttpResponse = client.http_get(uri_without).response
    assert_that(response_without.http_status, equal_to(400))
    assert_that(response_without.response_headers['content-type'],
        is_not(any_of(
                equal_to('application/jrd+json'),
                starts_with('application/jrd+json;'))))
    if "application/json" in response_without.response_headers.get('content-type', ""):
        assert_that(calling( lambda: interpret_payload_as_jrd(response_without.payload_as_string())), raises(RuntimeError))

