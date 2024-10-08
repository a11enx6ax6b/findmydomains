import json
import requests
import re
from datetime import date
from urllib.parse import quote 
api_url="https://api.whoxy.com"
class ReverseWhois():
  def __init__(self):
    self.valid_domains={}
    self.today=date.today()
  @staticmethod
  def load_rwhois_token(api_config_file):
    with open(api_config_file,'r') as file:
      tokens=json.load(file)
      return tokens
  def reverse_whois(self,seed_domain,second_level_domain,token_rwhois,token_whois,max_api_calls=5):
    self.seed_domain=seed_domain
    max_rwhois_api_calls=max_api_calls
    self.rwhois_token=token_rwhois
    self.whois_token=token_whois
    current_rwhois_api_calls=0
    self.second_level_domain=second_level_domain
    url = "https://zozor54-whois-lookup-v1.p.rapidapi.com/"
    querystring = {"domain":self.seed_domain,"format":"json","_forceRefresh":"0"}
    headers = {
        "x-rapidapi-key": self.whois_token,
        "x-rapidapi-host": "zozor54-whois-lookup-v1.p.rapidapi.com"
    } # whois -> new fn
    response = requests.get(url, headers=headers, params=querystring)
    response=response.json()
    organization,email,nameserver=set(),set(),set()
    if isinstance(response["contacts"],dict):
      for info in response["contacts"].values():
        organization.add(info[0]['organization'])
        email.add(info[0]['email'])
    nameserver=response["nameserver"]
    verified_organization,verified_email,verified_nameserver=self.verify_data(organization,email,nameserver) #optimize
    print(verified_organization)
    if verified_organization:
      for org in verified_organization:
        current_page=1
        total_page=1
        while current_page <= total_page and max_rwhois_api_calls > current_rwhois_api_calls:
          print(org)
          response_rwhois_by_company_name=requests.get(f"{api_url}/?key={self.rwhois_token}&reverse=whois&company={quote(org,safe='')}&mode=micro&page={current_page}") 
          current_rwhois_api_calls+=1
          #pagination needed #1#
          response_rwhois_by_company_name=response_rwhois_by_company_name.json()
          print(response_rwhois_by_company_name)
          current_page=response_rwhois_by_company_name["current_page"]+1
          total_page=response_rwhois_by_company_name["total_pages"]
          self.capture_rwhois_result(response_rwhois_by_company_name)
    if verified_email:
      for email in verified_email:
        current_page=1
        total_page=1
        while current_page <= total_page and max_rwhois_api_calls > current_rwhois_api_calls:
          response_rwhois_by_email=requests.get(f"{api_url}/?key={self.rwhois_token}&reverse=whois&email={email}&mode=micro&page={current_page}")
          current_rwhois_api_calls+=1
          response_rwhois_by_email=response_rwhois_by_email.json()
          current_page=response_rwhois_by_company_name["current_page"]+1
          total_page=response_rwhois_by_company_name["total_pages"]
          self.capture_rwhois_result(response_rwhois_by_email)
    return self.valid_domains,verified_nameserver    
  def capture_rwhois_result(self,response_rwhois):
    for result in response_rwhois["search_result"]:
        domain_name = result["domain_name"]
        try:
            expiry_date = result["expiry_date"]
        except:
            expiry_date = ""
        if domain_name and expiry_date:
          if date.fromisoformat(expiry_date)>self.today:
            self.valid_domains[domain_name]={"expiry_date": expiry_date}    
  #def generate_output(self,response_rwhois):
    # identifier = next(iter(response_rwhois["search_identifier"].values()))
    # print("=" * 50)
    # print(f"Domain names found and its expiry Date ( Identifier: {identifier} )")
    # print("=" * 50)

    # for result in response_rwhois["search_result"]:
    #     domain_name = result["domain_name"]
    #     try:
    #       expiry_date = result["expiry_date"]
    #     except:
    #       expiry_date = "No info"
    #     print(f"Domain: {domain_name}")
    #     print(f"Expiry Date: {expiry_date}")
    #     print("-" * 50) 

    # print("=" * 50)
    # response_rwhois_by_keyword=requests.get(f"{api_url}/?key={self.rwhois_token}&reverse=whois&keyword={self.second_level_domain}").json()
   # search by keyword might produce lot of false positives

  def verify_data(self,organization,email,nameserver):
    irrelevant_data=["info@domain-contact.org","REDACTED FOR PRIVACY","REDACTED"]
    cloud_provider_nameservers = [
    "ns-2048.awsdns-64.com",  #AWS nameserver
    "ns-2049.awsdns-65.net",
    "ns-2050.awsdns-66.org",
    "ns-2051.awsdns-67.co.uk",

    "ns-cloud-a1.googledomains.com", # Google Cloud Platform (GCP)
    "ns-cloud-a2.googledomains.com",
    "ns-cloud-a3.googledomains.com",
    "ns-cloud-a4.googledomains.com",

    "ns1-07.azure-dns.com",
    "ns2-07.azure-dns.net", # Microsoft Azure
    "ns3-07.azure-dns.org",
    "ns4-07.azure-dns.info",

    "ns1.digitalocean.com",  # DigitalOcean
    "ns2.digitalocean.com",
    "ns3.digitalocean.com",

    "ns1.ibmdns.com", # IBM Cloud
    "ns2.ibmdns.com",
    "ns3.ibmdns.com",

    "ns1.cloudflare.com",
    "ns2.cloudflare.com", # Cloudflare

    "ns1.linode.com",
    "ns2.linode.com", # Linode
    "ns3.linode.com",

    "ns1.vultr.com",  # Vultr
    "ns2.vultr.com",

    "dns1.registrar-servers.com", # Namecheap
    "dns2.registrar-servers.com",
    "dns3.registrar-servers.com",
    "dns4.registrar-servers.com",

    "ns1.godaddy.com",  # GoDaddy
    "ns2.godaddy.com",
    "ns3.godaddy.com",
    "ns4.godaddy.com",
]

    filtered_org = [
        item for item in organization 
        if not any(data in item for data in irrelevant_data)
    ]
    filtered_email = [
    item for item in email 
    if not any(data in item for data in irrelevant_data)
]
    filtered_nameserver=[ item for item in nameserver if item not in cloud_provider_nameservers and self.second_level_domain in item ]
     # Nameserver will be useful for verification
    filtered_email=self.is_valid_email(filtered_email)
    return filtered_org,filtered_email,filtered_nameserver
  def is_valid_email(self,filtered_email):
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    filtered_email={item for item in filtered_email if re.match(email_pattern,item) is not None}
    return filtered_email

  