from motor.motor_asyncio import AsyncIOMotorClient
from bson.objectid import ObjectId

# Conexão com o banco de dados MongoDB
client = AsyncIOMotorClient("mongodb://localhost:27017")
db = client["task_manager_db"]

# Função para adicionar um novo usuário
async def add_user(user_data: dict) -> dict:
    user = await db["users"].insert_one(user_data)
    new_user = await db["users"].find_one({"_id": user.inserted_id})
    return new_user

# Função para recuperar um usuário pelo nome de usuário
async def retrieve_user(username: str) -> dict:
    user = await db["users"].find_one({"username": username})
    return user

# Função para adicionar um novo projeto
async def add_project(project_data: dict) -> dict:
    project = await db["projects"].insert_one(project_data)
    new_project = await db["projects"].find_one({"_id": project.inserted_id})
    return new_project

# Função para recuperar os projetos do usuário
async def retrieve_user_projects(username: str) -> list:
    projects = await db["projects"].find({"members": username}).to_list(100)
    return projects
