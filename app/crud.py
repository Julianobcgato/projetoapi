from typing import List, Optional
from app import models

items_db = []

def create_item(item: models.ItemCreate) -> models.Item:
    item_id = len(items_db) + 1
    new_item = models.Item(id=item_id, **item.dict())
    items_db.append(new_item)
    return new_item

def get_items() -> List[models.Item]:
    return items_db

def get_item(item_id: int) -> Optional[models.Item]:
    for item in items_db:
        if item.id == item_id:
            return item
    return None

def update_item(item_id: int, item: models.ItemUpdate) -> Optional[models.Item]:
    for idx, existing_item in enumerate(items_db):
        if existing_item.id == item_id:
            updated_item = existing_item.copy(update=item.dict(exclude_unset=True))
            items_db[idx] = updated_item
            return updated_item
    return None

def delete_item(item_id: int) -> bool:
    global items_db
    items_db = [item for item in items_db if item.id != item_id]
    return True

