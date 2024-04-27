from hamcrest import assert_that

from feditest import step
from feditest.protocols.web.traffic import HttpResponse
from feditest.protocols.webfinger import WebFingerClient, WebFingerServer
from feditest.protocols.webfinger.utils import multi_dict_has_key


@step
def cors_header_required(
        client: WebFingerClient,
        server: WebFingerServer
) -> None:
    test_id = server.obtain_account_identifier()

    response : HttpResponse = client.perform_webfinger_query(test_id).http_request_response_pair.response

    assert_that(response.response_headers, multi_dict_has_key('access-control-allow-origin'))
    # FIXME not checking for a correct value. How?
