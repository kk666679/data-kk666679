# langchain_demo.py
from langchain.chains import LLMChain, RetrievalQA, ConversationChain
from langchain.llms import OpenAI, HuggingFaceHub
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory, ConversationBufferWindowMemory
from langchain.document_loaders import WebBaseLoader, TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings, HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.agents import initialize_agent, Tool, AgentType
from langchain.tools import DuckDuckGoSearchRun
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage
import os

# Set your API keys from environment variables
if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("OPENAI_API_KEY environment variable is required")
# os.environ["HUGGINGFACEHUB_API_TOKEN"] = os.getenv("HUGGINGFACEHUB_API_TOKEN")

def basic_llm_chain():
    """Basic LLM chain with prompt template"""
    print("\n=== Basic LLM Chain ===")
    
    # Create a prompt template
    template = """You are a helpful assistant that translates {input_language} to {output_language}.
    
    Text to translate: {text}
    Translation:"""
    
    prompt = PromptTemplate(
        input_variables=["input_language", "output_language", "text"],
        template=template,
    )
    
    # Initialize LLM
    llm = OpenAI(temperature=0.7)
    
    # Create chain
    chain = LLMChain(llm=llm, prompt=prompt)
    
    # Run the chain
    result = chain.run(
        input_language="English",
        output_language="French",
        text="Hello, how are you today?"
    )
    
    print("Translation result:", result)

def document_qa_chain():
    """Document question answering with retrieval"""
    print("\n=== Document QA Chain ===")
    
    try:
        # Load document (can be replaced with any document loader)
        loader = WebBaseLoader("https://en.wikipedia.org/wiki/Large_language_model")
        documents = loader.load()
        
        # Split text
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        texts = text_splitter.split_documents(documents)
        
        # Create embeddings and vector store
        embeddings = OpenAIEmbeddings()
        # Alternative: embeddings = HuggingFaceEmbeddings()
        db = FAISS.from_documents(texts, embeddings)
        retriever = db.as_retriever()
        
        # Create QA chain
        qa = RetrievalQA.from_chain_type(
            llm=OpenAI(),
            chain_type="stuff",
            retriever=retriever,
            return_source_documents=True
        )
        
        # Ask a question
        query = "What are large language models?"
        result = qa({"query": query})
        
        print("Question:", query)
        print("Answer:", result["result"])
        print("Source documents:", result["source_documents"][0].page_content[:200] + "...")
    except Exception as e:
        print(f"Error in document QA chain: {e}")

def conversational_agent():
    """Conversational agent with memory"""
    print("\n=== Conversational Agent ===")
    
    try:
        # Initialize LLM
        llm = ChatOpenAI(temperature=0)
        
        # Define tools
        search = DuckDuckGoSearchRun()
        tools = [
            Tool(
                name="Current Search",
                func=search.run,
                description="Useful for when you need to answer questions about current events"
            ),
        ]
        
        # Create agent
        agent = initialize_agent(
            tools,
            llm,
            agent=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True,
            memory=ConversationBufferMemory(memory_key="chat_history", return_messages=True),
            agent_kwargs={
                "system_message": SystemMessage(content="You are a helpful assistant.")
            }
        )
        
        # Run the agent
        print(agent.run("What's the latest news about AI?"))
        print(agent.run("Tell me more about the first item you mentioned."))
    except Exception as e:
        print(f"Error in conversational agent: {e}")

def conversation_with_memory():
    """Conversation chain with memory"""
    print("\n=== Conversation with Memory ===")
    
    # Initialize LLM
    llm = OpenAI(temperature=0.7)
    
    # Create memory
    memory = ConversationBufferWindowMemory(k=3)  # Remember last 3 exchanges
    
    # Create conversation chain
    conversation = ConversationChain(
        llm=llm,
        memory=memory,
        verbose=True
    )
    
    # Have a conversation
    print(conversation.predict(input="Hi, I'm Alice."))
    print(conversation.predict(input="What's the weather like today?"))
    print(conversation.predict(input="What was my name again?"))

def huggingface_integration():
    """HuggingFace model integration"""
    print("\n=== HuggingFace Integration ===")
    
    try:
        # Initialize HuggingFace LLM
        llm = HuggingFaceHub(
            repo_id="google/flan-t5-large",
            model_kwargs={"temperature": 0.7, "max_length": 64}
        )
        
        # Create prompt template
        template = """Question: {question}
        
        Answer:"""
        prompt = PromptTemplate(template=template, input_variables=["question"])
        
        # Create chain
        llm_chain = LLMChain(prompt=prompt, llm=llm)
        
        # Ask a question
        question = "Who was the first president of the United States?"
        print(llm_chain.run(question))
    except Exception as e:
        print(f"Error in HuggingFace integration: {e}")

def main():
    # Run all demonstrations
    basic_llm_chain()
    document_qa_chain()
    conversation_with_memory()
    conversational_agent()
    
    # Uncomment if you have HuggingFace API key
    # huggingface_integration()

if __name__ == "__main__":
    main()
