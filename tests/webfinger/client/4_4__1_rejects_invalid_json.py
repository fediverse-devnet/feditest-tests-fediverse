from feditest import hard_assert_that, test
from feditest.protocols.webfinger import WebFingerClient, WebFingerServer
from feditest.protocols.webfinger.traffic import WebFingerQueryResponse

@test
def rejects_invalid_json(
        client: WebFingerClient,
        server: WebFingerServer
) -> None:

    test_id = server.obtain_account_identifier()
    overridden_jrd_json_string = """{
       "subject" : "acct:bob@example.com",
       "aliases" :
       [
         "https://www.example.com/~bob/"
       ],
       "properties" :
       {
           "http://example.com/ns/role" : "employee"
       },
       "links" :
       [
         {
           "rel" : "http://webfinger.example/rel/profile-page",
           "href" : "https://www.example.com/~bob/"
         },
         {
           "rel" : "http://webfinger.example/rel/businesscard",
           "href" : "https://www.example.com/~bob/bob.vcf"
         }
       ]
     }
  }}}
  """ # same as in 4_3__6 but with some extra curly braces at the end

    webfinger_response : WebFingerQueryResponse = server.override_webfinger_response(
            lambda:
                client.perform_webfinger_query(test_id),
            {
                test_id : overridden_jrd_json_string
            }
    )
    hard_assert_that(not webfinger_response.jrd.validate())
