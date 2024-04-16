from hamcrest import assert_that, equal_to
from multidict import MultiDict

from feditest import step
from feditest.protocols.web.traffic import HttpResponse
from feditest.protocols.webfinger import WebFingerClient, WebFingerServer
from feditest.protocols.webfinger.traffic import WebFingerQueryResponse

@step
def follow_redirects(
        client: WebFingerClient,
        server: WebFingerServer
) -> None:

    test_id = server.obtain_existing_account_identifier()
    webfinger_uri = client.construct_webfinger_uri_for(test_id)

    normal_response = client.perform_webfinger_query(test_id)

    # can have any arguments per section 7
    redirect_https_uri = f'https://{ server.hostname() }/foo?abc=def&ghi=jkl'
    redirect_http_uri = f'http://{ server.hostname() }/foo?abc=def&ghi=jkl'

    jrd_headers = MultiDict([('content-type', 'application/jrd+json')])

    overridden_redirect_to_https_response : WebFingerQueryResponse = server.override_http_response( 
            lambda: client.perform_webfinger_query(test_id),
            {
                webfinger_uri : HttpResponse(301,  MultiDict([('location', redirect_https_uri)]).extend(jrd_headers), None ),
                redirect_https_uri : HttpResponse( 200, jrd_headers, normal_response.http_response.payload)
            }
    )
    assert_that(overridden_redirect_to_https_response, equal_to(normal_response))

    overridden_redirect_to_http_response : WebFingerQueryResponse = server.override_http_response( 
            lambda: client.perform_webfinger_query(test_id),
            {
                webfinger_uri : HttpResponse(301, MultiDict([('location', redirect_http_uri)]).extend(jrd_headers), None ),
                redirect_http_uri : HttpResponse( 200, jrd_headers, normal_response.http_response.payload)
            }
    )
    assert_that(not overridden_redirect_to_http_response.validate())
