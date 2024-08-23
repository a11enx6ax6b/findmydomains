from reverseWhois import ReverseWhois
from dnslookup import DNSLookup
class FindMyDomains:
  def __init__(self,seed_domain,api_config_file=".env"):
    self.seed_domain=seed_domain
    self.api_config_file=api_config_file
  def do_reverse_whois(self,max_rwhois_api_calls):
    reversewhois=ReverseWhois()
    reversewhois.load_rwhois_token(self.api_config_file)
    self.valid_domains,self.verified_nameserver=reversewhois.reverse_whois(self.seed_domain,max_rwhois_api_calls)
  def do_dns_lookup(self):
    dnslookup=DNSLookup(self.valid_domains)
    self.active_domains=dnslookup.check_active_dns_record()
    self.ips,self.asn_names=dnslookup.check_asn_for_ips_found(self.api_config_file)
    print(self.active_domains)
    print(self.ips)
    print(self.asn_names)
