import requests
class VerificationLLM:
  def __init__(self,token_pplx):
    self.token=token_pplx
  def verify_as_name(self,as_name,seed_domain):
    query=f"""Check if ASN name \"{as_name}\" belongs to organization of {seed_domain} . 
    Rules:
    1) No justification required.
    2) Score ranges from 1 to 10.
    3) Answer Format: Score: value, eg: Score: 8
    4) If the ASN_name is CDN/WAF eg: CLOUDFLARENET,AKAMAI-AS or Cloud providers like AMAZON-02, score must be 0
      unless organization searched is same as Cloud provider. """
    url = "https://api.perplexity.ai/chat/completions"
    payload = {
        "model": "llama-3.1-70b-instruct",
        "messages": [
            {
                "role": "user",
                "content": f"{query}"
            }
        ]
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {self.token}"
    }
    response = requests.post(url, json=payload, headers=headers)
    response_json=response.json()
    try:
      score=response_json["choices"][0]["message"]["content"].split(":")[1].strip()
    except:
      if response.status_code == 422:
        score=None
        print("Validation Error-PPLX")
      else:
        score=None
        print("Score might not be in proper format")
   # print(f"ASN_name: {as_name}, Suggested score: {response} ")
    return score
    