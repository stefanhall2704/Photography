import random
import string
import base64
import hashlib

code_verifier = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(random.randint(43, 128)))
code_verifier = base64.urlsafe_b64encode(code_verifier.encode('utf-8'))
print(code_verifier)

code_challenge = hashlib.sha256(code_verifier).digest()
code_challenge = base64.urlsafe_b64encode(code_challenge).decode('utf-8').replace('=', '')
print(code_challenge)

# print("code_verifier:", code_verifier)
# print("code_challenge:", code_challenge)


# http://127.0.0.1:8000/o/authorize/?response_type=code&code_challenge=QVWbUPzuz7nTmHjPC-WK4p7-bzMCah9TWrGWNOXkuD8&code_challenge_method=S256&client_id=UfiRboTyMuLLIhVSRNIy5TcgEcEFapKPlq7DKZO8&redirect_uri=http://127.0.0.1:8000/noexist/callback

# curl -X POST -d "client_id=UfiRboTyMuLLIhVSRNIy5TcgEcEFapKPlq7DKZO8&client_secret=cxZEC6pcNj15biaB1GEu1lbpq7a7jIdfI0Bl6y9NuNRAJb3aRiESrd0F9xia5uZ02bGXje2z8GO0O2sHbvpBU7SB6uyb7vXRyUAZLFyw8VHtJHFQoQFARGFYNfyKnBuy&grant_type=authorization_code&code=4cbu1fM06cly5dFrdtJB8xuIWLKIff&code_verifier=35PSDY6G3OC4FEF48RGCHYBCRL9IU8GCJWGNWEMKH1KCK8E5Y33JZNOVL8DGOXP&redirect_uri=http%3A%2F%2F127.0.0.1:8000%2Fnoexist%2Fcallback" http://127.0.0.1:8000/o/token/
# curl -X POST -H "Cache-Control: no-cache" -H "Content-Type: application/x-www-form-urlencoded" "http://127.0.0.1:8000/o/token/" -d "client_id=UfiRboTyMuLLIhVSRNIy5TcgEcEFapKPlq7DKZO8" -d "client_secret=cxZEC6pcNj15biaB1GEu1lbpq7a7jIdfI0Bl6y9NuNRAJb3aRiESrd0F9xia5uZ02bGXje2z8GO0O2sHbvpBU7SB6uyb7vXRyUAZLFyw8VHtJHFQoQFARGFYNfyKnBuy" -d "code=4cbu1fM06cly5dFrdtJB8xuIWLKIff" -d "code_verifier=35PSDY6G3OC4FEF48RGCHYBCRL9IU8GCJWGNWEMKH1KCK8E5Y33JZNOVL8DGOXP" -d "redirect_uri=http://127.0.0.1:8000/noexist/callback" -d "grant_type=authorization_code"
