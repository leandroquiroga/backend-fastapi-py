from fastapi.security import OAuth2PasswordBearer
# Instancia de OAuth2PasswordBearer para la autenticacion.
oauth2 = OAuth2PasswordBearer(tokenUrl="token")