from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import timedelta, datetime
from .models import UserSchema, ProjectCreateSchema, ProjectSchema, CurrentUser
from .crud import add_user, retrieve_user, add_project, retrieve_user_projects
from typing import List
from uuid import uuid4

# Configuração de JWT e autenticação
SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

app = FastAPI()

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Função para obter o usuário atual
async def get_current_user(token: str = Depends(oauth2_scheme)) -> CurrentUser:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = await retrieve_user(username)
    if user is None:
        raise credentials_exception

    return CurrentUser(**user)

# Rota para registrar um novo usuário
@app.post("/register")
async def register(user: UserSchema):
    existing_user = await retrieve_user(user.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="User already registered")

    user_dict = user.dict()
    user_dict["hashed_password"] = get_password_hash(user.password)
    new_user = await add_user(user_dict)
    return {"message": "User registered successfully"}

# Rota para login
@app.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await retrieve_user(form_data.username)
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user["username"]}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

# Rota para criar um novo projeto
@app.post("/projects/", response_model=ProjectSchema)
async def create_project(project: ProjectCreateSchema, current_user: CurrentUser = Depends(get_current_user)):
    project_data = project.dict()
    project_data["owner"] = current_user.username
    project_data["members"] = [current_user.username]
    project_data["id"] = str(uuid4())  # Gera um ID único para o projeto
    new_project = await add_project(project_data)
    return new_project

# Rota para listar projetos do usuário atual
@app.get("/projects/", response_model=List[ProjectSchema])
async def list_projects(current_user: CurrentUser = Depends(get_current_user)):
    projects = await retrieve_user_projects(current_user.username)
    return projects

@app.get("/")
def read_root():
    return {"Status": "Funcionando"}
