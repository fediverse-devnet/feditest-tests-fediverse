"""
See annotated WebFinger specification, test 4.2/6
"""

from hamcrest import assert_that
from feditest import step
from feditest.protocols.webfinger import WebFingerClient, WebFingerServer

# We currently have no way of inserting an invalid certificate
# @step
# def client_must_accept_failure_invalid_certificate(
#         client: WebFingerClient,
#         server: WebFingerServer
# -> None:
#


@step
def client_must_accept_failure_4xx(
        client: WebFingerClient,
        server: WebFingerServer
) -> None:
    test_id = server.obtain_non_existing_account_identifier();

    try:
        result = client.perform_webfinger_query_for(test_id)

        assert_that(False, 'Client obtained a response from webfinger query of non-existing account')

    except WebFingerClient.UnknownResourceException as e:
         pass


# We currently have no way of inserting a server fault
# @step
# def client_must_accept_failure_5xx(
#         client: WebFingerClient,
#         server: WebFingerServer
# -> None:
#
