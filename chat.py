from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
import asyncio
import json
from typing import Callable


class ChatService:
    def __init__(
            self,
            model_name: str,
            template: str = """
You are a helpful, friendly, and concise assistant.
Your primary domain is answering questions about a pizza restaurant using the provided customer reviews, but you may also answer general questions as long as your response stays relevant, safe, and helpful.

### Guidelines
1. Prioritize answering questions related to the pizza restaurant and use information from the reviews when relevant.
2. If the user asks something unrelated to the restaurant, you may answer briefly with general safe knowledge — but avoid sensitive opinions, medical, political, legal, or risky advice.
3. Do not invent facts from the reviews. If the reviews do not include the answer, respond with:
   "The reviews do not mention that, however, generally..."
   Then continue with a safe general explanation.
4. For inappropriate or harmful questions, respond safely and guide the conversation back to a positive or helpful topic.

### Customer Reviews
{reviews}

### User Question
{question}

### Your Response
Provide a short and clear answer that directly addresses the user’s question. If relevant to the reviews, include points supported by the reviews.
""",
    ):
        self.model_name = model_name
        self.template = template

        self.model = OllamaLLM(model=self.model_name)
        self.prompt = ChatPromptTemplate.from_template(self.template)
        self.chain = self.prompt | self.model

    async def streaming(self, reviews: str, question: str, func_save_memory: Callable[[str], None]):
        """streaming SSE Response"""
        
        full_response = ""
        
        for chunk in self.chain.stream({
            "reviews": reviews,
            "question": question,
        }):
            text = str(chunk)
            if not text:
                continue
            
            full_response += text

            yield f"data: {json.dumps({'token': text})}\n\n"
            await asyncio.sleep(0)

        # save to memory
        func_save_memory(full_response)
        
        # send end signal
        yield "data: [DONE]\n\n"
