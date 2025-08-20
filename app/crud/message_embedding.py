from typing import List
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.db.models.message_embedding import MessageEmbedding
from app.schemas.message_embedding import MessageEmbeddingCreate, MessageEmbeddingGet

def create(db: Session, messageEmbedding: MessageEmbeddingCreate) -> MessageEmbedding:
	db.add(messageEmbedding)
	db.commit()
	db.refresh(messageEmbedding)
	return messageEmbedding

def get_similar(db: Session, payload: MessageEmbeddingGet):
	query = text("""
		SELECT m.sender, m.content
		FROM message m
		JOIN message_embedding me ON me.message_id = m.id
		WHERE m.conversation_id = :conv_id
		ORDER BY me.embedding <-> :qemb
		LIMIT :k;
	""")
	result = db.execute(query, {
		"conv_id": payload.conversation_id,
		"qemb": payload.embedding,
		"k": payload.k
	})
	return result.fetchall()