from fastapi import APIRouter

from src.controllers import test_controller

api_router = APIRouter()


@api_router.get("/test")
async def test():
    # return {"message": "This is a protected route", "user_email": current_user.email}
    return await test_controller.test_endpoint()
