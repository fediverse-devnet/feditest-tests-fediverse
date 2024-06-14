from hamcrest import none

from feditest import InteropLevel, SkipTestException, SpecLevel, assert_that, test
from feditest.protocols.web import WebClient
from feditest.protocols.webfinger import WebFingerClient, WebFingerServer
from feditest.protocols.webfinger.traffic import ClaimedJrd, WebFingerQueryResponse
from feditest.protocols.webfinger.utils import link_subset_or_equal_to, none_except, wf_error
from feditest.reporting import info

# Note: we do not try all the known rel values, only the ones known to be used in a webfinger context
# See also https://fedidevs.org/reference/webfinger/
# Note: these are mostly commented-out as practice shows, it takes a lot of time and finds no issues.

KNOWN_RELS = [ # known to be used in webfinger files
#    'http://a9.com/-/spec/opensearch/1.1/',
#    'http://apinamespace.org/atom',
#    'http://apinamespace.org/twitter',
#    'http://gmpg.org/xfn/11',
#    'http://joindiaspora.com/guid',
#    'http://microformats.org/profile/hcard',
#    'http://openid.net/specs/connect/1.0/issuer',
#    'http://ostatus.org/schema/1.0/subscribe',
#    'http://purl.org/nomad',
#    'http://purl.org/openwebauth/v1',
#    'http://purl.org/openwebauth/v1#redirect',
#    'http://purl.org/zot/protocol/6.0',
#    'http://salmon-protocol.org/ns/salmon-mention',
#    'http://salmon-protocol.org/ns/salmon-replies',
#    'http://schemas.google.com/g/2010#updates-from',
#    'http://specs.openid.net/auth/2.0/provider',
#    'http://webfinger.net/rel/avatar',
#    'http://webfinger.net/rel/blog',
    'http://webfinger.net/rel/profile-page',

#    'describedby',
#    'diaspora-public-key',
#    'magic-public-key',
#    'salmon',
    'self'
]

UNKNOWN_RELS = [ # not known to be used in webfinger files, likely not real
#     'https://webfinger.example/rel/profile-page',
#     'https://webfinger.example/rel/businesscard',
#     'http://example.com/',

    'something-else'
]

@test
def accepts_known_link_rels_in_query(
        client: WebFingerClient,
        server: WebFingerServer
) -> None:
    """
    A server must accept all link rels in the query, even if it does not understand them.
    Tests one known link rel at a time.
    """
    test_id = server.obtain_account_identifier()
    response_without_rel : WebFingerQueryResponse = client.perform_webfinger_query(test_id)
    if ( response_without_rel.exc
         and response_without_rel.exc in (WebClient.WrongContentTypeError, ClaimedJrd.InvalidMediaTypeError, ClaimedJrd.InvalidRelError)
    ):
        raise SkipTestException('Error covered by another test')

    assert_that(
            response_without_rel.exc,
            none(),
            wf_error(response_without_rel),
            spec_level=SpecLevel.MUST,
            interop_level=InteropLevel.PROBLEM)

    for rel in KNOWN_RELS:
        info(f'WebFinger query for resource "{test_id}" with rel "{rel}"')
        response_with_rel : WebFingerQueryResponse = client.perform_webfinger_query(test_id, [rel])
        assert_that(
                response_without_rel.exc,
                none(),
                wf_error(response_with_rel),
                spec_level=SpecLevel.MUST,
                interop_level=InteropLevel.PROBLEM)
        assert_that(
                response_with_rel.jrd,
                link_subset_or_equal_to(response_without_rel.jrd),
                'Not same or subset of links.'
                + f'\nAccessed URI: "{ response_with_rel.http_request_response_pair.request.uri.get_uri() }" with rel { rel } vs none.',
                spec_level=SpecLevel.MUST,
                interop_level=InteropLevel.PROBLEM)


@test
def accepts_unknown_link_rels_in_query(
        client: WebFingerClient,
        server: WebFingerServer
) -> None:
    """
    A server must accept all link rels in the query, even if it does not understand them.
    Tests one unknown link rels at a time.
    """
    test_id = server.obtain_account_identifier()

    response_without_rel = client.perform_webfinger_query(test_id)
    if ( response_without_rel.exc
         and response_without_rel.exc in (WebClient.WrongContentTypeError, ClaimedJrd.InvalidMediaTypeError, ClaimedJrd.InvalidRelError)
    ):
        raise SkipTestException('Error covered by another test')

    assert_that(
            response_without_rel.exc,
            none(),
            wf_error(response_without_rel),
            spec_level=SpecLevel.MUST,
            interop_level=InteropLevel.PROBLEM)

    for rel in UNKNOWN_RELS:
        response_with_rel = client.perform_webfinger_query(test_id, [rel])
        assert_that(
                response_without_rel.exc,
                none(),
                wf_error(response_with_rel),
                spec_level=SpecLevel.MUST,
                interop_level=InteropLevel.PROBLEM)
        assert_that(
                response_with_rel.jrd,
                link_subset_or_equal_to(response_without_rel.jrd),
                'Not same or subset of links.'
                + f'\nAccessed URI: "{ response_with_rel.http_request_response_pair.request.uri.get_uri() }" with rel { rel } vs none.',
                spec_level=SpecLevel.MUST,
                interop_level=InteropLevel.PROBLEM)


@test
def accepts_combined_link_rels_in_query(
        client: WebFingerClient,
        server: WebFingerServer
) -> None:
    """
    A server must accept all link rels in the query, even if it does not understand them.
    Tests several known an unknown link rels at a time.
    """
    test_id = server.obtain_account_identifier()

    response_without_rel = client.perform_webfinger_query(test_id)
    if ( response_without_rel.exc
         and response_without_rel.exc in (WebClient.WrongContentTypeError, ClaimedJrd.InvalidMediaTypeError, ClaimedJrd.InvalidRelError)
    ):
        raise SkipTestException('Error covered by another test')

    assert_that(
            response_without_rel.exc,
            none(),
            wf_error(response_without_rel),
            spec_level=SpecLevel.MUST,
            interop_level=InteropLevel.PROBLEM)

    count = 0
    for rel1 in KNOWN_RELS:
        for rel2 in UNKNOWN_RELS:
            rels = [rel1, rel2] if count % 2 else [rel2, rel1]
            response_with_rel = client.perform_webfinger_query(test_id, rels)
            assert_that(
                    response_without_rel.exc,
                    none(),
                    wf_error(response_with_rel),
                    spec_level=SpecLevel.MUST,
                    interop_level=InteropLevel.PROBLEM)
            assert_that(
                    response_with_rel.jrd,
                    link_subset_or_equal_to(response_without_rel.jrd),
                    'Not same or subset of links.'
                    + f'\nAccessed URI: "{ response_with_rel.http_request_response_pair.request.uri.get_uri() }"'
                    + f' with rels { rels[0] } and { rels[1] } vs none.',
                    spec_level=SpecLevel.MUST,
                    interop_level=InteropLevel.PROBLEM)
            count += 1
