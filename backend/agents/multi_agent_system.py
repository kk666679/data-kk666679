from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain.tools import Tool
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.memory import ConversationBufferMemory
from typing import Dict, List
import asyncio

class HRMultiAgentSystem:
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
        self.agents = {}
        self._initialize_agents()
    
    def _initialize_agents(self):
        """Initialize specialized HR agents"""
        
        # Recruitment Agent
        recruitment_tools = [
            Tool(
                name="screen_resume",
                func=self._screen_resume,
                description="Screen resumes for job requirements"
            ),
            Tool(
                name="schedule_interview",
                func=self._schedule_interview,
                description="Schedule interviews with candidates"
            )
        ]
        
        # Payroll Agent
        payroll_tools = [
            Tool(
                name="calculate_salary",
                func=self._calculate_salary,
                description="Calculate employee salary with Malaysian compliance"
            ),
            Tool(
                name="generate_payslip",
                func=self._generate_payslip,
                description="Generate employee payslip"
            )
        ]
        
        # Employee Relations Agent
        er_tools = [
            Tool(
                name="analyze_feedback",
                func=self._analyze_feedback,
                description="Analyze employee feedback and sentiment"
            ),
            Tool(
                name="suggest_interventions",
                func=self._suggest_interventions,
                description="Suggest HR interventions based on analysis"
            )
        ]
        
        self.agents = {
            "recruitment": self._create_agent("recruitment", recruitment_tools),
            "payroll": self._create_agent("payroll", payroll_tools),
            "employee_relations": self._create_agent("employee_relations", er_tools)
        }
    
    def _create_agent(self, agent_type: str, tools: List[Tool]) -> AgentExecutor:
        """Create specialized agent with tools"""
        
        prompts = {
            "recruitment": "You are a Malaysian HR recruitment specialist. Help with hiring processes, resume screening, and interview coordination.",
            "payroll": "You are a Malaysian payroll specialist. Calculate salaries, EPF, SOCSO, and ensure compliance with Malaysian labor laws.",
            "employee_relations": "You are an employee relations specialist. Analyze feedback, suggest interventions, and improve workplace harmony."
        }
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", prompts[agent_type]),
            ("human", "{input}"),
            ("placeholder", "{agent_scratchpad}")
        ])
        
        agent = create_openai_functions_agent(self.llm, tools, prompt)
        return AgentExecutor(agent=agent, tools=tools, verbose=True)
    
    async def process_hr_request(self, request: str, agent_type: str = "auto") -> Dict:
        """Process HR request using appropriate agent"""
        
        if agent_type == "auto":
            agent_type = self._determine_agent_type(request)
        
        if agent_type not in self.agents:
            return {"error": f"Unknown agent type: {agent_type}"}
        
        try:
            result = await self.agents[agent_type].ainvoke({"input": request})
            return {
                "agent": agent_type,
                "response": result["output"],
                "success": True
            }
        except Exception as e:
            return {
                "agent": agent_type,
                "error": str(e),
                "success": False
            }
    
    def _determine_agent_type(self, request: str) -> str:
        """Determine which agent should handle the request"""
        request_lower = request.lower()
        
        if any(word in request_lower for word in ['hire', 'recruit', 'interview', 'resume', 'candidate']):
            return "recruitment"
        elif any(word in request_lower for word in ['salary', 'payroll', 'epf', 'socso', 'pay']):
            return "payroll"
        elif any(word in request_lower for word in ['feedback', 'sentiment', 'employee', 'satisfaction']):
            return "employee_relations"
        
        return "employee_relations"  # Default
    
    def _screen_resume(self, resume_text: str) -> str:
        """Screen resume for job requirements"""
        # Simplified screening logic
        skills = ['python', 'java', 'sql', 'leadership']
        found_skills = [skill for skill in skills if skill.lower() in resume_text.lower()]
        
        score = len(found_skills) / len(skills) * 100
        return f"Resume screening score: {score:.1f}%. Found skills: {', '.join(found_skills)}"
    
    def _schedule_interview(self, candidate_info: str) -> str:
        """Schedule interview with candidate"""
        return f"Interview scheduled for candidate. Confirmation email sent."
    
    def _calculate_salary(self, employee_data: str) -> str:
        """Calculate salary with Malaysian compliance"""
        # Mock calculation
        basic_salary = 5000
        epf_employee = basic_salary * 0.11
        epf_employer = basic_salary * 0.13
        
        return f"Salary calculation: Basic RM{basic_salary}, EPF Employee RM{epf_employee:.2f}, EPF Employer RM{epf_employer:.2f}"
    
    def _generate_payslip(self, employee_id: str) -> str:
        """Generate employee payslip"""
        return f"Payslip generated for employee {employee_id}. Sent to employee email."
    
    def _analyze_feedback(self, feedback_text: str) -> str:
        """Analyze employee feedback"""
        # Simple sentiment analysis
        negative_words = ['bad', 'terrible', 'awful', 'hate', 'unfair']
        negative_count = sum(1 for word in negative_words if word in feedback_text.lower())
        
        sentiment = "negative" if negative_count > 0 else "positive"
        return f"Feedback analysis: {sentiment} sentiment detected. Risk level: {'high' if negative_count > 2 else 'low'}"
    
    def _suggest_interventions(self, analysis_result: str) -> str:
        """Suggest HR interventions"""
        if "negative" in analysis_result:
            return "Suggested interventions: 1) Schedule 1-on-1 meeting, 2) Review workload, 3) Provide support resources"
        return "Suggested interventions: Continue positive engagement, recognize good performance"

class ConversationalHRAgent:
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)
        self.memory = ConversationBufferMemory(return_messages=True)
        
    async def chat(self, message: str, context: Dict = None) -> str:
        """Conversational HR assistant"""
        
        system_prompt = """You are CikguHR, a friendly Malaysian HR assistant. 
        You help with HR queries in English, Bahasa Malaysia, and basic Mandarin.
        You understand Malaysian workplace culture, EPF, SOCSO, and local labor laws.
        Be helpful, professional, and culturally sensitive."""
        
        # Add Malaysian context
        if context:
            system_prompt += f"\nContext: {context}"
        
        response = await self.llm.ainvoke([
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": message}
        ])
        
        return response.content