from typing import List
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.db.models.message_embedding import MessageEmbedding
from app.schemas.message_embedding import MessageEmbeddingCreate, MessageEmbeddingGet

def create(db: Session, messageEmbedding: MessageEmbeddingCreate) -> MessageEmbedding:
	db_embedding = MessageEmbedding(
        message_id=messageEmbedding.message_id,
        embedding=messageEmbedding.embedding
    )
	db.add(db_embedding)
	db.commit()
	db.refresh(db_embedding)
	return db_embedding

def get_similar(db: Session, payload: MessageEmbeddingGet):
	query = text("""
		SELECT m.role, m.content
		FROM messages m
		JOIN message_embeddings me ON me.message_id = m.id
		WHERE m.conversation_id = :conv_id
		ORDER BY me.embedding <-> CAST(:qemb AS vector)
		LIMIT :k;
	""")
	result = db.execute(query, {
		"conv_id": payload.conversation_id,
		"qemb": payload.embedding,
		"k": payload.k
	})
	return result.fetchall()