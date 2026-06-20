# API Authentication and Error Guide

## Bearer Token Authentication
All API requests to the production environment must pass a valid Bearer Token in the HTTP Authorization header. 
Format: `Authorization: Bearer <YOUR_TOKEN>`

## Error 401 Unauthorized
If the system returns a 401 response code, it indicates a cryptographic signature mismatch or token expiration.
- Tokens expire precisely 60 minutes after generation.
- Solution: Call the `/v1/auth/refresh` endpoint using your primary Secret Key to obtain a clean runtime session payload.

## Error 500 Internal Server Failure
Occurs when database connection limits are reached during large payload bursts.
- Solution: Implement an exponential backoff retry loop with a random jitter factor of 1-3 seconds.