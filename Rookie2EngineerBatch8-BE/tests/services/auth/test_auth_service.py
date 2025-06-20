from datetime import datetime, timezone, timedelta
from jose import jwt
from core.config import settings
from services.auth import AuthService, AuthenticationException, HTTPException, PasswordValidationException
from schemas.auth import TokenResponse
from unittest.mock import MagicMock
import pytest

class TestAuthService:
    def test_create_access_token(self, mock_access_token_data):
        """Test basic functionality of create_access_token"""
        # Arrange
        current_time = datetime.now(timezone.utc)
        expected_exp = int((current_time + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)).timestamp())
        
        # Act
        token = AuthService.create_access_token(mock_access_token_data)
        decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        
        # Assert
        # Token format
        assert isinstance(token, str)
        assert len(token) > 0
        
        # Required claims
        assert "sub" in decoded
        assert "exp" in decoded
        assert "user_id" in decoded
        
        # Token data
        assert decoded["sub"] == mock_access_token_data["sub"]
        assert decoded["user_id"] == mock_access_token_data["user_id"]
        assert decoded["type"] == mock_access_token_data["type"]
        assert decoded["is_first_login"] == mock_access_token_data["is_first_login"]
        assert decoded["location"] == mock_access_token_data["location"]
        
        # Expiration time
        assert decoded["exp"] > current_time.timestamp()
        assert decoded["exp"] == expected_exp

    def test_create_access_token_with_payload(self, mock_access_token_payload):
        """Test creating access token with AccessTokenPayload"""
        # Arrange
        expected_payload = {
            "sub": mock_access_token_payload.sub,
            "user_id": mock_access_token_payload.user_id,
            "first_name": mock_access_token_payload.first_name,
            "last_name": mock_access_token_payload.last_name,
            "type": mock_access_token_payload.type.value,
            "is_first_login": mock_access_token_payload.is_first_login,
            "location": mock_access_token_payload.location.value
        }
        
        # Act
        token = AuthService.create_access_token(mock_access_token_payload)
        decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        
        # Assert
        for key, value in expected_payload.items():
            assert decoded[key] == value
        
    def test_create_access_token_with_dict(self, mock_access_token_data):
        """Test creating access token with dictionary data"""
        # Arrange
        current_time = datetime.now(timezone.utc)
        expected_exp = int((current_time + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)).timestamp())
        
        # Act
        token = AuthService.create_access_token(mock_access_token_data)
        decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        
        # Assert
        for key, value in mock_access_token_data.items():
            assert decoded[key] == value
        assert decoded["exp"] == expected_exp
            
    def test_create_access_token_custom_expiry(self, mock_access_token_data, mock_custom_expiry_delta):
        """Test creating access token with custom expiry time"""
        # Arrange
        current_time = datetime.now(timezone.utc)
        expected_exp = int((current_time + mock_custom_expiry_delta).timestamp())
            
        # Act
        token = AuthService.create_access_token(mock_access_token_data, mock_custom_expiry_delta)
        decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        
        # Assert
        for key, value in mock_access_token_data.items():
            assert decoded[key] == value
        assert decoded["exp"] == expected_exp

    def test_create_refresh_token(self, mock_refresh_token_data):
        """Test creating refresh token"""
        # Arrange
        current_time = datetime.now(timezone.utc)
        expected_exp = int((current_time + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)).timestamp())
        
        # Act
        token = AuthService.create_refresh_token(mock_refresh_token_data)
        decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        
        # Assert
        # Token format
        assert isinstance(token, str)
        assert len(token) > 0
        
        # Required claims
        assert "sub" in decoded
        assert "exp" in decoded
        assert "user_id" in decoded
        assert "jti" in decoded
        
        # Token data
        assert decoded["sub"] == mock_refresh_token_data["sub"]
        assert decoded["user_id"] == mock_refresh_token_data["user_id"]
        assert decoded["jti"] == mock_refresh_token_data["jti"]
        
        # Expiration time
        assert decoded["exp"] > current_time.timestamp()
        assert decoded["exp"] == expected_exp

    def test_create_refresh_token_with_payload(self, mock_refresh_token_payload):
        """Test creating refresh token with RefreshTokenPayload"""
        # Arrange
        expected_payload = {
            "sub": mock_refresh_token_payload.sub,
            "user_id": mock_refresh_token_payload.user_id,
            "jti": mock_refresh_token_payload.jti
        }
        
        # Act
        token = AuthService.create_refresh_token(mock_refresh_token_payload)
        decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        
        # Assert
        for key, value in expected_payload.items():
            assert decoded[key] == value
        
    def test_create_refresh_token_custom_expiry(self, mock_refresh_token_data, mock_custom_expiry_delta):
        """Test creating refresh token with custom expiry time"""
        # Arrange
        current_time = datetime.now(timezone.utc)
        expected_exp = int((current_time + mock_custom_expiry_delta).timestamp())
            
        # Act
        token = AuthService.create_refresh_token(mock_refresh_token_data, mock_custom_expiry_delta)
        decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        
        # Assert
        for key, value in mock_refresh_token_data.items():
            assert decoded[key] == value
        assert decoded["exp"] == expected_exp
    
    def test_login_success(self, user_service, mock_current_user):
        # Arrange
        response = MagicMock()
        
        # Mock the authenticate_user method
        user_service.authenticate_user = MagicMock()
        user_service.authenticate_user.return_value = mock_current_user
        
        # Create AuthService instance with mocked dependencies
        auth_service = AuthService(MagicMock())
        auth_service.user_service = user_service
        auth_service.redis_client = MagicMock()
        
        # Act
        result = auth_service.login("testuser", "password", response)
        
        # Assert
        # Check if user authentication was called
        user_service.authenticate_user.assert_called_once_with("testuser", "password")
        
        # Verify return type and token presence
        assert isinstance(result, TokenResponse)
        assert result.access_token is not None
        assert result.refresh_token is not None
        
        # Verify cookies were set
        response.set_cookie.assert_any_call(
            key="access_token",
            value=result.access_token,
            max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            httponly=True,
            secure=True,
            samesite="none"
        )
        response.set_cookie.assert_any_call(
            key="refresh_token",
            value=result.refresh_token,
            max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
            httponly=True,
            secure=True,
            samesite="none"
        )
        
        # Decode and verify access token contents
        decoded_access = jwt.decode(result.access_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        assert decoded_access["sub"] == mock_current_user.username
        assert decoded_access["user_id"] == mock_current_user.id
        assert decoded_access["type"] == mock_current_user.type
        assert decoded_access["first_name"] == mock_current_user.first_name
        assert decoded_access["last_name"] == mock_current_user.last_name
        assert decoded_access["is_first_login"] == mock_current_user.is_first_login
        assert decoded_access["location"] == mock_current_user.location
        assert "exp" in decoded_access
        
        # Decode and verify refresh token contents
        decoded_refresh = jwt.decode(result.refresh_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        assert decoded_refresh["sub"] == mock_current_user.username
        assert decoded_refresh["user_id"] == mock_current_user.id
        assert "jti" in decoded_refresh
        assert "exp" in decoded_refresh
    
    def test_login_invalid_credentials(self, user_service):
        # Arrange
        response = MagicMock()
        
        # Mock the authenticate_user method
        user_service.authenticate_user = MagicMock()
        user_service.authenticate_user.return_value = None
        
        # Act & Assert
        with pytest.raises(AuthenticationException, match="Invalid username or password"):
            AuthService(MagicMock()).login("testuser", "password", response)
    
    @pytest.mark.asyncio
    async def test_refresh_token_success(self, user_service, mock_current_user, mock_refresh_token_payload, mocker):
        # Arrange
        response = MagicMock()
        request = MagicMock()
        old_refresh_token = "valid_token"
        request.cookies = {"refresh_token": old_refresh_token}
        
        # Mock JWT decode to return valid payload as dict
        current_time = datetime.now(timezone.utc)
        mock_payload_dict = {
            "sub": mock_refresh_token_payload.sub,
            "user_id": mock_refresh_token_payload.user_id,
            "jti": mock_refresh_token_payload.jti,
            "exp": int((current_time + timedelta(days=7)).timestamp())  # Set explicit expiration
        }
        
        # Create auth service instance with redis_client set to None
        auth_service = AuthService(MagicMock())
        auth_service.redis_client = None  # Explicitly set redis_client to None
        
        # Mock JWT decode
        decode_mock = mocker.patch("jose.jwt.decode")
        decode_mock.return_value = mock_payload_dict
        
        # Mock user service
        mocker.patch("services.user.UserService.get_user_by_username", return_value=mock_current_user)
        
        # Act
        result = await auth_service.refresh_token(response, request)
        
        # Assert
        assert isinstance(result, TokenResponse)
        assert result.access_token is not None
        assert result.refresh_token is not None
        assert result.refresh_token != old_refresh_token  # New token should be different
        
        # Verify cookies were set
        response.set_cookie.assert_any_call(
            key="access_token",
            value=result.access_token,
            max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            httponly=True,
            secure=True,
            samesite="none"
        )
        response.set_cookie.assert_any_call(
            key="refresh_token",
            value=result.refresh_token,
            max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
            httponly=True,
            secure=True,
            samesite="none"
        )
    
    @pytest.mark.asyncio
    async def test_refresh_token_no_token(self, mocker):
        # Arrange
        response = MagicMock()
        request = MagicMock()
        request.cookies = {}
        
        # Act & Assert
        with pytest.raises(HTTPException, match="Refresh token not found in cookies or request body"):
            await AuthService(MagicMock()).refresh_token(response, request)
    
    @pytest.mark.asyncio
    async def test_refresh_token_invalid_token(self, mocker):
        # Arrange
        response = MagicMock()
        request = MagicMock()
        request.cookies = {"refresh_token": "invalid_token"}
        
        # Mock JWT decode to raise JWTError
        mocker.patch("jose.jwt.decode", side_effect=jwt.JWTError("Invalid token"))
        
        # Act & Assert
        with pytest.raises(HTTPException, match="Invalid refresh token"):
            await AuthService(MagicMock()).refresh_token(response, request)
    
    @pytest.mark.asyncio
    async def test_refresh_token_invalid_user_id_payload(self, mocker, mock_current_user):
        # Arrange
        response = MagicMock()
        request = MagicMock()
        request.cookies = {"refresh_token": "valid_token"}
        
        # Mock JWT decode to return payload without user_id
        mock_payload = {
            "sub": mock_current_user.username,
            "jti": "test-jti",
            "exp": int((datetime.now(timezone.utc) + timedelta(days=7)).timestamp())
        }
        mocker.patch("jose.jwt.decode", return_value=mock_payload)
        
        # Act & Assert
        with pytest.raises(AuthenticationException, match="Invalid refresh token payload"):
            await AuthService(MagicMock()).refresh_token(response, request)
    
    @pytest.mark.asyncio
    async def test_refresh_token_invalid_username_payload(self, mocker, mock_current_user):
        # Arrange
        response = MagicMock()
        request = MagicMock()
        request.cookies = {"refresh_token": "valid_token"}
        
        # Mock JWT decode to return payload with user_id but without username (sub)
        mock_payload = {
            "user_id": mock_current_user.id,
            "jti": "test-jti",
            "exp": int((datetime.now(timezone.utc) + timedelta(days=7)).timestamp())
        }
        mocker.patch("jose.jwt.decode", return_value=mock_payload)
        
        # Mock user service to return None (user not found)
        mocker.patch("services.user.UserService.get_user_by_username", return_value=None)
        
        # Act & Assert
        with pytest.raises(AuthenticationException, match="Invalid refresh token payload"):
            await AuthService(MagicMock()).refresh_token(response, request)
    
    @pytest.mark.asyncio
    async def test_logout(self):
        """Test logout with access token in cookie"""
        # Arrange
        response = MagicMock()
        request = MagicMock()
        request.cookies = {"access_token": "valid_token"}
        
        # Act
        result = await AuthService(MagicMock()).logout(response, request)
        
        # Assert
        assert result == {"message": "Logged out successfully"}
        response.delete_cookie.assert_any_call(key="access_token", path="/", domain=None)
        response.delete_cookie.assert_any_call(key="refresh_token", path="/", domain=None)
    
    def test_change_password_success(self, mocker):
        # Arrange
        user = MagicMock()
        user.password = "hashed_old_password"
        user.is_first_login = True
        db = MagicMock()
        
        # Mock password verification to return True
        mocker.patch("services.auth.verify_password", return_value=True)
        
        # Mock password hashing
        mocker.patch("services.auth.hash_password", return_value="hashed_new_password")
        
        # Act
        result = AuthService(db).change_password(user, "old_password", "new_password")
        
        # Assert
        assert result == {"message": "Your password has been changed successfully"}
        assert user.is_first_login is False
        assert user.password == "hashed_new_password"
        db.commit.assert_called_once()
    
    def test_change_password_invalid_old_password(self, mocker):
        # Arrange
        user = MagicMock()
        user.password = "hashed_old_password"
        user.is_first_login = True
        db = MagicMock()
        
        # Mock password verification to return False
        mocker.patch("services.auth.verify_password", return_value=False)
        
        # Act & Assert
        with pytest.raises(PasswordValidationException, match="Password is incorrect"):
            AuthService(db).change_password(user, "old_password", "new_password")
    