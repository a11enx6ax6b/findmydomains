from reverseWhois import ReverseWhois
class FindMyDomains:
  def __init__(self,seed_domain,api_config_file=".env"):
    self.seed_domain=seed_domain
    self.api_config_file=api_config_file
    reversewhois=ReverseWhois(self.api_config_file)
    reversewhois.load_rwhois_token()
    reversewhois.reverse_whois(self.seed_domain)
  
  