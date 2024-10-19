from feditest import InteropLevel, SpecLevel, assert_that, test
from feditest.protocols.webfinger import WebFingerServer
from feditest.protocols.webfinger.diag import WebFingerDiagClient
from feditest.protocols.webfinger.utils import wf_error
from hamcrest import none, not_none


@test
def normal_query(
        client: WebFingerDiagClient,
        server: WebFingerServer
) -> None:
    """
    Perform a normal, simple query on an existing account.
    """
    test_id = server.obtain_account_identifier()

    webfinger_response = client.diag_perform_webfinger_query(test_id)

    assert_that(
            webfinger_response.exc,
            none(),
            wf_error(webfinger_response),
            spec_level=SpecLevel.MUST,
            interop_level=InteropLevel.PROBLEM)

    assert_that(
            webfinger_response.jrd,
            not_none(),
            wf_error(webfinger_response),
            spec_level=SpecLevel.MUST,
            interop_level=InteropLevel.PROBLEM)

    try:
        webfinger_response.jrd.validate() # type: ignore [union-attr]

    except Exception as e:
        assert_that(False, wf_error(webfinger_response), spec_level=SpecLevel.MUST, interop_level=InteropLevel.PROBLEM)

