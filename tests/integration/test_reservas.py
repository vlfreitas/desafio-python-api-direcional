import pytest
from datetime import datetime, timedelta


@pytest.mark.integration
def test_create_reserva(client, auth_token):
    """Test creating a reserva."""
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

    # Create a reserva
    data_expiracao = (datetime.utcnow() + timedelta(days=7)).isoformat()
    reserva_data = {
        "cliente_id": cliente_id,
        "apartamento_id": apartamento_id,
        "data_expiracao": data_expiracao,
    }
    response = client.post(
        "/reservas/",
        json=reserva_data,
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert response.status_code == 201
    assert response.json()["cliente_id"] == cliente_id
    assert response.json()["apartamento_id"] == apartamento_id
    assert response.json()["ativa"] is True

    # Check that apartamento status was updated to reservado
    apartamento_check = client.get(
        f"/apartamentos/{apartamento_id}",
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert apartamento_check.json()["status"] == "reservado"


@pytest.mark.integration
def test_create_reserva_apartamento_not_disponivel(client, auth_token):
    """Test creating a reserva for an apartamento that is not available."""
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

    # Create first reserva
    data_expiracao = (datetime.utcnow() + timedelta(days=7)).isoformat()
    reserva_data = {
        "cliente_id": cliente_id,
        "apartamento_id": apartamento_id,
        "data_expiracao": data_expiracao,
    }
    client.post(
        "/reservas/",
        json=reserva_data,
        headers={"Authorization": f"Bearer {auth_token}"},
    )

    # Try to create another reserva for the same apartamento
    reserva_data2 = {
        "cliente_id": cliente_id2,
        "apartamento_id": apartamento_id,
        "data_expiracao": data_expiracao,
    }
    response = client.post(
        "/reservas/",
        json=reserva_data2,
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert response.status_code == 400


@pytest.mark.integration
def test_cancel_reserva(client, auth_token):
    """Test cancelling a reserva."""
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

    # Create a reserva
    data_expiracao = (datetime.utcnow() + timedelta(days=7)).isoformat()
    reserva_data = {
        "cliente_id": cliente_id,
        "apartamento_id": apartamento_id,
        "data_expiracao": data_expiracao,
    }
    reserva_response = client.post(
        "/reservas/",
        json=reserva_data,
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    reserva_id = reserva_response.json()["id"]

    # Cancel the reserva
    response = client.post(
        f"/reservas/{reserva_id}/cancel",
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert response.status_code == 200

    # Check that apartamento status was updated back to disponivel
    apartamento_check = client.get(
        f"/apartamentos/{apartamento_id}",
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert apartamento_check.json()["status"] == "disponivel"


@pytest.mark.integration
def test_venda_from_reserva(client, auth_token):
    """Test creating a venda from a reserved apartamento."""
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

    # Create a reserva
    data_expiracao = (datetime.utcnow() + timedelta(days=7)).isoformat()
    reserva_data = {
        "cliente_id": cliente_id,
        "apartamento_id": apartamento_id,
        "data_expiracao": data_expiracao,
    }
    client.post(
        "/reservas/",
        json=reserva_data,
        headers={"Authorization": f"Bearer {auth_token}"},
    )

    # Create a venda from the reserved apartamento
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

    # Check that apartamento status was updated to vendido
    apartamento_check = client.get(
        f"/apartamentos/{apartamento_id}",
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert apartamento_check.json()["status"] == "vendido"
