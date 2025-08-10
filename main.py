from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


from ROUTER.root import router as root_router
from ROUTER.auth import router as auth_router
from ROUTER.note import router as note_router
from ROUTER.user import router as user_router
from ROUTER.category import router as category_router



app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(root_router)
app.include_router(auth_router)
app.include_router(note_router)
app.include_router(user_router)
app.include_router(category_router)