#!/usr/bin/env python3
"""
Advanced NLP and Agent Demo for HRMS Malaysia
"""

import asyncio
from nlp.advanced_nlp import AdvancedNLPEngine
from agents.multi_agent_system import HRMultiAgentSystem, ConversationalHRAgent
from agents.rag_system import SmartHRAssistant

async def demo_advanced_nlp():
    """Demo advanced NLP capabilities"""
    
    print("🤖 HRMS Malaysia - Advanced NLP & Agent Demo")
    print("=" * 50)
    
    # Initialize engines
    nlp_engine = AdvancedNLPEngine()
    multi_agent = HRMultiAgentSystem()
    conversational_agent = ConversationalHRAgent()
    smart_assistant = SmartHRAssistant()
    
    # 1. Advanced Sentiment Analysis
    print("\n1. 📊 Advanced Sentiment Analysis:")
    feedback = "The work environment is quite stressful and I'm considering to quit. Management is unfair."
    
    sentiment_result = nlp_engine.analyze_employee_feedback(feedback)
    print(f"   Feedback: {feedback}")
    print(f"   Sentiment: {sentiment_result['sentiment']}")
    print(f"   Risk Level: {sentiment_result['risk_level']}")
    print(f"   Risk Score: {sentiment_result['risk_score']}")
    
    # 2. Semantic Job Matching
    print("\n2. 🎯 Semantic Job Matching:")
    job_desc = "Looking for Python developer with 3+ years experience in web development"
    resumes = [
        "Software engineer with 5 years Python experience, Django, Flask",
        "Fresh graduate in computer science, knows Java and C++",
        "Senior developer, 8 years experience in Python, web applications"
    ]
    
    matches = nlp_engine.semantic_job_matching(job_desc, resumes)
    print(f"   Job: {job_desc}")
    for i, match in enumerate(matches[:2]):
        print(f"   Match {i+1}: Score {match['similarity_score']}, Quality: {match['match_quality']}")
    
    # 3. Multi-Agent Processing
    print("\n3. 🤝 Multi-Agent System:")
    hr_request = "Calculate EPF for employee with RM5500 salary"
    
    agent_result = await multi_agent.process_hr_request(hr_request, "payroll")
    print(f"   Request: {hr_request}")
    print(f"   Agent: {agent_result['agent']}")
    print(f"   Response: {agent_result.get('response', 'Processing...')}")
    
    # 4. Conversational Agent
    print("\n4. 💬 Conversational HR Agent (CikguHR):")
    chat_message = "What is the minimum wage in Malaysia?"
    
    chat_response = await conversational_agent.chat(chat_message)
    print(f"   User: {chat_message}")
    print(f"   CikguHR: {chat_response[:150]}...")
    
    # 5. Knowledge Base Query
    print("\n5. 📚 HR Knowledge Base (RAG):")
    knowledge_query = "What are the EPF contribution rates?"
    
    knowledge_result = await smart_assistant.process_query(knowledge_query)
    print(f"   Query: {knowledge_query}")
    print(f"   Answer: {knowledge_result['response'][:150]}...")
    print(f"   Confidence: {knowledge_result.get('confidence', 'N/A')}")
    
    print("\n✅ Advanced NLP & Agent Demo completed!")

if __name__ == "__main__":
    asyncio.run(demo_advanced_nlp())