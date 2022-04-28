class FTX:
    import time
    import hmac
    from requests import Request

    

    def __init__(self):
        self.secret = None
        self.key = None
    
    def connect(self,secret:str,key:str):
        self.secret = secret
        self.key = key
        
        
    def get(self, request):
        ts = int(time.time() * 1000)
        request = Request('GET', request)
        prepared = request.prepare()
        signature_payload = f'{ts}{prepared.method}{prepared.path_url}'.encode()
        signature = hmac.new(self.secret.encode(), signature_payload, 'sha256').hexdigest()

        prepared.headers['FTX-KEY'] = self.key
        prepared.headers['FTX-SIGN'] = signature
        prepared.headers['FTX-TS'] = str(ts)
    
    