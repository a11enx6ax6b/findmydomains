import requests
import re
class ASNLookup:
  def __init__(self,sld):
    self.url = "https://asn.cymru.com/cgi-bin/whois.cgi"
    self.sld=sld
    self.valid_as_names={}
  def do_asn_lookup(self,ips):  
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
      as_name= match[0].split('|')[2].strip()
      as_num= match[0].split('|')[0].strip()
      if self.validate_asn(as_name):
        self.valid_as_names[ip]=as_name
    return self.valid_as_names
  def validate_asn(self,as_name):
    if self.sld.lower() in as_name.lower():
      return as_name
    else:
      pass #ask llama

    


