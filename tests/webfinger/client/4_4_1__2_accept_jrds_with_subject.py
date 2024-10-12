import json

from feditest import InteropLevel, SpecLevel, assert_that, test
from feditest.protocols.webfinger import WebFingerServer
from feditest.protocols.webfinger.diag import WebFingerDiagClient, WebFingerQueryResponse


@test
def accept_jrds_with_subject(
        client: WebFingerDiagClient,
        server: WebFingerServer
) -> None:

    test_id = server.obtain_account_identifier()

    normal_response : WebFingerQueryResponse = client.diag_perform_webfinger_query(test_id)

    if 'subject' not in normal_response.jrd.subject():
        json_with_subject = json.loads(normal_response.jrd.as_json_string())
        json_with_subject['subject'] = 'acct:foo@example.com'

        with_subject_response = server.override_webfinger_response(
            lambda:
                client.perform_webfinger_query(test_id),
            {
                test_id : json.dumps(json_with_subject)
            }
        )
        assert_that(with_subject_response.jrd.validate(), spec_level=SpecLevel.MUST, interop_level=InteropLevel.PROBLEM)
