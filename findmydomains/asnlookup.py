import requests
import re
class ASNLookup:
  def __init__(self):
    self.url = "https://asn.cymru.com/cgi-bin/whois.cgi"
  def do_asn_lookup(self,ip):
    self.ip=ip
    headers = {
        "Content-Type": "multipart/form-data; boundary=---------------------------123"
    }
    print(self.ip)
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
    return match[0].split('|')[2].strip()

