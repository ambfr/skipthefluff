from fastapi import APIRouter, HTTPException, Depends
from app.models.user import UserSignup, UserLogin, TokenResponse, UserPublic
from app.services.auth import hash_password, verify_password, create_access_token
from app.database import get_db
from app.dependencies import get_current_user
from app.config import settings
from bson import ObjectId
import httpx

router = APIRouter(prefix="/auth", tags=["auth"])


def user_to_public(user: dict) -> UserPublic:
    return UserPublic(
        id=str(user["_id"]),
        email=user["email"],
        name=user.get("name", ""),
        avatar_url=user.get("avatar_url"),
        auth_provider=user.get("auth_provider", "email"),
    )


@router.post("/signup", response_model=TokenResponse)
async def signup(data: UserSignup):
    db = get_db()

    existing = await db["users"].find_one({"email": data.email})
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    user_doc = {
        "email": data.email,
        "name": data.name,
        "password_hash": hash_password(data.password),
        "auth_provider": "email",
        "avatar_url": None,
    }
    result = await db["users"].insert_one(user_doc)
    user_doc["_id"] = result.inserted_id

    token = create_access_token(str(result.inserted_id), data.email)
    return TokenResponse(access_token=token, user=user_to_public(user_doc))


@router.post("/login", response_model=TokenResponse)
async def login(data: UserLogin):
    db = get_db()
    user = await db["users"].find_one({"email": data.email})

    if not user or user.get("auth_provider") != "email":
        raise HTTPException(status_code=401, detail="Invalid email or password")

    if not verify_password(data.password, user.get("password_hash", "")):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = create_access_token(str(user["_id"]), user["email"])
    return TokenResponse(access_token=token, user=user_to_public(user))


@router.post("/google", response_model=TokenResponse)
async def google_login(id_token: str):
    """Verify a Google ID token (sent from frontend Google Sign-In) and log the user in."""
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            "https://oauth2.googleapis.com/tokeninfo",
            params={"id_token": id_token},
        )
        if resp.status_code != 200:
            raise HTTPException(status_code=401, detail="Invalid Google token")

        payload = resp.json()

        if payload.get("aud") != settings.google_client_id:
            raise HTTPException(status_code=401, detail="Token audience mismatch")

        email = payload.get("email")
        name = payload.get("name", "")
        picture = payload.get("picture")

    db = get_db()
    user = await db["users"].find_one({"email": email})

    if not user:
        user_doc = {
            "email": email,
            "name": name,
            "password_hash": None,
            "auth_provider": "google",
            "avatar_url": picture,
        }
        result = await db["users"].insert_one(user_doc)
        user_doc["_id"] = result.inserted_id
        user = user_doc

    token = create_access_token(str(user["_id"]), user["email"])
    return TokenResponse(access_token=token, user=user_to_public(user))


@router.get("/me", response_model=UserPublic)
async def get_me(current_user: dict = Depends(get_current_user)):
    return user_to_public(current_user)
