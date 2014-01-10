Supybot Pre dupe check
=====================

Plugin for the supybot IRC bot for checking scene releases against the pre database.


Documentation:

* https://pre.im/doku/index.htm


Example using CURL
```
curl https://api.pre.im/v1.0/dupe -H Accesskey:[API Key] -H Accept:application/json -H Content-Type:application/json -v -d '{ "search": "eyes wide shut", "limit": 10 }' --insecure
```
