import pytest
from unittest.mock import Mock
from src.application.use_cases.venda_service import VendaService
from src.application.dtos import VendaCreate
from src.infrastructure.database.models import Venda, Cliente, Apartamento
from src.infrastructure.database.models.apartamento import StatusApartamento


@pytest.mark.unit
def test_create_venda_success():
    """Test creating a venda successfully."""
    # Arrange
    mock_db = Mock()
    mock_venda_repo = Mock()
    mock_apartamento_repo = Mock()
    mock_cliente_repo = Mock()

    venda_data = VendaCreate(
        cliente_id=1,
        apartamento_id=1,
        valor_venda=250000.0,
        valor_entrada=50000.0
    )

    # Mock cliente exists
    mock_cliente_repo.get_by_id.return_value = Cliente(
        id=1,
        nome="Test Client",
        cpf="12345678901",
        email="test@example.com",
        telefone="11999999999"
    )

    # Mock apartamento exists and is available
    mock_apartamento_repo.get_by_id.return_value = Apartamento(
        id=1,
        numero="101",
        bloco="A",
        andar=1,
        quartos=2,
        area=65.5,
        preco=250000.0,
        status=StatusApartamento.DISPONIVEL
    )

    # Mock no existing venda
    mock_venda_repo.get_by_apartamento_id.return_value = None

    # Mock venda creation
    mock_venda_repo.create.return_value = Venda(
        id=1,
        cliente_id=1,
        apartamento_id=1,
        valor_venda=250000.0,
        valor_entrada=50000.0
    )

    # Act
    service = VendaService(mock_db)
    service.venda_repo = mock_venda_repo
    service.apartamento_repo = mock_apartamento_repo
    service.cliente_repo = mock_cliente_repo

    result = service.create_venda(venda_data)

    # Assert
    assert result.cliente_id == 1
    assert result.apartamento_id == 1
    mock_apartamento_repo.update_status.assert_called_once_with(1, StatusApartamento.VENDIDO)


@pytest.mark.unit
def test_create_venda_cliente_not_found():
    """Test creating venda with non-existent cliente."""
    # Arrange
    mock_db = Mock()
    mock_venda_repo = Mock()
    mock_apartamento_repo = Mock()
    mock_cliente_repo = Mock()

    venda_data = VendaCreate(
        cliente_id=999,
        apartamento_id=1,
        valor_venda=250000.0,
        valor_entrada=50000.0
    )

    mock_cliente_repo.get_by_id.return_value = None

    # Act & Assert
    service = VendaService(mock_db)
    service.venda_repo = mock_venda_repo
    service.apartamento_repo = mock_apartamento_repo
    service.cliente_repo = mock_cliente_repo

    with pytest.raises(ValueError, match="Cliente not found"):
        service.create_venda(venda_data)


@pytest.mark.unit
def test_create_venda_apartamento_not_found():
    """Test creating venda with non-existent apartamento."""
    # Arrange
    mock_db = Mock()
    mock_venda_repo = Mock()
    mock_apartamento_repo = Mock()
    mock_cliente_repo = Mock()

    venda_data = VendaCreate(
        cliente_id=1,
        apartamento_id=999,
        valor_venda=250000.0,
        valor_entrada=50000.0
    )

    mock_cliente_repo.get_by_id.return_value = Cliente(
        id=1,
        nome="Test Client",
        cpf="12345678901",
        email="test@example.com",
        telefone="11999999999"
    )

    mock_apartamento_repo.get_by_id.return_value = None

    # Act & Assert
    service = VendaService(mock_db)
    service.venda_repo = mock_venda_repo
    service.apartamento_repo = mock_apartamento_repo
    service.cliente_repo = mock_cliente_repo

    with pytest.raises(ValueError, match="Apartamento not found"):
        service.create_venda(venda_data)


@pytest.mark.unit
def test_create_venda_apartamento_already_sold():
    """Test creating venda for already sold apartamento."""
    # Arrange
    mock_db = Mock()
    mock_venda_repo = Mock()
    mock_apartamento_repo = Mock()
    mock_cliente_repo = Mock()

    venda_data = VendaCreate(
        cliente_id=1,
        apartamento_id=1,
        valor_venda=250000.0,
        valor_entrada=50000.0
    )

    mock_cliente_repo.get_by_id.return_value = Cliente(
        id=1,
        nome="Test Client",
        cpf="12345678901",
        email="test@example.com",
        telefone="11999999999"
    )

    # Apartamento already sold
    mock_apartamento_repo.get_by_id.return_value = Apartamento(
        id=1,
        numero="101",
        bloco="A",
        andar=1,
        quartos=2,
        area=65.5,
        preco=250000.0,
        status=StatusApartamento.VENDIDO
    )

    # Act & Assert
    service = VendaService(mock_db)
    service.venda_repo = mock_venda_repo
    service.apartamento_repo = mock_apartamento_repo
    service.cliente_repo = mock_cliente_repo

    with pytest.raises(ValueError, match="not available for sale"):
        service.create_venda(venda_data)


@pytest.mark.unit
def test_create_venda_duplicate():
    """Test creating duplicate venda."""
    # Arrange
    mock_db = Mock()
    mock_venda_repo = Mock()
    mock_apartamento_repo = Mock()
    mock_cliente_repo = Mock()

    venda_data = VendaCreate(
        cliente_id=1,
        apartamento_id=1,
        valor_venda=250000.0,
        valor_entrada=50000.0
    )

    mock_cliente_repo.get_by_id.return_value = Cliente(
        id=1,
        nome="Test Client",
        cpf="12345678901",
        email="test@example.com",
        telefone="11999999999"
    )

    mock_apartamento_repo.get_by_id.return_value = Apartamento(
        id=1,
        numero="101",
        bloco="A",
        andar=1,
        quartos=2,
        area=65.5,
        preco=250000.0,
        status=StatusApartamento.DISPONIVEL
    )

    # Venda already exists
    mock_venda_repo.get_by_apartamento_id.return_value = Venda(
        id=1,
        cliente_id=2,
        apartamento_id=1,
        valor_venda=250000.0,
        valor_entrada=50000.0
    )

    # Act & Assert
    service = VendaService(mock_db)
    service.venda_repo = mock_venda_repo
    service.apartamento_repo = mock_apartamento_repo
    service.cliente_repo = mock_cliente_repo

    with pytest.raises(ValueError, match="already sold"):
        service.create_venda(venda_data)


@pytest.mark.unit
def test_create_venda_from_reserva():
    """Test creating venda from reserved apartamento."""
    # Arrange
    mock_db = Mock()
    mock_venda_repo = Mock()
    mock_apartamento_repo = Mock()
    mock_cliente_repo = Mock()

    venda_data = VendaCreate(
        cliente_id=1,
        apartamento_id=1,
        valor_venda=250000.0,
        valor_entrada=50000.0
    )

    mock_cliente_repo.get_by_id.return_value = Cliente(
        id=1,
        nome="Test Client",
        cpf="12345678901",
        email="test@example.com",
        telefone="11999999999"
    )

    # Apartamento is reserved
    mock_apartamento_repo.get_by_id.return_value = Apartamento(
        id=1,
        numero="101",
        bloco="A",
        andar=1,
        quartos=2,
        area=65.5,
        preco=250000.0,
        status=StatusApartamento.RESERVADO
    )

    mock_venda_repo.get_by_apartamento_id.return_value = None

    mock_venda_repo.create.return_value = Venda(
        id=1,
        cliente_id=1,
        apartamento_id=1,
        valor_venda=250000.0,
        valor_entrada=50000.0
    )

    # Act
    service = VendaService(mock_db)
    service.venda_repo = mock_venda_repo
    service.apartamento_repo = mock_apartamento_repo
    service.cliente_repo = mock_cliente_repo

    result = service.create_venda(venda_data)

    # Assert
    assert result is not None
    mock_apartamento_repo.update_status.assert_called_once_with(1, StatusApartamento.VENDIDO)
