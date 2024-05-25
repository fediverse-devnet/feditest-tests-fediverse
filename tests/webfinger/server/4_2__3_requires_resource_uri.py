from feditest import hard_assert_that, test
from feditest.protocols.web.traffic import HttpResponse
from feditest.protocols.webfinger import WebFingerClient, WebFingerServer
from feditest.protocols.webfinger.traffic import ClaimedJrd
from hamcrest import (
    any_of,
    calling,
    equal_to,
    greater_than_or_equal_to,
    is_not,
    raises,
    starts_with,
)


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
    q = correct_webfinger_uri.find('?resource=')
    hard_assert_that(q, greater_than_or_equal_to(0))
    uri_without = correct_webfinger_uri[0:q]

    response_without : HttpResponse = client.http_get(uri_without).response
    hard_assert_that(response_without.http_status, equal_to(400))
    content_type = response_without.response_headers.get('content-type', "")
    hard_assert_that(content_type,
        is_not(any_of(
                equal_to('application/jrd+json'),
                starts_with('application/jrd+json;'))))
    if "application/json" in content_type:
        hard_assert_that(calling( lambda: interpret_payload_as_jrd(response_without.payload)), raises(RuntimeError))

