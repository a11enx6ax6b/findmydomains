from reverseWhois import ReverseWhois
from dnslookup import DNSLookup
class FindMyDomains:
  def __init__(self,seed_domain,api_config_file=".env"):
    self.seed_domain=seed_domain
    self.api_config_file=api_config_file
  def do_reverse_whois(self):
    reversewhois=ReverseWhois(self.api_config_file)
    reversewhois.load_rwhois_token()
    self.valid_domains=reversewhois.reverse_whois(self.seed_domain)
  def do_dns_lookup(self):
    dnslookup=DNSLookup(self.valid_domains)
    self.active_domains=dnslookup.check_active_dns_record()
    print(self.active_domains)
  