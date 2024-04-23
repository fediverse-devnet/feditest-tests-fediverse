from urllib.parse import quote
from hamcrest import assert_that, equal_to

from feditest import step
from feditest.protocols.web.traffic import HttpResponse
from feditest.protocols.webfinger import WebFingerClient, WebFingerServer

@step
def any_uri_scheme_for_resource_identifiers(
        client: WebFingerClient,
        server: WebFingerServer
) -> None:
    # We use the lower-level API from WebClient because we can't make the WebFingerClient do something
    # with a scheme it does not understand
    hostname : str = server.hostname

    for test_id in [ 'mailto:abc@def.com', 'foo://' + hostname ]:
        url : str = f"https://{ hostname }/.well-known/webfinger?resource={ quote(test_id) }"

        response : HttpResponse = client.http_get(url).response
        assert_that(response.http_status, equal_to(404), 'Not HTTP status 404')

