from json import JSONDecodeError
from typing import cast
import urllib

from hamcrest import all_of, equal_to, greater_than_or_equal_to, less_than

from feditest import AssertionFailure, InteropLevel, SpecLevel, assert_that, test
from feditest.protocols.web.diag import HttpResponse
from feditest.protocols.webfinger import WebFingerServer
from feditest.protocols.webfinger.diag import ClaimedJrd, WebFingerDiagClient


@test
def requires_valid_resource_uri_http_status(
        client: WebFingerDiagClient,
        server: WebFingerServer
) -> None:
    """
    Do not accept malformed resource parameters. Test HTTP status for missing acct: scheme.
    """
    # We use the lower-level API from WebClient because we can't make the WebFingerDiagClient do something invalid
    test_id : str = server.obtain_account_identifier()
    hostname : str = server.hostname

    test_id_no_scheme = test_id.replace("acct:", "")
    malformed_webfinger_uri : str = f"https://{hostname}/.well-known/webfinger?resource={test_id_no_scheme}"

    response = client.http_get(malformed_webfinger_uri).response
    if not response:
        raise AssertionFailure(SpecLevel.MUST, InteropLevel.PROBLEM, "No response")

    assert_that(
            response.http_status,
			all_of(
                greater_than_or_equal_to(400),
                less_than(500)),
			f'Not HTTP status 4xx.\nAccessed URI: "{ malformed_webfinger_uri }".',
            spec_level=SpecLevel.MUST,
            interop_level=InteropLevel.UNAFFECTED)
    assert_that(
            response.http_status,
            equal_to(400),
            f'Not HTTP status 400\nAccessed URI: "{ malformed_webfinger_uri }".',
            spec_level=SpecLevel.MUST,
            interop_level=InteropLevel.UNAFFECTED)


@test
def requires_valid_resource_uri_jrd(
        client: WebFingerDiagClient,
        server: WebFingerServer
) -> None:
    """
    Do not accept malformed resource parameters. Test JRD content for missing acct: scheme.
    """
    # We use the lower-level API from WebClient because we can't make the WebFingerDiagClient do something invalid
    test_id : str = server.obtain_account_identifier()
    hostname : str = server.hostname

    test_id_no_scheme = test_id.replace("acct:", "")
    malformed_webfinger_uri : str = f"https://{hostname}/.well-known/webfinger?resource={test_id_no_scheme}"

    response = client.http_get(malformed_webfinger_uri).response
    if not response:
        raise AssertionFailure(SpecLevel.MUST, InteropLevel.PROBLEM, "No response")

    try: # don't use the pyhamcrest any_of(raises, raises) because the error message is incomprehensible
        payload = cast(bytes, response.payload).decode('utf-8')
        ClaimedJrd.create_and_validate(payload)

        assert_that(
                False,
                f'Returns JRD content.\nAccessed URI: "{ malformed_webfinger_uri }".',
                spec_level=SpecLevel.MUST,
                interop_level=InteropLevel.UNAFFECTED)

    except ExceptionGroup as exc:
        for e in exc.exceptions:
            if not isinstance(e, (RuntimeError, JSONDecodeError)):
                raise exc
        pass # expected
    except RuntimeError:
        pass # expected
    except JSONDecodeError:
        pass # expected


@test
def double_equals_http_status(
        client: WebFingerDiagClient,
        server: WebFingerServer
) -> None:
    """
    Do not accept malformed resource parameters. Test HTTP status for inserting an extra = character.
    """
    # We use the lower-level API from WebClient because we can't make the WebFingerClient do something invalid
    test_id = server.obtain_account_identifier()
    hostname : str = server.hostname

    malformed_webfinger_uri = f"https://{hostname}/.well-known/webfinger?resource=={urllib.parse.quote(test_id)}"

    response = client.http_get(malformed_webfinger_uri).response
    if not response:
        raise AssertionFailure(SpecLevel.MUST, InteropLevel.PROBLEM, "No response")

    assert_that(
            response.http_status,
			all_of(
                greater_than_or_equal_to(400),
                less_than(500)),
			f'Not HTTP status 4xx.\nAccessed URI: "{ malformed_webfinger_uri }".',
            spec_level=SpecLevel.MUST,
            interop_level=InteropLevel.UNAFFECTED)
    assert_that(
            response.http_status,
            equal_to(400),
            f'Not HTTP status 400\nAccessed URI: "{ malformed_webfinger_uri }".',
            spec_level=SpecLevel.MUST,
            interop_level=InteropLevel.UNAFFECTED)


@test
def double_equals_jrd(
        client: WebFingerDiagClient,
        server: WebFingerServer
) -> None:
    """
    Do not accept malformed resource parameters. Test JRD content for inserting an extra = character.
    """
    # We use the lower-level API from WebClient because we can't make the WebFingerClient do something invalid
    test_id = server.obtain_account_identifier()
    hostname : str = server.hostname

    malformed_webfinger_uri = f"https://{hostname}/.well-known/webfinger?resource=={urllib.parse.quote(test_id)}"

    response = client.http_get(malformed_webfinger_uri).response
    if not response:
        raise AssertionFailure(SpecLevel.MUST, InteropLevel.PROBLEM, "No response")

    try: # don't use the pyhamcrest any_of(raises, raises) because the error message is incomprehensible
        payload = cast(bytes, response.payload).decode('utf-8')
        ClaimedJrd.create_and_validate(payload)

        assert_that(
                False,
                f'Returns JRD content.\nAccessed URI: "{ malformed_webfinger_uri }".',
                spec_level=SpecLevel.MUST,
                interop_level=InteropLevel.UNAFFECTED)

    except ExceptionGroup as exc:
        for e in exc.exceptions:
            if not isinstance(e, (RuntimeError, JSONDecodeError)):
                raise exc
        pass # expected
    except RuntimeError:
        pass # expected
    except JSONDecodeError:
        pass # expected
