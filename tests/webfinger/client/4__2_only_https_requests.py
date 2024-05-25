from hamcrest import any_of, equal_to, is_not, all_of

from feditest import hard_assert_that, test
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

    assert(len(responses) == len(test_ids))
    for i in range(0, len(responses)):
        response = responses[i]
        test_id = test_ids[i]

        hard_assert_that(response.request.uri.scheme, equal_to('https'))
        hard_assert_that(response.request.uri.query, all_of(is_not(None), is_not('')))
        hard_assert_that(response.request.uri.has_param('resource'))
        hard_assert_that(uri_parse_validate(response.request.uri.param_single('resource')))

        parsed_test_id = ParsedUri.parse(test_id)
        hard_assert_that(response.request.uri.netloc, equal_to(parsed_test_id.netloc))
        hard_assert_that(response.request.uri.path, equal_to('/.well-known/webfinger'))

