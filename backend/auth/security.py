from fastapi import HTTPException, Header

# Store emails of logged-in users
authenticated_users = set()

def require_auth(x_user_email: str | None = Header(default=None)):
    if not x_user_email:
        raise HTTPException(status_code=401, detail="Not authenticated")

    if x_user_email not in authenticated_users:
        raise HTTPException(status_code=401, detail="Invalid user")

    return x_user_email