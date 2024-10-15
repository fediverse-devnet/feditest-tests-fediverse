from json import JSONDecodeError
from typing import cast

from feditest import AssertionFailure, InteropLevel, SpecLevel, assert_that, test
from feditest.protocols.web.diag import HttpResponse
from feditest.protocols.webfinger import WebFingerServer
from feditest.protocols.webfinger.diag import ClaimedJrd, WebFingerDiagClient
from feditest.protocols.webfinger.utils import construct_webfinger_uri_for
from hamcrest import any_of, equal_to, is_not, starts_with


@test
def requires_resource_uri_http_status(
        client: WebFingerDiagClient,
        server: WebFingerServer
) -> None:
    """
    Do not accept requests with missing resource parameter: HTTP status.
    """
    test_id = server.obtain_account_identifier()

    correct_webfinger_uri = construct_webfinger_uri_for(test_id)
    q = correct_webfinger_uri.find('?resource=')
    assert(q>0) # This is a server-side test, so we don't test the client side here
    uri_without = correct_webfinger_uri[0:q]

    response_without = client.http_get(uri_without).response
    if not response_without:
        raise AssertionFailure(SpecLevel.MUST, InteropLevel.PROBLEM, "No response")

    assert_that(
            response_without.http_status,
            not(equal_to(200)),
            f'HTTP status 200.\nAccessed URI: "{ uri_without }".',
            spec_level=SpecLevel.MUST,
            interop_level=InteropLevel.UNAFFECTED)
    assert_that(
            response_without.http_status,
            equal_to(400),
            f'Not HTTP status 400.\nAccessed URI: "{ uri_without }".',
            spec_level=SpecLevel.MUST,
            interop_level=InteropLevel.UNAFFECTED)


@test
def requires_resource_uri_jrd(
        client: WebFingerDiagClient,
        server: WebFingerServer
) -> None:
    """
    Do not accept requests with missing resource parameter: JRD content.
    """
    test_id = server.obtain_account_identifier()

    correct_webfinger_uri = construct_webfinger_uri_for(test_id)
    q = correct_webfinger_uri.find('?resource=')
    assert(q>0) # This is a server-side test, so we don't test the client side here
    uri_without = correct_webfinger_uri[0:q]

    response_without = client.http_get(uri_without).response
    if not response_without:
        raise AssertionFailure(SpecLevel.MUST, InteropLevel.PROBLEM, "No response")

    content_type = response_without.response_headers.get('content-type', "")
    assert_that(
            content_type,
            is_not( any_of(
                    equal_to('application/jrd+json'),
                    starts_with('application/jrd+json;'))),
            f'Returns JRD content.\nAccessed URI: "{ uri_without }".',
            spec_level=SpecLevel.MUST,
            interop_level=InteropLevel.UNAFFECTED)

    if content_type.startswith('application/json'):
        try :
            payload = cast(bytes, response_without.payload).decode('utf-8')
            ClaimedJrd.create_and_validate(payload)

            assert_that(
                    False,
                    f'Returns JRD content.\nAccessed URI: "{ uri_without }".',
                    spec_level=SpecLevel.MUST,
                    interop_level=InteropLevel.UNKNOWN)

        except ExceptionGroup as exc:
            for e in exc.exceptions:
                if not isinstance(e, (ClaimedJrd.JrdError, JSONDecodeError)):
                    raise exc
            pass # expected
        except ClaimedJrd.JrdError:
            pass # expected
        except JSONDecodeError:
            pass # expected
