import json
from google import genai
from src.config import Config

class SupportAgentEngine:
    def __init__(self):
        self.ai_client = genai.Client(api_key=Config.GEMINI_API_KEY)

    def figure_out_customer_feeling(self, user_message: str) -> str:
        """Identifies how the user is feeling or communicating."""
        prompt = (
            "Look at this customer support message. Classify the user into exactly one of these labels:\n"
            "- 'Technical Expert' (uses code, logs, technical jargon)\n"
            "- 'Frustrated User' (angry tone, capital letters, upset, values speed)\n"
            "- 'Business Executive' (cares about timeline, business impact, very brief)\n\n"
            f"Customer Message: \"{user_message}\"\n\n"
            "Reply with JUST the label name, nothing else."
        )
        response = self.ai_client.models.generate_content(
            model=Config.TEXT_MODEL,
            contents=prompt
        )
        cleaned_label = response.text.strip()
        if "Technical" in cleaned_label: return "Technical Expert"
        if "Frustrated" in cleaned_label: return "Frustrated User"
        return "Business Executive"

    def talk_to_customer(self, user_question: str, persona: str, found_help_docs: list) -> dict:
        """Uses Gemini to actively resolve or suggest answers matching the persona style."""
        
        # Check if it hits our predefined high-risk keyword rule
        is_urgent = any(word in user_question.lower() for word in Config.URGENT_KEYWORDS)
        
        # Check if our database search came back empty
        is_missing_docs = not found_help_docs or max([doc["score"] for doc in found_help_docs]) < 0.40

        # Dynamic Tone Instructions for Gemini
        if persona == "Technical Expert":
            tone_rule = "Be granular, analytical, skip pleasantries, and suggest technical diagnostic steps or log checks."
        elif persona == "Frustrated User":
            tone_rule = "Be deeply empathetic, apologize warmly for their long wait/trouble, keep things reassuring, and offer immediate troubleshooting advice."
        else:
            tone_rule = "Be concise, highly professional, business-outcome focused, and give clear action expectations."

        # Build context from documents if they exist
        if not is_missing_docs:
            knowledge_context = "\n\n".join([f"Document [{d['source']}]: {d['text']}" for d in found_help_docs])
            system_instructions = (
                f"You are an intelligent support agent helping a {persona}.\n"
                f"Tone Style: {tone_rule}\n"
                f"Base your answers on these official help documents:\n{knowledge_context}"
            )
        else:
            system_instructions = (
                f"You are an intelligent support agent helping a {persona}.\n"
                f"Tone Style: {tone_rule}\n"
                "CRITICAL: We don't have a specific documentation article matching this exact problem. "
                "Provide a helpful, polite support response and general troubleshooting suggestions based on your own knowledge "
                "to assist the user while we get a human support expert to look into their ticket."
            )

        # Let Gemini generate a real, smart chat response
        response = self.ai_client.models.generate_content(
            model=Config.TEXT_MODEL,
            contents=user_question,
            config={"system_instruction": system_instructions}
        )

        # Determine if we should still attach a human handoff background packet
        should_escalate = is_urgent or is_missing_docs
        handoff = None
        
        if should_escalate:
            # 1. Deduplicate our document source names cleanly
            documents_used = list(set([d["source"] for d in found_help_docs])) if found_help_docs else ["None found"]
            
            # 2. Extract logical historical attempted steps based on input content
            attempted_steps = ["User interacted with automated persona support chat router"]
            if "tried" in user_question.lower() or "everything" in user_question.lower():
                attempted_steps.append("Basic consumer troubleshooting attempted by user prior to queue entry")
            
            # 3. Formulate the human recommended action based on why it broke
            if is_urgent:
                recommendation = "Review account verification records and manually audit core financial gateway transactions."
            elif "password" in user_question.lower() or "login" in user_question.lower():
                recommendation = "Investigate account lock status flags and verify client access identification parameters."
            else:
                recommendation = "Cross-reference logs with the referenced documents used list to begin structural debugging."

            # FIX: Format the dictionary keys to EXACTLY match section 4.5 parameters
            handoff = {
                "persona": persona,
                "issue": user_question if len(user_question) < 80 else user_question[:80] + "...",
                "documents_used": documents_used,
                "attempted_steps": attempted_steps,
                "recommendation": recommendation
            }

        return {
            "escalated": should_escalate,
            "reply_text": response.text,
            "handoff_details": handoff
        }