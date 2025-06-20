from sqlalchemy.orm import Session
from schemas.auth import TokenResponse, AccessTokenPayload, RefreshTokenPayload
from fastapi import Response, Request, HTTPException
from core.config import settings
from datetime import timedelta, datetime, timezone
from jose import jwt
from services.user import UserService
from core.exceptions import AuthenticationException
from utils.hash import verify_password, hash_password
from core.exceptions import PasswordValidationException
import uuid
import redis.asyncio as redis
import logging
import asyncio

class AuthService:
    def __init__(self, db: Session):
        self.db = db
        self.user_service = UserService(db)
        self.logger = logging.getLogger(__name__)
        self.redis_client: redis.Redis | None = None
        try:
            pool = redis.ConnectionPool(
                host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                db=0,
                decode_responses=True,
                max_connections=10,
                socket_timeout=2.0,
            )
            self.redis_client = redis.Redis(connection_pool=pool)
            # Test connection asynchronously (need event loop)
            # But constructor is sync, so we just trust connection here
            self.logger.info("Initialized async Redis connection pool")
        except Exception as e:
            self.logger.error(f"Error initializing Redis connection pool: {str(e)}")
            self.redis_client = None

    @staticmethod
    def create_access_token(data: dict | AccessTokenPayload, expires_delta: timedelta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)):
        # Convert Pydantic model to dict if necessary
        if hasattr(data, 'model_dump'):
            data = data.model_dump()

        # Ensure all values are JSON serializable
        to_encode = {}
        for key, value in data.items():
            # Convert enum values to strings if needed
            if hasattr(value, 'value'):
                value = value.value
            to_encode[key] = value

        # Add expiration time
        expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
        to_encode["exp"] = int(expire.timestamp())

        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return encoded_jwt

    @staticmethod
    def create_refresh_token(data: dict | RefreshTokenPayload, expires_delta: timedelta = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)):
        # Convert Pydantic model to dict if necessary
        if hasattr(data, 'model_dump'):
            data = data.model_dump()

        # Ensure all values are JSON serializable
        to_encode = {}
        for key, value in data.items():
            # Convert enum values to strings if needed
            if hasattr(value, 'value'):
                value = value.value
            to_encode[key] = value

        # Add expiration time
        expire = datetime.now(timezone.utc) + (expires_delta or timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS))
        to_encode["exp"] = int(expire.timestamp())

        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return encoded_jwt

    async def _store_refresh_token_in_redis(self, user_id: str | int, refresh_token: str) -> bool:
        if not self.redis_client:
            self.logger.warning("Redis client is not available, refresh token not stored")
            return False
        try:
            # Ensure user_id is a string for Redis key
            user_id_str = str(user_id)
            expiration_seconds = settings.REFRESH_TOKEN_EXPIRE_DAYS * 60 * 60 * 24
            await self.redis_client.setex(user_id_str, expiration_seconds, refresh_token)
            self.logger.info(f"Successfully stored refresh token for user {user_id_str}")
            return True
        except redis.RedisError as e:
            self.logger.warning(f"Redis error when storing refresh token: {str(e)}")
            return False
        except Exception as e:
            self.logger.error(f"Unexpected error when storing refresh token: {str(e)}")
            return False

    def login(self, username: str, password: str, response: Response = None) -> TokenResponse:
        user = self.user_service.authenticate_user(username, password)
        if not user:
            raise AuthenticationException(detail="Invalid username or password")

        # Ensure is_first_login is a boolean
        is_first_login_value = bool(user.is_first_login) if hasattr(user, 'is_first_login') else True

        access_token_payload = AccessTokenPayload(
            sub=user.username,
            type=user.type,
            user_id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            exp=0,  # Will be set by create_access_token
            is_first_login=is_first_login_value,
            location=user.location
        )

        jti = str(uuid.uuid4())
        refresh_token_payload = RefreshTokenPayload(
            sub=user.username,
            user_id=user.id,
            jti=jti,
            exp=0  # Will be set by create_refresh_token
        )

        access_token = self.create_access_token(access_token_payload)
        refresh_token = self.create_refresh_token(refresh_token_payload)

        # Set cookies if response object is provided
        if response:
            response.set_cookie(
                key="access_token",
                value=access_token,
                max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
                httponly=True,
                secure=True,
                samesite="none"
            )
            response.set_cookie(
                key="refresh_token",
                value=refresh_token,
                max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
                httponly=True,
                secure=True,
                samesite="none"
            )

        # Store refresh token in Redis
        try:
            asyncio.run(self._store_refresh_token_in_redis(user.id, refresh_token))
        except Exception as e:
            self.logger.warning(f"Failed to store refresh token asynchronously: {str(e)}")
            # Continue even if Redis storage fails - the token is still valid

        return TokenResponse(access_token=access_token, refresh_token=refresh_token)

    async def refresh_token(self, response: Response = None, request: Request = None) -> TokenResponse:
        # Get refresh token from HTTP-only cookies first
        refresh_token = request.cookies.get("refresh_token")
        
        if not refresh_token:
            raise HTTPException(status_code=401, detail="Refresh token not found in cookies or request body")

        try:
            # Decode the refresh token to get user information
            refresh_token_payload = jwt.decode(refresh_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        except jwt.JWTError:
            raise HTTPException(status_code=401, detail="Invalid refresh token")

        # Extract user_id from the refresh token payload
        user_id = refresh_token_payload.get("user_id")
        if not user_id:
            raise AuthenticationException(detail="Invalid refresh token payload")

        # Get the username from the refresh token payload
        username = refresh_token_payload.get("sub")
        if not username:
            raise AuthenticationException(detail="Invalid refresh token payload")

        # Get the user from the database
        user = self.user_service.get_user_by_username(username)
        if not user or user.id != user_id:
            raise AuthenticationException(detail="User not found or mismatched")

        # Ensure is_first_login is a boolean
        is_first_login_value = bool(user.is_first_login) if hasattr(user, 'is_first_login') else True

        # Check Redis availability and validate refresh token if possible
        redis_validation_passed = False
        
        if self.redis_client:
            try:
                # Verify the refresh token against the stored one in Redis
                stored_refresh_token = await self.redis_client.get(str(user_id))
                if stored_refresh_token and stored_refresh_token == refresh_token:
                    redis_validation_passed = True
                    self.logger.info("Refresh token validated against Redis")
                else:
                    self.logger.warning("Refresh token not found or doesn't match in Redis")
                    # Don't fail here - continue without Redis validation
            except redis.RedisError as e:
                self.logger.warning(f"Redis error during token validation: {str(e)}")
                # Continue without Redis validation
        else:
            self.logger.warning("Redis client not available - skipping refresh token validation")

        # If Redis validation failed but Redis is available, reject the request
        if self.redis_client and not redis_validation_passed:
            # Only check expiration as fallback validation
            try:
                exp = refresh_token_payload.get("exp")
                if exp and datetime.fromtimestamp(exp, tz=timezone.utc) < datetime.now(timezone.utc):
                    raise HTTPException(status_code=401, detail="Refresh token expired")
            except Exception:
                raise HTTPException(status_code=401, detail="Invalid refresh token")

        # Create new access token
        access_token_payload = AccessTokenPayload(
            sub=user.username,
            type=user.type,
            user_id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            exp=1000,  # Will be overridden by create_access_token
            is_first_login=is_first_login_value,
            location=user.location
        )

        # Create new refresh token
        jti = str(uuid.uuid4())
        refresh_token_payload = RefreshTokenPayload(
            sub=user.username,
            user_id=user.id,
            jti=jti,
            exp=1000  # Will be overridden by create_refresh_token
        )

        # Generate tokens
        new_access_token = self.create_access_token(access_token_payload)
        new_refresh_token = self.create_refresh_token(refresh_token_payload)

        # Store the new refresh token in Redis if available
        if self.redis_client:
            try:
                await self._store_refresh_token_in_redis(str(user.id), new_refresh_token)
                self.logger.info("New refresh token stored in Redis")
            except redis.RedisError as e:
                self.logger.warning(f"Failed to store new refresh token in Redis: {str(e)}")
                # Continue even if Redis storage fails
        else:
            self.logger.warning("Redis not available - new refresh token not stored")

        # Set cookies if response object is provided
        if response:
            response.set_cookie(
                key="access_token",
                value=new_access_token,
                max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
                httponly=True,
                secure=True,
                samesite="none"
            )

            response.set_cookie(
                key="refresh_token",
                value=new_refresh_token,
                max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
                httponly=True,
                secure=True,
                samesite="none"
            )

        # Return the new tokens
        return TokenResponse(access_token=new_access_token, refresh_token=new_refresh_token)

    async def logout(self, response: Response, request: Request) -> dict:
        # Try to get token from cookies first
        access_token = request.cookies.get("access_token")

        # If not in cookies, try to get from Authorization header
        if not access_token:
            auth_header = request.headers.get("Authorization")
            if auth_header and auth_header.startswith("Bearer "):
                access_token = auth_header.replace("Bearer ", "")

        # If still no access token, try to get user_id from request body
        user_id = None
        if not access_token:
            try:
                body = await request.json()
                user_id = body.get("user_id")
            except Exception:
                pass

        # If we have an access token, decode it to get user_id
        if access_token:
            try:
                access_token_payload = jwt.decode(access_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
                user_id = access_token_payload.get("user_id")
            except jwt.JWTError:
                self.logger.warning("Invalid access token during logout")
                # Continue with logout even if token is invalid

        # If we have a user_id, delete their refresh token from Redis
        if user_id and self.redis_client:
            try:
                await self.redis_client.delete(str(user_id))
                self.logger.info(f"Successfully deleted refresh token for user {user_id}")
            except redis.RedisError as e:
                self.logger.warning(f"Failed to delete refresh token from Redis: {str(e)}")

        # Clear cookies if response object is provided
        if response:
            self.logger.info("Clearing cookies in logout response")
            # Clear with path to ensure cookies are properly removed
            response.delete_cookie(
                key="access_token",
                path="/",
                domain=None,
            )
            response.delete_cookie(
                key="refresh_token",
                path="/",
                domain=None,
            )
        return {"message": "Logged out successfully"}

    def change_password(self, user, old_password: str, new_password: str):
        if not verify_password(old_password, user.password):
            raise PasswordValidationException(detail="Password is incorrect")
        user.password = hash_password(new_password)
        user.is_first_login = False
        self.db.commit()
        return {"message": "Your password has been changed successfully"}
