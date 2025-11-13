"""
Tests automatizados para la API de autenticación.
Ejecutar con: pytest test_main.py -v
"""
import pytest
from fastapi.testclient import TestClient

from main import app
from auth import get_password_hash, verify_password

client = TestClient(app)


class TestHealthCheck:
    """Tests para el endpoint de health check."""
    
    def test_health_check(self):
        """Verifica que la API responde correctamente al health check."""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "ok"


class TestRegistration:
    """Tests para el endpoint de registro."""
    
    def test_register_valid_user(self):
        """Registra un usuario válido correctamente."""
        user_data = {
            "username": "testuser",
            "password": "securepassword123"
        }
        response = client.post("/register", json=user_data)
        assert response.status_code == 201
        assert response.json()["username"] == "testuser"
        assert response.json()["id"] is not None
    
    def test_register_duplicate_username(self):
        """No permite registrar dos usuarios con el mismo nombre."""
        user_data = {
            "username": "duplicateuser",
            "password": "securepassword123"
        }
        # Primer registro
        response1 = client.post("/register", json=user_data)
        assert response1.status_code == 201
        
        # Segundo registro con el mismo usuario
        response2 = client.post("/register", json=user_data)
        assert response2.status_code == 400
        assert "ya está registrado" in response2.json()["detail"]
    
    def test_register_short_password(self):
        """Rechaza contraseñas muy cortas."""
        user_data = {
            "username": "testuser",
            "password": "short"
        }
        response = client.post("/register", json=user_data)
        assert response.status_code == 422  # Validation error
    
    def test_register_short_username(self):
        """Rechaza nombres de usuario muy cortos."""
        user_data = {
            "username": "ab",
            "password": "securepassword123"
        }
        response = client.post("/register", json=user_data)
        assert response.status_code == 422
    
    def test_register_missing_fields(self):
        """Rechaza requests sin campos requeridos."""
        response = client.post("/register", json={})
        assert response.status_code == 422


class TestAuthentication:
    """Tests para autenticación y tokens."""
    
    @pytest.fixture(autouse=True)
    def setup_auth_user(self):
        """Crea un usuario de prueba para tests de autenticación."""
        client.post("/register", json={
            "username": "authuser",
            "password": "testpassword123"
        })
        yield
    
    def test_login_valid_credentials(self):
        """Login exitoso con credenciales válidas."""
        response = client.post(
            "/token",
            data={
                "username": "authuser",
                "password": "testpassword123"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["token_type"] == "bearer"
    
    def test_login_invalid_password(self):
        """Login falla con contraseña incorrecta."""
        response = client.post(
            "/token",
            data={
                "username": "authuser",
                "password": "wrongpassword"
            }
        )
        assert response.status_code == 401
        assert "incorrectos" in response.json()["detail"]
    
    def test_login_nonexistent_user(self):
        """Login falla para usuario no existente."""
        response = client.post(
            "/token",
            data={
                "username": "nonexistent",
                "password": "password123"
            }
        )
        assert response.status_code == 401
    
    def test_get_current_user(self):
        """Obtiene información del usuario autenticado."""
        # Primero obtenemos el token
        login_response = client.post(
            "/token",
            data={
                "username": "authuser",
                "password": "testpassword123"
            }
        )
        token = login_response.json()["access_token"]
        
        # Luego accedemos al endpoint protegido
        response = client.get(
            "/users/me",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200
        assert response.json()["username"] == "authuser"
    
    def test_get_current_user_no_token(self):
        """Falla al acceder sin token."""
        response = client.get("/users/me")
        assert response.status_code == 401  # FastAPI devuelve 401 Unauthorized sin token
    
    def test_get_current_user_invalid_token(self):
        """Falla con token inválido."""
        response = client.get(
            "/users/me",
            headers={"Authorization": "Bearer invalid_token"}
        )
        assert response.status_code == 401
    
    def test_refresh_token(self):
        """Refrescar access token funciona correctamente."""
        # Obtener tokens iniciales
        login_response = client.post(
            "/token",
            data={
                "username": "authuser",
                "password": "testpassword123"
            }
        )
        refresh_token = login_response.json()["refresh_token"]
        
        # Usar refresh token para obtener nuevo access token
        refresh_response = client.post(
            "/refresh",
            headers={"Authorization": f"Bearer {refresh_token}"}
        )
        assert refresh_response.status_code == 200
        data = refresh_response.json()
        assert "access_token" in data
        assert "refresh_token" in data


class TestPasswordHashing:
    """Tests para hashing de contraseñas."""
    
    def test_password_hashing_consistency(self):
        """El hash de la misma contraseña produce resultados diferentes (salt)."""
        from auth import get_password_hash, verify_password
        
        password = "testpassword123"
        hash1 = get_password_hash(password)
        hash2 = get_password_hash(password)
        
        # Los hashes deben ser diferentes (salt aleatorio)
        assert hash1 != hash2
        
        # Pero ambos deben verificar correctamente
        assert verify_password(password, hash1)
        assert verify_password(password, hash2)
    
    def test_password_verification_fails_for_wrong_password(self):
        """La verificación falla para contraseña incorrecta."""
        from auth import get_password_hash, verify_password
        
        password = "testpassword123"
        hash_value = get_password_hash(password)
        
        assert not verify_password("wrongpassword", hash_value)


class TestEdgeCases:
    """Tests para casos edge."""
    
    def test_special_characters_in_password(self):
        """Acepta caracteres especiales en contraseñas."""
        user_data = {
            "username": "specialuser",
            "password": "P@ssw0rd!#$%&*"
        }
        response = client.post("/register", json=user_data)
        assert response.status_code == 201
        
        # Verifica que el login funciona
        login_response = client.post(
            "/token",
            data={
                "username": "specialuser",
                "password": "P@ssw0rd!#$%&*"
            }
        )
        assert login_response.status_code == 200
    
    def test_long_username(self):
        """Rechaza usernames demasiado largos."""
        user_data = {
            "username": "a" * 100,  # Más de 50 caracteres
            "password": "securepassword123"
        }
        response = client.post("/register", json=user_data)
        assert response.status_code == 422
