from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI
from typing import List, Dict
import os

class HRKnowledgeRAG:
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        self.llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
        self.vectorstore = None
        self.qa_chain = None
        self._initialize_knowledge_base()
    
    def _initialize_knowledge_base(self):
        """Initialize RAG with Malaysian HR knowledge"""
        
        # Malaysian HR knowledge base
        hr_documents = [
            """
            Employment Act 1955 Malaysia:
            - Probation period: Maximum 6 months
            - Notice period: 4 weeks for monthly paid employees
            - Overtime: 1.5x normal rate after 8 hours
            - Annual leave: Minimum 8 days after 12 months service
            """,
            """
            EPF (Employees Provident Fund) Malaysia:
            - Employee contribution: 11% of salary
            - Employer contribution: 13% of salary (12% to Account 1, 1% to Account 2)
            - Maximum salary for EPF: RM5,000
            - Withdrawal at age 55 or earlier under specific conditions
            """,
            """
            SOCSO (Social Security Organisation) Malaysia:
            - Employee contribution: 0.5% of salary
            - Employer contribution: 1.75% of salary
            - Maximum salary for SOCSO: RM4,000
            - Covers employment injury and invalidity schemes
            """,
            """
            Malaysian Public Holidays 2024:
            - New Year: 1 January
            - Chinese New Year: 10-11 February
            - Hari Raya Puasa: 10-11 April
            - Labour Day: 1 May
            - Wesak Day: 22 May
            - Hari Raya Haji: 17 June
            - Merdeka Day: 31 August
            - Malaysia Day: 16 September
            - Deepavali: 31 October
            - Christmas: 25 December
            """,
            """
            HRDF (Human Resources Development Fund) Malaysia:
            - Levy rate: 1% of monthly payroll
            - Applicable to companies with 10+ employees
            - Training claims up to levy amount
            - Claimable training must be approved by HRDF
            """
        ]
        
        # Split documents
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50
        )
        
        texts = []
        for doc in hr_documents:
            chunks = text_splitter.split_text(doc)
            texts.extend(chunks)
        
        # Create vector store
        self.vectorstore = FAISS.from_texts(texts, self.embeddings)
        
        # Create QA chain
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.vectorstore.as_retriever(search_kwargs={"k": 3})
        )
    
    async def query_knowledge(self, question: str) -> Dict:
        """Query HR knowledge base"""
        try:
            # Get relevant documents
            docs = self.vectorstore.similarity_search(question, k=3)
            
            # Generate answer
            result = await self.qa_chain.ainvoke({"query": question})
            
            return {
                "answer": result["result"],
                "sources": [doc.page_content[:200] + "..." for doc in docs],
                "confidence": self._calculate_confidence(question, docs)
            }
        except Exception as e:
            return {
                "answer": "I'm sorry, I couldn't find relevant information for your question.",
                "sources": [],
                "confidence": 0.0,
                "error": str(e)
            }
    
    def add_document(self, content: str, metadata: Dict = None):
        """Add new document to knowledge base"""
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        chunks = text_splitter.split_text(content)
        
        # Add to existing vectorstore
        self.vectorstore.add_texts(chunks)
    
    def _calculate_confidence(self, question: str, docs: List) -> float:
        """Calculate confidence score based on document relevance"""
        if not docs:
            return 0.0
        
        # Simple confidence calculation based on keyword overlap
        question_words = set(question.lower().split())
        doc_words = set()
        
        for doc in docs:
            doc_words.update(doc.page_content.lower().split())
        
        overlap = len(question_words.intersection(doc_words))
        confidence = min(overlap / len(question_words), 1.0)
        
        return round(confidence, 2)

class SmartHRAssistant:
    def __init__(self):
        self.rag_system = HRKnowledgeRAG()
        self.llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.3)
    
    async def process_query(self, query: str, context: Dict = None) -> Dict:
        """Process HR query with RAG and context"""
        
        # First, try to get information from knowledge base
        rag_result = await self.rag_system.query_knowledge(query)
        
        # If confidence is low, use general LLM
        if rag_result.get("confidence", 0) < 0.3:
            general_response = await self._general_hr_response(query, context)
            return {
                "response": general_response,
                "source": "general_knowledge",
                "confidence": 0.5
            }
        
        return {
            "response": rag_result["answer"],
            "sources": rag_result["sources"],
            "source": "knowledge_base",
            "confidence": rag_result["confidence"]
        }
    
    async def _general_hr_response(self, query: str, context: Dict = None) -> str:
        """Generate general HR response"""
        
        system_prompt = """You are a Malaysian HR expert. Provide helpful, accurate information about:
        - Malaysian labor laws and regulations
        - EPF, SOCSO, HRDF requirements
        - HR best practices
        - Employee relations
        
        If you're not certain about specific legal requirements, recommend consulting official sources."""
        
        context_info = ""
        if context:
            context_info = f"Additional context: {context}"
        
        response = await self.llm.ainvoke([
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"{query}\n{context_info}"}
        ])
        
        return response.content