from feditest import InteropLevel, SpecLevel, assert_that, test
from feditest.protocols.web.diag import HttpResponse
from feditest.protocols.webfinger import WebFingerServer
from feditest.protocols.webfinger.diag import WebFingerDiagClient
from feditest.protocols.webfinger.diag import WebFingerQueryDiagResponse
from hamcrest import equal_to
from multidict import MultiDict


@test
def follow_redirects(
        client: WebFingerDiagClient,
        server: WebFingerServer
) -> None:

    test_id = server.obtain_account_identifier()
    webfinger_uri = client.construct_webfinger_uri_for(test_id)
    hostname = server.hostname

    normal_response = client.perform_webfinger_query(test_id)

    # can have any arguments per section 7
    redirect_https_uri = f'https://{ hostname }/foo?abc=def&ghi=jkl'
    redirect_http_uri = f'http://{ hostname }/foo?abc=def&ghi=jkl'

    jrd_headers = MultiDict([('content-type', 'application/jrd+json')])

    overridden_redirect_to_https_response : WebFingerQueryDiagResponse = server.override_http_response(
            lambda: client.perform_webfinger_query(test_id),
            {
                webfinger_uri : HttpResponse(301,  MultiDict([('location', redirect_https_uri)]).extend(jrd_headers), None ),
                redirect_https_uri : HttpResponse( 200, jrd_headers, normal_response.http_request_response_pair.response.payload)
            }
    )
    assert_that(overridden_redirect_to_https_response, equal_to(normal_response), spec_level=SpecLevel.MUST, interop_level=InteropLevel.PROBLEM)

    overridden_redirect_to_http_response : WebFingerQueryDiagResponse = server.override_http_response(
            lambda: client.perform_webfinger_query(test_id),
            {
                webfinger_uri : HttpResponse(301, MultiDict([('location', redirect_http_uri)]).extend(jrd_headers), None ),
                redirect_http_uri : HttpResponse( 200, jrd_headers, normal_response.http_request_response_pair.response.payload)
            }
    )
    assert_that(not overridden_redirect_to_http_response.validate(), spec_level=SpecLevel.MUST, interop_level=InteropLevel.PROBLEM)
