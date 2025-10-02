import pytest


@pytest.mark.integration
def test_create_cliente(client, auth_token):
    """Test creating a cliente."""
    cliente_data = {
        "nome": "João Silva",
        "cpf": "12345678901",
        "email": "joao@example.com",
        "telefone": "11999999999",
    }
    response = client.post(
        "/clientes/",
        json=cliente_data,
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert response.status_code == 201
    assert response.json()["nome"] == "João Silva"
    assert response.json()["cpf"] == "12345678901"


@pytest.mark.integration
def test_create_cliente_duplicate_cpf(client, auth_token):
    """Test creating a cliente with duplicate CPF."""
    cliente_data = {
        "nome": "João Silva",
        "cpf": "12345678901",
        "email": "joao@example.com",
        "telefone": "11999999999",
    }
    client.post(
        "/clientes/",
        json=cliente_data,
        headers={"Authorization": f"Bearer {auth_token}"},
    )

    # Try to create another cliente with same CPF
    cliente_data2 = {
        "nome": "Maria Silva",
        "cpf": "12345678901",
        "email": "maria@example.com",
        "telefone": "11888888888",
    }
    response = client.post(
        "/clientes/",
        json=cliente_data2,
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert response.status_code == 400
    assert "already exists" in response.json()["detail"].lower()


@pytest.mark.integration
def test_get_clientes(client, auth_token):
    """Test getting all clientes."""
    # Create a cliente first
    cliente_data = {
        "nome": "João Silva",
        "cpf": "12345678901",
        "email": "joao@example.com",
        "telefone": "11999999999",
    }
    client.post(
        "/clientes/",
        json=cliente_data,
        headers={"Authorization": f"Bearer {auth_token}"},
    )

    response = client.get(
        "/clientes/", headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 200
    assert len(response.json()) > 0


@pytest.mark.integration
def test_get_cliente_by_id(client, auth_token):
    """Test getting a cliente by ID."""
    # Create a cliente
    cliente_data = {
        "nome": "João Silva",
        "cpf": "12345678901",
        "email": "joao@example.com",
        "telefone": "11999999999",
    }
    create_response = client.post(
        "/clientes/",
        json=cliente_data,
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    cliente_id = create_response.json()["id"]

    # Get the cliente
    response = client.get(
        f"/clientes/{cliente_id}",
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert response.status_code == 200
    assert response.json()["id"] == cliente_id


@pytest.mark.integration
def test_update_cliente(client, auth_token):
    """Test updating a cliente."""
    # Create a cliente
    cliente_data = {
        "nome": "João Silva",
        "cpf": "12345678901",
        "email": "joao@example.com",
        "telefone": "11999999999",
    }
    create_response = client.post(
        "/clientes/",
        json=cliente_data,
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    cliente_id = create_response.json()["id"]

    # Update the cliente
    update_data = {"nome": "João Silva Updated"}
    response = client.put(
        f"/clientes/{cliente_id}",
        json=update_data,
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert response.status_code == 200
    assert response.json()["nome"] == "João Silva Updated"


@pytest.mark.integration
def test_delete_cliente(client, auth_token):
    """Test deleting a cliente."""
    # Create a cliente
    cliente_data = {
        "nome": "João Silva",
        "cpf": "12345678901",
        "email": "joao@example.com",
        "telefone": "11999999999",
    }
    create_response = client.post(
        "/clientes/",
        json=cliente_data,
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    cliente_id = create_response.json()["id"]

    # Delete the cliente
    response = client.delete(
        f"/clientes/{cliente_id}",
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert response.status_code == 204


@pytest.mark.integration
def test_unauthorized_access(client):
    """Test accessing clientes without authentication."""
    response = client.get("/clientes/")
    assert response.status_code == 401
