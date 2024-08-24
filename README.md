# findmydomains
Find apex domains that you own

## Usage:
```
from findmydomains import FindMyDomains
d=FindMyDomains("your_seed_domain")
d.do_reverse_whois(max_rwhois_api_calls=1)
d.do_dns_lookup()
d.do_asn_lookup()
```
