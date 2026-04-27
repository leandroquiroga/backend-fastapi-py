from fastapi import HTTPException, Request, status
from time import time
from typing import Dict

RATE_LIMIT_STORAGE: Dict[str, Dict] = {}
def create_rate_limiter(max_requests: int, window_seconds: int):
    """
      Crea un rate limiter para limitar el numero de request por IP
      
      Args: 
        max_requests: numero maximo de request permitidos
        window_seconds: ventana de tiempo en segundos para el rate limit
        
      Returns:
        # Dependency de FastAPI para aplicar el rate limit

    """
    
    async def rate_limiter(request: Request):
        client_id = request.client.host # IP del cliente
        current_time = time() # Formato: timestamp en segundos
        
        # Crea un registro para un cliente
        if client_id not in RATE_LIMIT_STORAGE:
            RATE_LIMIT_STORAGE[client_id] = {
                "count": 1,
                "reset_time": current_time + window_seconds
            }
            
            return

        client_data = RATE_LIMIT_STORAGE[client_id]
        
        
        # Verificar si la ventana expiró
        if current_time >=  client_data['reset_time']:
            client_data["count"] = 1
            client_data["reset_time"] = current_time + window_seconds
        else:
            # Incrementar contador
            client_data["count"] += 1
            
            # Verificar Limite
            if client_data["count"] > max_requests: 
                retry_after = int(client_data['rest_time'] - current_time) # 30 - 10 = 20
                raise HTTPException(
                    status_code= status.HTTP_429_TOO_MANY_REQUESTS,
                    detail=f"Rate limit exceeded. Try again in {retry_after} seconds.",
                    headers={"Retry-After": str(retry_after)}
                )
                
    return rate_limiter
  
  
# Rate limiters especificos para cada endpoint
login_rate_limiter = create_rate_limiter(max_requests=5, window_seconds=60)
change_password_rate_limiter = create_rate_limiter(max_requests=3, window_seconds=300)
get_users_rate_limiter = create_rate_limiter(max_requests=30, window_seconds=60)
get_user_rate_limiter = create_rate_limiter(max_requests=50, window_seconds=60)
update_user_rate_limiter = create_rate_limiter(max_requests=20, window_seconds=60)