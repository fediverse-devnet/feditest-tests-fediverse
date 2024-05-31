from json import JSONDecodeError

from feditest import hard_assert_that, test
from feditest.protocols.web.traffic import HttpResponse
from feditest.protocols.webfinger import WebFingerClient, WebFingerServer
from feditest.protocols.webfinger.traffic import ClaimedJrd
from hamcrest import (
    any_of,
    calling,
    equal_to,
    is_not,
    raises,
    starts_with,
)


@test
def requires_resource_uri_http_status(
        client: WebFingerClient,
        server: WebFingerServer
) -> None:
    """
    Do not accept requests with missing resource parameter: HTTP status.
    """
    test_id = server.obtain_account_identifier()

    correct_webfinger_uri = client.construct_webfinger_uri_for(test_id)
    q = correct_webfinger_uri.find('?resource=')
    assert(q>0)
    uri_without = correct_webfinger_uri[0:q]

    response_without : HttpResponse = client.http_get(uri_without).response
    hard_assert_that(
            response_without.http_status,
            equal_to(400),
            f'Not HTTP status 400.\nAccessed URI: "{ uri_without }".')


@test
def requires_resource_uri_jrd(
        client: WebFingerClient,
        server: WebFingerServer
) -> None:
    """
    Do not accept requests with missing resource parameter: JRD content.
    """
    test_id = server.obtain_account_identifier()

    correct_webfinger_uri = client.construct_webfinger_uri_for(test_id)
    q = correct_webfinger_uri.find('?resource=')
    assert(q>0)
    uri_without = correct_webfinger_uri[0:q]

    response_without : HttpResponse = client.http_get(uri_without).response

    content_type = response_without.response_headers.get('content-type', "")
    hard_assert_that(
            content_type,
            is_not( any_of(
                    equal_to('application/jrd+json'),
                    starts_with('application/jrd+json;'))),
            f'Returns JRD content.\nAccessed URI: "{ uri_without }".')

    if content_type.startswith('application/json'):
        hard_assert_that(
                calling(lambda: ClaimedJrd.create_and_validate(response_without.payload)),
                any_of( raises(RuntimeError),
                        raises(JSONDecodeError)),
                f'Returns JRD content.\nAccessed URI: "{ uri_without }".')
