from fastapi import HTTPException, APIRouter, Depends

from business.bao.services.user_bao_service import UserBAOService
from persistence.dal.user_dal import UserDAL
from presentation.pao.services.user_pao_service import UserPAOService
from business.bal.user_bal import UserBAL
from database import get_db
from presentation.pal.user_pal import UserPAL, PasswordRequest
from configurations.jws_authentification import get_current_user


router = APIRouter()

db = next(get_db())

user_dal = UserDAL(db)
user_bao = UserBAOService(user_dal)
user_bal = UserBAL(user_bao)
user_pao = UserPAOService(user_bal)
user_pal = UserPAL(user_pao)


@router.post("/api/trademind/users/register")
def register_user(user_data: dict):
    try:
        return user_pal.register_user(user_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/api/trademind/users/login")
def login_user(user_data: dict):
    try:
        return user_pal.login_user(user_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/api/trademind/users/verify-email")
def verify_email(token: str):
    try:
        return user_pal.verify_user_email_by_token(token)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/api/trademind/users/forgot-password")
def forgot_password(user_data: dict):
    try:
        email = user_data.get("email")
        if not email:
            raise HTTPException(status_code=400, detail="Email is required")
        user_pal.forgot_password(email)
        return {"message": "Password reset initiated."}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/api/trademind/users/reset-password")
def reset_password(user_data: dict):
    try:
        token = user_data.get("token")
        new_password = user_data.get("new_password")

        if not token or not new_password:
            raise HTTPException(status_code=400, detail="Token and new password are required.")

        user_pal.reset_password(token, new_password)
        return {"message": "Password successfully reset."}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/api/trademind/users/update-password")
def update_password(user_data: dict, current_user: dict = Depends(get_current_user)):
    email_from_token = current_user.get("sub")
    email_from_request = user_data.get("email")

    if email_from_token != email_from_request:
        raise HTTPException(status_code=403, detail="Not authorized to change this user's password.")

    try:
        email = user_data.get("email")
        current_password = user_data.get("current_password")
        new_password = user_data.get("new_password")

        if not email or not new_password:
            raise HTTPException(status_code=400, detail="Email and new password are required")
        user_pal.update_password(email, current_password, new_password)
        return {"message": "Password successfully reset"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/api/trademind/users/details/{user_id}")
def get_user_details(user_id: int, current_user: dict = Depends(get_current_user)):
    if current_user["user_id"] != user_id:
        raise HTTPException(status_code=403, detail="Not authorized.")

    try:
        return user_pal.get_user_details(user_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/api/trademind/users/{user_id}")
def update_user_details(user_id: int, user_data: dict, current_user: dict = Depends(get_current_user)):
    if current_user["user_id"] != user_id:
        raise HTTPException(status_code=403, detail="Not authorized.")

    try:
        print("Received update data:", user_data)
        return user_pal.update_user_details(user_id, user_data)
    except ValueError as e:
        print("Update failed:", e)
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/api/trademind/users/password")
def get_user_by_password(request: PasswordRequest):
    user_entity = user_pal.get_user_by_password(request.password)

    if not user_entity:
        raise HTTPException(status_code=404, detail="User not found")

    return user_entity


@router.delete("/api/trademind/users/{email}")
def delete_user(email: str):
    try:
        user_pal.delete_user(email)
        return {"message": "User successfully deleted"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/api/trademind/users")
def get_all_users():
    return user_pal.get_all_users()




