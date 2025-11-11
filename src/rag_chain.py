from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI

class RAGChainBuilder:
    def __init__(self, llm_model, temperature, system_prompt):
        self.llm = ChatGoogleGenerativeAI(
            model=llm_model, 
            temperature=temperature
        )
        self.system_prompt = system_prompt
        self.prompt_template = ChatPromptTemplate.from_messages([
            ("system", self.system_prompt),
            ("human", "{question}"),
        ])

    def build(self, retriever):
        chain = (
            {
                "context": retriever | RunnablePassthrough(lambda data: "\n\n".join(d.page_content for d in data)),
                "question": RunnablePassthrough(),
            }
            | self.prompt_template
            | self.llm
            | StrOutputParser()
        )
        return chain
