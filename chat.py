from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
import asyncio
import json


class ChatService:
    def __init__(
            self,
            model_name="gpt-oss:20b",
            template: str = """
You are an expert in answering questions about a pizza restaurant

Here are some relevant reviews: {reviews}

Here is the question to answer: {question}
""",
    ):
        self.model_name = model_name
        self.template = template

        self.model = OllamaLLM(model=self.model_name)
        self.prompt = ChatPromptTemplate.from_template(self.template)
        self.chain = self.prompt | self.model

    async def streaming(self, reviews: str, question: str):
        """streaming"""
        for chunk in self.chain.stream({
            "reviews": reviews,
            "question": question,
        }):
            text = str(chunk).strip()
            if not text:
                continue

            yield f"data: {json.dumps({'token': chunk})}\n\n"
            await asyncio.sleep(0)
