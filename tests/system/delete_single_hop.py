"""
Test single-hop delete

See also: https://github.com/fediverse-devnet/feditest-tests-fediverse/issues/3

1. `actor-b@b.example` follows `actor-a@a.example`
2. `actor-a@a.example`: `Create(Note-X)`
3. `actor-b@b.example`: receives `Create(Note-X)` and `Note-X` is now in `actor-b@b.example`'s inbox
4. `actor-a@a.example`: `Delete(Note-X)`
5. On `b.example`, `Note-X` is now inaccessible (404) or has been replaced with a tombstone

FIXME
"""
