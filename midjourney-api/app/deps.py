from app.utils.security import verify_api_key
from fastapi import HTTPException, Security
from fastapi.security import APIKeyHeader, HTTPBearer

BearerAuthentication = HTTPBearer()

API_KEY_NAME = "api-key"
api_key_header = APIKeyHeader(
    name=API_KEY_NAME, scheme_name="API key header", auto_error=False
)


# apikey approach
def api_key_security(header_param: str = Security(api_key_header)) -> str:
    if header_param and verify_api_key(header_param):
        return header_param
    else:
        raise HTTPException(status_code=403, detail="apiKey header invalid")
