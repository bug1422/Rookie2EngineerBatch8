# Repositories

This directory contains the data access layer of the application. Repositories handle all database operations and abstract the database implementation details from the rest of the application.

## Structure

Each repository should focus on a specific model/entity:

```python
from typing import Optional, List, Dict, Any
from sqlmodel import select
from database.postgres import get_session

class BaseRepository:
    def __init__(self):
        self.session = get_session()

    async def get_by_id(self, id: int) -> Optional[Model]:
        query = select(self.model).where(self.model.id == id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_all(self) -> List[Model]:
        query = select(self.model)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def create(self, data: Dict[str, Any]) -> Model:
        db_obj = self.model(**data)
        self.session.add(db_obj)
        await self.session.commit()
        await self.session.refresh(db_obj)
        return db_obj

    async def update(
        self,
        id: int,
        data: Dict[str, Any]
    ) -> Optional[Model]:
        db_obj = await self.get_by_id(id)
        if db_obj:
            for key, value in data.items():
                setattr(db_obj, key, value)
            await self.session.commit()
            await self.session.refresh(db_obj)
        return db_obj

    async def delete(self, id: int) -> bool:
        db_obj = await self.get_by_id(id)
        if db_obj:
            await self.session.delete(db_obj)
            await self.session.commit()
            return True
        return False
```

## Guidelines

1. Repository Layer Responsibilities:
   - Database CRUD operations
   - Query optimization
   - Transaction handling
   - Data mapping
   - Connection management

2. Best Practices:
   - Use type hints
   - Handle database errors appropriately
   - Use async/await for database operations
   - Implement proper transaction management
   - Use efficient queries
   - Include proper error handling

## Example Repository with Complex Queries

```python
from typing import Optional, List, Dict, Any
from sqlmodel import select, and_, or_
from datetime import datetime, timedelta

class OrderRepository(BaseRepository):
    model = Order

    async def get_orders_by_user(
        self,
        user_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> List[Order]:
        query = (
            select(self.model)
            .where(self.model.user_id == user_id)
            .offset(skip)
            .limit(limit)
            .order_by(self.model.created_at.desc())
        )
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_recent_orders(
        self,
        days: int = 30,
        status: Optional[OrderStatus] = None
    ) -> List[Order]:
        filters = [
            self.model.created_at >= datetime.utcnow() - timedelta(days=days)
        ]
        if status:
            filters.append(self.model.status == status)

        query = (
            select(self.model)
            .where(and_(*filters))
            .order_by(self.model.created_at.desc())
        )
        result = await self.session.execute(query)
        return result.scalars().all()

    async def search_orders(
        self,
        search_term: str,
        status: Optional[OrderStatus] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> List[Order]:
        filters = []
        
        # Search term filter
        if search_term:
            filters.append(or_(
                self.model.id.cast(String).like(f"%{search_term}%"),
                self.model.customer_name.ilike(f"%{search_term}%"),
                self.model.product_name.ilike(f"%{search_term}%")
            ))
        
        # Status filter
        if status:
            filters.append(self.model.status == status)
        
        # Date range filter
        if start_date:
            filters.append(self.model.created_at >= start_date)
        if end_date:
            filters.append(self.model.created_at <= end_date)

        query = (
            select(self.model)
            .where(and_(*filters))
            .order_by(self.model.created_at.desc())
        )
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_order_statistics(
        self,
        start_date: datetime,
        end_date: datetime
    ) -> Dict[str, Any]:
        query = (
            select(
                func.count().label("total_orders"),
                func.sum(self.model.total).label("total_revenue"),
                func.avg(self.model.total).label("average_order_value")
            )
            .where(
                and_(
                    self.model.created_at >= start_date,
                    self.model.created_at <= end_date,
                    self.model.status == OrderStatus.COMPLETED
                )
            )
        )
        result = await self.session.execute(query)
        return dict(result.mappings().first())
```

## Transaction Management

```python
from sqlmodel import Session
from typing import Optional, List

class UserRepository(BaseRepository):
    model = User

    async def transfer_balance(
        self,
        from_user_id: int,
        to_user_id: int,
        amount: float
    ) -> bool:
        async with self.session.begin():
            try:
                # Get users
                from_user = await self.get_by_id(from_user_id)
                to_user = await self.get_by_id(to_user_id)
                
                if not from_user or not to_user:
                    return False
                
                if from_user.balance < amount:
                    return False
                
                # Update balances
                from_user.balance -= amount
                to_user.balance += amount
                
                # Create transaction records
                transaction = Transaction(
                    from_user_id=from_user_id,
                    to_user_id=to_user_id,
                    amount=amount
                )
                self.session.add(transaction)
                
                await self.session.commit()
                return True
                
            except Exception as e:
                await self.session.rollback()
                logger.error(f"Transfer failed: {str(e)}")
                return False
```

## Bulk Operations

```python
from typing import List, Dict, Any

class ProductRepository(BaseRepository):
    model = Product

    async def bulk_create(self, items: List[Dict[str, Any]]) -> List[Product]:
        db_objects = [self.model(**item) for item in items]
        self.session.add_all(db_objects)
        await self.session.commit()
        
        for obj in db_objects:
            await self.session.refresh(obj)
        
        return db_objects

    async def bulk_update(
        self,
        items: List[Dict[str, Any]]
    ) -> List[Optional[Product]]:
        updated = []
        for item in items:
            id = item.pop("id", None)
            if id:
                updated_item = await self.update(id, item)
                updated.append(updated_item)
        return updated

    async def bulk_delete(self, ids: List[int]) -> int:
        query = (
            delete(self.model)
            .where(self.model.id.in_(ids))
        )
        result = await self.session.execute(query)
        await self.session.commit()
        return result.rowcount
```
