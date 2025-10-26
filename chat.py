from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
import asyncio
import json


class ChatService:
    def __init__(
            self,
            model_name: str,
            template: str = """
You are a helpful and concise assistant that **only** answers questions about a pizza restaurant.

### Context Rules (Follow Strictly)

1. You must restrict your answers to the topic of the pizza restaurant and the provided customer reviews.
2. If the user asks anything outside this context (e.g., unrelated topics, personal advice, math, coding, politics, health, or anything not relevant to the restaurant), you must respond with:  
   "I can only answer questions related to the pizza restaurant."
3. Base your answer only on the information provided in the reviews and the question. Do not invent facts or assume details that are not stated.
4. If the answer cannot be found in the reviews, say:  
   "The reviews do not provide that information."

### Available Customer Reviews
{reviews}

### User Question
{question}

### Your Task
Provide a short, accurate answer that directly addresses the user’s question using only the given reviews.
""",
    ):
        self.model_name = model_name
        self.template = template

        self.model = OllamaLLM(model=self.model_name)
        self.prompt = ChatPromptTemplate.from_template(self.template)
        self.chain = self.prompt | self.model

    async def streaming(self, reviews: str, question: str):
        """streaming SSE Response"""
        for chunk in self.chain.stream({
            "reviews": reviews,
            "question": question,
        }):
            text = str(chunk)
            if not text:
                continue

            yield f"data: {json.dumps({'token': text})}\n\n"
            await asyncio.sleep(0)

        # send end signal
        yield "data: [DONE]\n\n"
