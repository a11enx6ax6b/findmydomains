from nslookup import Nslookup
from reverseWhois import ReverseWhois
from asnlookup import ASNLookup
class DNSLookup:
    def __init__(self,domains):
        self.domains=domains
    def check_active_dns_record(self):
        for domain in self.domains.keys():
            dns_query = Nslookup()
            dns_query = Nslookup(dns_servers=["1.1.1.1"], verbose=False, tcp=False)
            ips_record = dns_query.dns_lookup(domain)
            self.domains[domain]["IP"]=ips_record.answer
        return self.domains
            # soa_record = dns_query.soa_lookup(domain) # check with nameserver whois
            # print(soa_record.response_full, soa_record.answer)
    def check_asn_for_ips_found(self,api_config_file):
        self.asn_names={}
        reverse_whois=ReverseWhois()
        self.api_config_file=api_config_file
        self.token=reverse_whois.load_rwhois_token(self.api_config_file)["whois_api_token"]
        self.ips=[ip for domain in self.domains.keys() if self.domains[domain]["IP"] for ip in self.domains[domain]["IP"]]
        asn_lookup=ASNLookup()
        for ip in self.ips:
          self.asn_names[ip]=asn_lookup.do_asn_lookup(ip)
        return self.ips,self.asn_names


                