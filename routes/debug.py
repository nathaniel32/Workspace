from fastapi import Depends, Request, Body, APIRouter

class DebugAPI:
    def __init__(self):
        self.router = APIRouter(prefix="/debug", tags=["Debug"])
        self.router.add_api_route("/request", self.debug_request, methods=["GET"])

    async def debug_request(self, request: Request):
        headers = dict(request.headers)
        cookies = request.cookies
        query_params = dict(request.query_params)
        client_host = request.client.host if request.client else "Unknown"
        method = request.method
        url = str(request.url)
        body = await request.body()
        
        return {
            "method": method,
            "url": url,
            "client_ip": client_host,
            "headers": headers,
            "cookies": cookies,
            "query_params": query_params,
            "body": body.decode("utf-8") if body else None
        }