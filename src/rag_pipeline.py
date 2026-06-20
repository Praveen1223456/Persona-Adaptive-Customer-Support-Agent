import os
import chromadb
from google import genai
from src.config import Config

class SupportKnowledgeBase:
    def __init__(self):
        # Start the official Gemini connection
        self.ai_client = genai.Client(api_key=Config.GEMINI_API_KEY)
        
        # Open or create a local storage drawer on your hard drive
        self.db_client = chromadb.PersistentClient(path=Config.DATABASE_FOLDER)
        self.collection = self.db_client.get_or_create_collection(name="help_articles")

    def turn_text_into_numbers(self, text: str):
        """Converts text into mathematical meaning so the database can search it."""
        response = self.ai_client.models.embed_content(
            model=Config.EMBEDDING_MODEL,
            contents=text
        )
        return response.embeddings[0].values

    def add_article(self, article_name: str, full_text: str):
        """Chops a file into tiny pieces and saves them into the drawer."""
        # Simple human rule: split by double blank lines (paragraphs)
        paragraphs = [p.strip() for p in full_text.split("\n\n") if p.strip()]
        
        for index, paragraph in enumerate(paragraphs):
            math_vector = self.turn_text_into_numbers(paragraph)
            
            self.collection.add(
                ids=[f"{article_name}_{index}"],
                embeddings=[math_vector],
                documents=[paragraph],
                metadatas=[{"source": article_name}]
            )

    def search_for_answers(self, user_question: str):
        """Looks inside the drawer for the top 2 closest paragraphs matching the user's question."""
        question_vector = self.turn_text_into_numbers(user_question)
        
        results = self.collection.query(
            query_embeddings=[question_vector],
            n_results=2
        )
        
        # Format the found text nicely for our system
        found_chunks = []
        if results and results['documents'] and results['documents'][0]:
            for i in range(len(results['documents'][0])):
                # Turn distance scores into a simpler 0% to 100% confidence match
                raw_distance = results['distances'][0][i] if results['distances'] else 1.0
                confidence_match = 1.0 - raw_distance
                
                found_chunks.append({
                    "text": results['documents'][0][i],
                    "source": results['metadatas'][0][i]['source'],
                    "score": confidence_match
                })
        return found_chunks