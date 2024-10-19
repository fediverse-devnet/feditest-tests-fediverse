from feditest import InteropLevel, SpecLevel, assert_that, test
from feditest.protocols.web.diag import HttpResponse
from feditest.protocols.webfinger import WebFingerClient, WebFingerServer
from feditest.utils import uri_parse_validate, ParsedUri
from hamcrest import all_of, equal_to, is_not


@test
def only_https_requests(
        client: WebFingerClient,
        server: WebFingerServer
) -> None:
    test_ids = [ server.obtain_account_identifier() ]

    responses : list[HttpResponse] = server.transaction(
            lambda:[ client.perform_webfinger_query(test_id) for test_id in test_ids ]
    ).entries()

    assert(len(responses) == len(test_ids))
    for i in range(0, len(responses)):
        response = responses[i]
        test_id = test_ids[i]

        assert_that(response.request.uri.scheme, equal_to('https'), SpecLevel.MUST, InteropLevel.UNKNOWN)
        assert_that(response.request.uri.query, all_of(is_not(None), is_not('')), SpecLevel.MUST, InteropLevel.PROBLEM)
        assert_that(response.request.uri.has_param('resource'), SpecLevel.MUST, InteropLevel.PROBLEM)
        assert_that(uri_parse_validate(response.request.uri.param_single('resource')), SpecLevel.MUST, InteropLevel.PROBLEM)

        parsed_test_id = ParsedUri.parse(test_id)
        assert_that(response.request.uri.netloc, equal_to(parsed_test_id.netloc), SpecLevel.MUST, InteropLevel.PROBLEM)
        assert_that(response.request.uri.path, equal_to('/.well-known/webfinger'), SpecLevel.MUST, InteropLevel.PROBLEM)

