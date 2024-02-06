"Main app"


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# from auth.api import router as auth_router
from item.api import router
# from user.api import router as user_router

app = FastAPI()


origins = [
    "http://localhost",
    "http://localhost:3000",
]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )
app.include_router(router)
# app.include_router(auth_router)
# app.include_router(user_router)
