import time
from fastapi import Request
from datetime import datetime
from utilities import logging

async def logging_middleware(request: Request, call_next):
    """Resgistra informacion de cada request"""
    
    start_time = time.perf_counter()
    client_ip = request.client.host if request.client else "unknown"
    method = request.method
    url = str(request.url)
    
    logging(f"📤  [{datetime.now().strftime('%d/%m/%Y, %H:%M:%S')}] REQUEST", context="REQUEST")
    logging(f"    Method: {method}", context="REQUEST")
    logging(f"    URL: {url}", context="REQUEST")
    logging(f"    Client IP: {client_ip}", context="REQUEST")
    
    response = await call_next(request)
    
    process_time = time.perf_counter() - start_time
    
    logging(f"📥  RESPONSE", context="RESPONSE")
    logging(f"    Status Code: {response.status_code}", context="RESPONSE")
    logging(f"    Process Time: {process_time:.3f}s", context="RESPONSE")
    
    response.headers['X-Process-Time'] = str(process_time)
    
    return response