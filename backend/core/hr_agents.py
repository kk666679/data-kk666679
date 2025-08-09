from langchain.agents import AgentExecutor, Tool
from langchain.chat_models import ChatOpenAI
from langchain.agents import initialize_agent
from .malaysian_compliance import MalaysianCompliance
from .models import EPFCalculation, HRDFCourse

class HRAgents:
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    
    def create_hr_agent(self):
        """Creates LangChain HR agent with Malaysian compliance tools"""
        tools = [
            Tool(
                name="EPF_Calculator",
                func=self._epf_tool,
                description="Calculates Malaysian EPF contributions for given salary"
            ),
            Tool(
                name="HRDF_Claim",
                func=self._hrdf_tool,
                description="Processes HRDF training claims and calculates claimable amounts"
            ),
            Tool(
                name="SOCSO_Calculator", 
                func=self._socso_tool,
                description="Calculates Malaysian SOCSO contributions"
            )
        ]
        
        return initialize_agent(
            tools,
            self.llm,
            agent="chat-conversational-react-description",
            verbose=True
        )
    
    def _epf_tool(self, salary_str: str) -> str:
        """EPF calculation tool for agent"""
        try:
            salary = float(salary_str)
            calc = EPFCalculation(basic_salary=salary)
            result = MalaysianCompliance.calculate_epf(calc)
            return f"EPF: Employee RM{result['employee_share']}, Employer RM{result['employer_share']}"
        except:
            return "Invalid salary amount"
    
    def _hrdf_tool(self, course_info: str) -> str:
        """HRDF claim tool for agent"""
        try:
            # Simple parsing - in production would be more sophisticated
            hours = 40  # default
            levy_balance = 5000  # default
            course = HRDFCourse(code="HRDF001", hours=hours, provider="Default")
            claimable = MalaysianCompliance.claim_hrdf(course, levy_balance)
            return f"HRDF claimable amount: RM{claimable}"
        except:
            return "Unable to calculate HRDF claim"
    
    def _socso_tool(self, salary_str: str) -> str:
        """SOCSO calculation tool for agent"""
        try:
            salary = float(salary_str)
            result = MalaysianCompliance.calculate_socso(salary)
            return f"SOCSO: Employee RM{result['employee_contribution']}, Employer RM{result['employer_contribution']}"
        except (ValueError, TypeError) as e:
            return f"Invalid salary amount: {e}"
        except Exception as e:
            return f"Error calculating SOCSO: {e}"