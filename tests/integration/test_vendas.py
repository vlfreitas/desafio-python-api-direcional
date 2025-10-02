import pytest


@pytest.mark.integration
def test_create_venda(client, auth_token):
    """Test creating a venda."""
    # Create a cliente
    cliente_data = {
        "nome": "João Silva",
        "cpf": "12345678901",
        "email": "joao@example.com",
        "telefone": "11999999999",
    }
    cliente_response = client.post(
        "/clientes/",
        json=cliente_data,
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    cliente_id = cliente_response.json()["id"]

    # Create an apartamento
    apartamento_data = {
        "numero": "101",
        "bloco": "A",
        "andar": 1,
        "quartos": 2,
        "area": 65.5,
        "preco": 250000.0,
    }
    apartamento_response = client.post(
        "/apartamentos/",
        json=apartamento_data,
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    apartamento_id = apartamento_response.json()["id"]

    # Create a venda
    venda_data = {
        "cliente_id": cliente_id,
        "apartamento_id": apartamento_id,
        "valor_venda": 250000.0,
        "valor_entrada": 50000.0,
    }
    response = client.post(
        "/vendas/",
        json=venda_data,
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert response.status_code == 201
    assert response.json()["cliente_id"] == cliente_id
    assert response.json()["apartamento_id"] == apartamento_id

    # Check that apartamento status was updated
    apartamento_check = client.get(
        f"/apartamentos/{apartamento_id}",
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert apartamento_check.json()["status"] == "vendido"


@pytest.mark.integration
def test_create_venda_apartamento_already_sold(client, auth_token):
    """Test creating a venda for an already sold apartamento."""
    # Create a cliente
    cliente_data = {
        "nome": "João Silva",
        "cpf": "12345678901",
        "email": "joao@example.com",
        "telefone": "11999999999",
    }
    cliente_response = client.post(
        "/clientes/",
        json=cliente_data,
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    cliente_id = cliente_response.json()["id"]

    # Create another cliente
    cliente_data2 = {
        "nome": "Maria Silva",
        "cpf": "98765432109",
        "email": "maria@example.com",
        "telefone": "11888888888",
    }
    cliente_response2 = client.post(
        "/clientes/",
        json=cliente_data2,
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    cliente_id2 = cliente_response2.json()["id"]

    # Create an apartamento
    apartamento_data = {
        "numero": "101",
        "bloco": "A",
        "andar": 1,
        "quartos": 2,
        "area": 65.5,
        "preco": 250000.0,
    }
    apartamento_response = client.post(
        "/apartamentos/",
        json=apartamento_data,
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    apartamento_id = apartamento_response.json()["id"]

    # Create first venda
    venda_data = {
        "cliente_id": cliente_id,
        "apartamento_id": apartamento_id,
        "valor_venda": 250000.0,
        "valor_entrada": 50000.0,
    }
    client.post(
        "/vendas/",
        json=venda_data,
        headers={"Authorization": f"Bearer {auth_token}"},
    )

    # Try to create another venda for the same apartamento
    venda_data2 = {
        "cliente_id": cliente_id2,
        "apartamento_id": apartamento_id,
        "valor_venda": 250000.0,
        "valor_entrada": 50000.0,
    }
    response = client.post(
        "/vendas/",
        json=venda_data2,
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert response.status_code == 400


@pytest.mark.integration
def test_get_vendas(client, auth_token):
    """Test getting all vendas."""
    # Create a cliente and apartamento first
    cliente_data = {
        "nome": "João Silva",
        "cpf": "12345678901",
        "email": "joao@example.com",
        "telefone": "11999999999",
    }
    cliente_response = client.post(
        "/clientes/",
        json=cliente_data,
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    cliente_id = cliente_response.json()["id"]

    apartamento_data = {
        "numero": "101",
        "bloco": "A",
        "andar": 1,
        "quartos": 2,
        "area": 65.5,
        "preco": 250000.0,
    }
    apartamento_response = client.post(
        "/apartamentos/",
        json=apartamento_data,
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    apartamento_id = apartamento_response.json()["id"]

    # Create a venda
    venda_data = {
        "cliente_id": cliente_id,
        "apartamento_id": apartamento_id,
        "valor_venda": 250000.0,
        "valor_entrada": 50000.0,
    }
    client.post(
        "/vendas/",
        json=venda_data,
        headers={"Authorization": f"Bearer {auth_token}"},
    )

    # Get all vendas
    response = client.get(
        "/vendas/", headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 200
    assert len(response.json()) > 0
