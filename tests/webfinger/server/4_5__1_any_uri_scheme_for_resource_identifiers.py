from urllib.parse import quote
from hamcrest import equal_to

from feditest import soft_assert_that, test
from feditest.protocols.web.traffic import HttpResponse
from feditest.protocols.webfinger import WebFingerClient, WebFingerServer


@test
def any_uri_scheme_for_resource_identifiers(
        client: WebFingerClient,
        server: WebFingerServer
) -> None:
    """
    The server must accept resource identifiers provided in the query that use any scheme.
    """
    # We use the lower-level API from WebClient because we can't make the WebFingerClient do something
    # with a scheme it does not understand
    hostname : str = server.hostname

    for test_id in [ 'mailto:abc@def.com', 'foo://' + hostname ]:
        url : str = f"https://{ hostname }/.well-known/webfinger?resource={ quote(test_id) }"

        response : HttpResponse = client.http_get(url).response
        soft_assert_that(
                response.http_status,
                equal_to(404),
                f'Not HTTP status 404.\nAccessed URI: "{ url }".')

