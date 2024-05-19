from sqlalchemy import event, text
from sqlalchemy.orm import Session
from sqlalchemy.sql import func

def register_listeners():
    from .models import Plant  # Import local pour éviter les dépendances circulaires

    @event.listens_for(Plant, 'after_delete')
    def upidondelte(mapper, connection, target):
        max_id = connection.execute(func.max(Plant.id)).scalar()
        if max_id:
            current_id = target.id
            for i in range(current_id + 1, max_id + 2):
                connection.execute(text(f"UPDATE plants SET id = {i-1} WHERE id = {i}"))

    @event.listens_for(Plant, 'before_insert')
    def upidoncreate(mapper, connection, target):
        max_id = connection.execute(func.max(Plant.id)).scalar()
        if max_id is not None:
            connection.execute(text(f"ALTER TABLE plants AUTO_INCREMENT = {max_id + 1}"))
