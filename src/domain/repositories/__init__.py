from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Optional, List

T = TypeVar("T")


class BaseRepository(ABC, Generic[T]):
    """Base repository interface."""

    @abstractmethod
    def create(self, entity: T) -> T:
        """Create a new entity."""
        pass

    @abstractmethod
    def get_by_id(self, entity_id: int) -> Optional[T]:
        """Get an entity by ID."""
        pass

    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 100) -> List[T]:
        """Get all entities."""
        pass

    @abstractmethod
    def update(self, entity_id: int, entity: T) -> Optional[T]:
        """Update an entity."""
        pass

    @abstractmethod
    def delete(self, entity_id: int) -> bool:
        """Delete an entity."""
        pass
