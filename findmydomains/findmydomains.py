from reverseWhois import ReverseWhois
from dnslookup import DNSLookup
from asnlookup import ASNLookup
class FindMyDomains:
  def __init__(self,seed_domain,api_config_file=".env"):
    self.seed_domain=seed_domain
    self.api_config_file=api_config_file
    self.second_level_domain=seed_domain.split(".")[-2] if seed_domain.split(".")[-2] not in ["com","co"] else seed_domain.split(".")[-3]
  def do_reverse_whois(self,max_rwhois_api_calls):
    reversewhois=ReverseWhois()
    self.tokens=reversewhois.load_rwhois_token(self.api_config_file)
    token_rwhois=self.tokens["reversewhois_api_token"]
    token_whois=self.tokens["whois_api_token"]
    self.valid_domains,self.verified_nameserver=reversewhois.reverse_whois(self.seed_domain,self.second_level_domain,token_rwhois,token_whois,max_rwhois_api_calls)
  def do_dns_lookup(self):
    dnslookup=DNSLookup(self.valid_domains)
    self.active_domains,self.ips=dnslookup.check_active_dns_record()
    print(self.active_domains)
    print(self.ips)
  def do_asn_lookup(self):
    asn_lookup=ASNLookup(self.second_level_domain,self.seed_domain)
    self.token_pplx=self.tokens["pplx_token"]
    self.token_asnlookup=self.tokens["asnlookup"]
    self.asn_names=asn_lookup.do_asn_lookup(self.ips,self.token_pplx,self.token_asnlookup)
    print(self.asn_names)