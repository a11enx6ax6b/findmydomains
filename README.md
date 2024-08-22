# findmydomains
Find apex domains that you own

## Usage:
```
from findmydomains import FindMyDomains
d=FindMyDomains("google.com")
d.do_reverse_whois(max_rwhois_api_calls=10) # default = 5
d.do_dns_lookup()
```
