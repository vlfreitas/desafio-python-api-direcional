import pytest


@pytest.mark.integration
def test_create_apartamento(client, auth_token):
    """Test creating an apartamento."""
    apartamento_data = {
        "numero": "101",
        "bloco": "A",
        "andar": 1,
        "quartos": 2,
        "area": 65.5,
        "preco": 250000.0,
    }
    response = client.post(
        "/apartamentos/",
        json=apartamento_data,
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert response.status_code == 201
    assert response.json()["numero"] == "101"
    assert response.json()["status"] == "disponivel"


@pytest.mark.integration
def test_get_apartamentos(client, auth_token):
    """Test getting all apartamentos."""
    # Create an apartamento first
    apartamento_data = {
        "numero": "101",
        "bloco": "A",
        "andar": 1,
        "quartos": 2,
        "area": 65.5,
        "preco": 250000.0,
    }
    client.post(
        "/apartamentos/",
        json=apartamento_data,
        headers={"Authorization": f"Bearer {auth_token}"},
    )

    response = client.get(
        "/apartamentos/", headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 200
    assert len(response.json()) > 0


@pytest.mark.integration
def test_check_disponibilidade(client, auth_token):
    """Test checking apartamento availability."""
    # Create an apartamento
    apartamento_data = {
        "numero": "101",
        "bloco": "A",
        "andar": 1,
        "quartos": 2,
        "area": 65.5,
        "preco": 250000.0,
    }
    create_response = client.post(
        "/apartamentos/",
        json=apartamento_data,
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    apartamento_id = create_response.json()["id"]

    # Check availability
    response = client.get(
        f"/apartamentos/{apartamento_id}/disponibilidade",
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert response.status_code == 200
    assert response.json()["disponivel"] is True


@pytest.mark.integration
def test_update_apartamento(client, auth_token):
    """Test updating an apartamento."""
    # Create an apartamento
    apartamento_data = {
        "numero": "101",
        "bloco": "A",
        "andar": 1,
        "quartos": 2,
        "area": 65.5,
        "preco": 250000.0,
    }
    create_response = client.post(
        "/apartamentos/",
        json=apartamento_data,
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    apartamento_id = create_response.json()["id"]

    # Update the apartamento
    update_data = {"preco": 280000.0}
    response = client.put(
        f"/apartamentos/{apartamento_id}",
        json=update_data,
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert response.status_code == 200
    assert response.json()["preco"] == 280000.0


@pytest.mark.integration
def test_delete_apartamento(client, auth_token):
    """Test deleting an apartamento."""
    # Create an apartamento
    apartamento_data = {
        "numero": "101",
        "bloco": "A",
        "andar": 1,
        "quartos": 2,
        "area": 65.5,
        "preco": 250000.0,
    }
    create_response = client.post(
        "/apartamentos/",
        json=apartamento_data,
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    apartamento_id = create_response.json()["id"]

    # Delete the apartamento
    response = client.delete(
        f"/apartamentos/{apartamento_id}",
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert response.status_code == 204
