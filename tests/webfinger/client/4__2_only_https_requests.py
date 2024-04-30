from hamcrest import any_of, assert_that, equal_to, is_not, all_of

from feditest import test
from feditest.utils import uri_parse_validate
from feditest.protocols.web.traffic import HttpResponse, ParsedUri
from feditest.protocols.webfinger import WebFingerClient, WebFingerServer

@test
def only_https_requests(
        client: WebFingerClient,
        server: WebFingerServer
) -> None:
    test_ids =[ server.obtain_account_identifier() ]

    responses : list[HttpResponse] = server.transaction(
            lambda:[ client.perform_webfinger_query(test_id) for test_id in test_ids ]
    ).entries()

    assert_that(len(responses), equal_to(len(test_ids)))
    for i in range(0, len(responses)):
        response = responses[i]
        test_id = test_ids[i]

        assert_that(response.request.uri.scheme, equal_to('https'))
        assert_that(response.request.uri.query, all_of(is_not(None), is_not('')))
        assert_that(response.request.uri.has_param('resource'))
        assert_that(uri_parse_validate(response.request.uri.param_single('resource')))

        parsed_test_id = ParsedUri.parse(test_id)
        assert_that(response.request.uri.netloc, equal_to(parsed_test_id.netloc))
        assert_that(response.request.uri.path, equal_to('/.well-known/webfinger'))

