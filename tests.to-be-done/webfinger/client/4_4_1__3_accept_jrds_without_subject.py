import json

from feditest import InteropLevel, SpecLevel, assert_that, test
from feditest.protocols.webfinger import WebFingerServer
from feditest.protocols.webfinger.diag import WebFingerDiagClient, WebFingerQueryDiagResponse


@test
def accept_jrds_without_subject(
        client: WebFingerDiagClient,
        server: WebFingerServer
) -> None:

    test_id = server.obtain_account_identifier()

    normal_response : WebFingerQueryDiagResponse = client.diag_perform_webfinger_query(test_id)

    if 'subject' in normal_response.jrd.subject():
        json_without_subject = json.loads(normal_response.jrd.as_json_string())
        json_without_subject.pop('subject')

        without_subject_response : WebFingerQueryDiagResponse = server.override_webfinger_response(
            lambda: client.diag_perform_webfinger_query(test_id),
            {
                test_id : json.dumps(json_without_subject)
            }
        )
        assert_that(without_subject_response.jrd.validate(), spec_level=SpecLevel.MUST, interop_level=InteropLevel.PROBLEM)
