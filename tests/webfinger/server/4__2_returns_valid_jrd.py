from hamcrest import any_of, assert_that, equal_to, is_not, starts_with

from feditest import test
from feditest.protocols.web.traffic import HttpResponse
from feditest.protocols.webfinger import WebFingerClient, WebFingerServer

from feditest.protocols.webfinger.traffic import ClaimedJrd

@test
def returns_valid_jrd(
        client: WebFingerClient,
        server: WebFingerServer
) -> None:
    test_id = server.obtain_account_identifier()

    webfinger_uri = client.construct_webfinger_uri_for(test_id)

    # TODO Not sure if this could use perform_webfinger_query ???
    response : HttpResponse = client.http_get(webfinger_uri).response
    assert_that(response.http_status, equal_to(200))
    assert_that(response.response_headers.get('content-type'),
        any_of(
                equal_to('application/jrd+json'),
                starts_with('application/jrd+json;')))

    jrd = ClaimedJrd(response.payload)
    try:
        jrd.validate()
    except ClaimedJrd.JrdError as ex:
        raise AssertionError(*ex.args[1:])