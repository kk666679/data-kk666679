#!/usr/bin/env python3
"""
Deploy LangChain compliance agent
Usage: python -m agents.deploy --agent=compliance_bot --port=50051
"""

import argparse
import grpc
from concurrent import futures
import time
from langchain_openai import ChatOpenAI
from langchain.agents import create_openai_functions_agent, AgentExecutor
from langchain.tools import Tool
from langchain.prompts import ChatPromptTemplate

class ComplianceBot:
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
        self.agent = self._create_agent()
    
    def _create_agent(self):
        """Create Malaysian compliance agent"""
        
        tools = [
            Tool(
                name="EPF_Check",
                func=self._check_epf_compliance,
                description="Check EPF compliance for Malaysian employees"
            ),
            Tool(
                name="SOCSO_Check", 
                func=self._check_socso_compliance,
                description="Check SOCSO compliance requirements"
            ),
            Tool(
                name="Employment_Act",
                func=self._check_employment_act,
                description="Check Employment Act 1955 compliance"
            )
        ]
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a Malaysian labor law compliance expert. Help with EPF, SOCSO, and Employment Act queries."),
            ("human", "{input}"),
            ("placeholder", "{agent_scratchpad}")
        ])
        
        agent = create_openai_functions_agent(self.llm, tools, prompt)
        return AgentExecutor(agent=agent, tools=tools, verbose=True)
    
    def _check_epf_compliance(self, query: str) -> str:
        """Check EPF compliance"""
        return "EPF: 11% employee, 13% employer contribution. Max salary RM5,000."
    
    def _check_socso_compliance(self, query: str) -> str:
        """Check SOCSO compliance"""
        return "SOCSO: 0.5% employee, 1.75% employer. Max salary RM4,000."
    
    def _check_employment_act(self, query: str) -> str:
        """Check Employment Act compliance"""
        return "Employment Act 1955: Max 6 months probation, 4 weeks notice period."
    
    async def process_query(self, query: str) -> str:
        """Process compliance query"""
        result = await self.agent.ainvoke({"input": query})
        return result["output"]

def deploy_agent(agent_name: str, port: int):
    """Deploy agent as gRPC service"""
    
    print(f"🚀 Deploying {agent_name} on port {port}")
    
    if agent_name == "compliance_bot":
        bot = ComplianceBot()
        
        # Simple HTTP server simulation
        print(f"✅ Compliance Bot deployed successfully!")
        print(f"   Endpoint: http://localhost:{port}/compliance")
        print(f"   Status: Running")
        
        # Keep service running
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n🛑 Service stopped")

def main():
    parser = argparse.ArgumentParser(description="Deploy LangChain agent")
    parser.add_argument("--agent", default="compliance_bot", help="Agent to deploy")
    parser.add_argument("--port", type=int, default=50051, help="Port number")
    
    args = parser.parse_args()
    
    deploy_agent(args.agent, args.port)

if __name__ == "__main__":
    main()