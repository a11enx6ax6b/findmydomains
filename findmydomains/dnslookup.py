from nslookup import Nslookup
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
