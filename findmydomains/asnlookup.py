import requests
import re
import time
from verificationllm import VerificationLLM
class ASNLookup:
  def __init__(self,sld,seed_domain):
    self.url = "https://asn.cymru.com/cgi-bin/whois.cgi"
    self.sld=sld
    self.seed_domain=seed_domain
    self.valid_as_names={}
  def do_asn_lookup(self,ips,token_pplx,token_asnlookup):  
    """
    Expects:
      IP in a list
      Perplexity token "pplx_token" key in config file
      ASNlookup token  "asnlookup" key in config file
    """
    self.token_asnlookup=token_asnlookup
    self.verification=VerificationLLM(token_pplx)
    for ip in ips:
      self.ip=ip
      headers = {
          "Content-Type": "multipart/form-data; boundary=---------------------------123"
      }
      data = (
          "-----------------------------123\r\n"
          "Content-Disposition: form-data; name=\"action\"\r\n\r\n"
          "do_whois\r\n"
          "-----------------------------123\r\n"
          "Content-Disposition: form-data; name=\"family\"\r\n\r\n"
          "ipv4\r\n"
          "-----------------------------123\r\n"
          "Content-Disposition: form-data; name=\"method_whois\"\r\n\r\n"
          "whois\r\n"
          "-----------------------------123\r\n"
          "Content-Disposition: form-data; name=\"bulk_paste\"\r\n\r\n"
          f"{self.ip}\r\n"
          "-----------------------------123\r\n"
          "Content-Disposition: form-data; name=\"submit_paste\"\r\n\r\n"
          "Submit\r\n"
          "-----------------------------123--\r\n"
      )
      response = requests.post(self.url,headers=headers,data=data)
      pattern=r"^(?!<).*?\|.*?\|.*$"
      match=re.findall(pattern,response.text,re.MULTILINE)
      if match:
        as_name= match[0].split('|')[2].strip()
        as_num= match[0].split('|')[0].strip()
        if self.validate_asn(as_name):
          self.valid_as_names[ip]={"AS_Name":as_name,"ASN":as_num}
    self.find_ip_range_from_asn()
    print(self.valid_as_names)
    return self.valid_as_names
  def validate_asn(self,as_name):
    if self.sld.lower() in as_name.lower():
      return as_name
    else:
      score=self.verification.verify_as_name(as_name,self.seed_domain)
      if score:
        if int(score) > 8 :
          return as_name
        else:
          return None
      else:
        return None
  def find_ip_range_from_asn(self):
    for asn_details in self.valid_as_names.values():
      url = "https://asn-lookup.p.rapidapi.com/api"
      querystring = {"asn":f"{asn_details['ASN']}"}
      headers = {
        "x-rapidapi-key": f"{self.token_asnlookup}",
        "x-rapidapi-host": "asn-lookup.p.rapidapi.com"
      }
      time.sleep(5)
      response = requests.get(url, headers=headers, params=querystring)
      print(response.json())
