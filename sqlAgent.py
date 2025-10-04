from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent
import os 
from dotenv import load_dotenv 

load_dotenv()
class SQLAgent:
    def __init__(self):


        llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",          
            google_api_key=os.environ.get("GOOGLE_API_KEY"),
            temperature=0.0,
            max_output_tokens=512
        )

        db = SQLDatabase.from_uri(
            os.getenv("DATABASE_URL")
        )

        self.agent = create_sql_agent(
            llm=llm,
            db=db,
            verbose=True,
            handle_parsing_errors=True,
            agent_type="zero-shot-react-description",
            max_iterations=10  ,
            max_execution_time=60,
            prefix="""You are a SQL Agent.
        Your ONLY valid outputs are:
        1. Action: <tool>\nAction Input: <input>
        2. Final Answer: <answer>

        NEVER output both an Action and a Final Answer together.
        Do not include 'Thoughts'. """,
        suffix="""Begin!
        Question: {input}

        {agent_scratchpad}

        Remember:
        - If you need to run a tool, ONLY output Action and Action Input.
        - Once the tool gives results, ALWAYS output result.
        - Answer must summarize the tool result in plain text.
        - Do not stop at tool output. Always close with result.
        - Give answer in more readable format. 
        """
        )
    def response(self, query):
        try:
            response = self.agent.invoke(query)
            print("Raw LLM Output:", response)
            return response["output"]
        except Exception as e:
            print("Raw LLM Output:", e)