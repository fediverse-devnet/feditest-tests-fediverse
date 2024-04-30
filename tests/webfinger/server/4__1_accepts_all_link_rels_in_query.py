from hamcrest import assert_that, equal_to

from feditest import test
from feditest.protocols.webfinger import WebFingerClient, WebFingerServer
from feditest.protocols.webfinger.traffic import WebFingerQueryResponse
from feditest.protocols.webfinger.utils import link_subset_or_equal_to
from feditest.reporting import info

# Note: we do not try all the known rel values, only the ones known to be used in a webfinger context
# See also https://fedidevs.org/reference/webfinger/

KNOWN_RELS = ( # known to be used in webfinger files
#    'http://a9.com/-/spec/opensearch/1.1/',
#    'http://apinamespace.org/atom',
#    'http://apinamespace.org/twitter',
#    'http://gmpg.org/xfn/11',
    'http://joindiaspora.com/guid',
    'http://microformats.org/profile/hcard',
    'http://openid.net/specs/connect/1.0/issuer',
    'http://ostatus.org/schema/1.0/subscribe',
    'http://purl.org/nomad',
    'http://purl.org/openwebauth/v1',
    'http://purl.org/openwebauth/v1#redirect',
    'http://purl.org/zot/protocol/6.0',
#    'http://salmon-protocol.org/ns/salmon-mention',
#    'http://salmon-protocol.org/ns/salmon-replies',
#    'http://schemas.google.com/g/2010#updates-from',
#    'http://specs.openid.net/auth/2.0/provider',
#    'http://webfinger.net/rel/avatar',
    'http://webfinger.net/rel/blog',
    'http://webfinger.net/rel/profile-page',

    'describedby',
    'diaspora-public-key',
    'magic-public-key',
#    'salmon',
    'self'
)

UNKNOWN_RELS = ( # not known to be used in webfinger files, likely not real
    'https://webfinger.example/rel/profile-page',
#    'https://webfinger.example/rel/businesscard',
    'http://example.com/',

    'something-else'
)

@test
def accepts_known_link_rels_in_query(
        client: WebFingerClient,
        server: WebFingerServer
) -> None:
    test_id = server.obtain_account_identifier()
    response_without_rel : WebFingerQueryResponse = client.perform_webfinger_query(test_id)
    for rel in KNOWN_RELS:
        info(f'WebFinger query for resource "{test_id}" with rel "{rel}"')
        response_with_rel : WebFingerQueryResponse = client.perform_webfinger_query(test_id, [rel])
        assert_that(response_with_rel.http_request_response_pair.response.http_status, equal_to(200))
        assert_that(response_with_rel.jrd, link_subset_or_equal_to(response_without_rel.jrd))


@test
def accepts_unknown_link_rels_in_query(
        client: WebFingerClient,
        server: WebFingerServer
) -> None:
    test_id = server.obtain_account_identifier()

    response_without_rel = client.perform_webfinger_query(test_id)
    for rel in UNKNOWN_RELS:
        response_with_rel = client.perform_webfinger_query(test_id, [rel])
        assert_that(response_with_rel.http_request_response_pair.response.http_status, equal_to(200))
        assert_that(response_with_rel.jrd, link_subset_or_equal_to(response_without_rel.jrd))


@test
def accepts_combined_link_rels_in_query(
        client: WebFingerClient,
        server: WebFingerServer
) -> None:
    test_id = server.obtain_account_identifier()

    response_without_rel = client.perform_webfinger_query(test_id)
    count = 0
    for rel1 in KNOWN_RELS:
        for rel2 in UNKNOWN_RELS:
            rels = [rel1, rel2] if count % 2 else [rel2, rel1]
            response_with_rel = client.perform_webfinger_query(test_id, rels)
            assert_that(response_with_rel.http_request_response_pair.response.http_status, equal_to(200))
            assert_that(response_with_rel.jrd, link_subset_or_equal_to(response_without_rel.jrd))
            ++count
