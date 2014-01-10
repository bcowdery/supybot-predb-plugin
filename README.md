Supybot Pre Dupe Check
======================

Plugin for the supybot IRC bot for checking scene releases against the pre database.


# Getting Started

## Dependencies

* [requests](http://docs.python-requests.org/)

**Installation:**
```
pip install requests
```


## Configuration

A sample configuration file `pre.cfg.sample` is provided

```config
[PreDb]
ApiKey: deadbeef123
Url: https://api.pre.im/v1.0/
VerifyCertificate: True
```

* `ApiKey` - PRE.iM Accesskey
* `Url` - Url endpoint for the PRE.iM API
* `VerifyCertificate` - Set to 'False' to ignore SSL certificate errors

_Note: Do not disable SSL certificate verification unless you know what you are doing! Typically updating your machines
certificate store is enough to solve most SSL verification errors_


# Documentation:

* [PRE.iM API Documentation](https://pre.im/doku/index.htm)

