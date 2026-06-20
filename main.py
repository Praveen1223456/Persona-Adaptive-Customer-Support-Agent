from src.rag_pipeline import SupportKnowledgeBase
from src.generator import SupportAgentEngine

# Boot up our sub-systems
knowledge_base = SupportKnowledgeBase()
agent_brain = SupportAgentEngine()

def run_customer_support_pipeline(customer_message: str) -> dict:
    # 1. Figure out how the user is behaving/feeling
    detected_persona = agent_brain.figure_out_customer_feeling(customer_message)
    
    # 2. Search our data files for answers
    matched_articles = knowledge_base.search_for_answers(customer_message)
    
    # 3. Process the results (Either respond with nice tone or handoff to a human)
    final_output = agent_brain.talk_to_customer(customer_message, detected_persona, matched_articles)
    
    # Attach tracking metrics for your visual user interface to display
    final_output["detected_persona"] = detected_persona
    final_output["sources_used"] = list(set([doc["source"] for doc in matched_articles])) if matched_articles else []
    
    return final_output