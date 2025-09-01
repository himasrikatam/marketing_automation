from dotenv import load_dotenv
from langchain_groq import ChatGroq
from crewai import Agent, Task, Crew
from crewai.tools import BaseTool

import os
load_dotenv()
key = os.getenv("GROQ_API_KEY")
if key:
    print("GROQ_API_KEY is set")
else:
    print("GROQ_API_KEY is not set")

llm = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model="groq/llama-3.3-70b-versatile",
    temperature=0.7,
    max_tokens=1000,
)
# response = llm.invoke("whos taylor swift")
# print(response)

class ReplaceJargonsTool(BaseTool):
    name:str = "Replace Jargons"
    description:str = "A tool to replace jargons in the email with specific terms."
    def _run(self, email:str)-> str:
        # Example implementation, replace with actual logic
        jargon_dict = {
            "WIP": "work in progress",
            "ASAP": "as soon as possible",
            "FYI": "for your information"
        }
        for jargon, replacement in jargon_dict.items():
            email = email.replace(jargon, replacement)
        return email
    
jt = ReplaceJargonsTool()

# jt.run(original_email)
# print(jt.run(original_email))

email_assistant = Agent(
    role = "Improve emails by making them more professional, clear, and concise.",
    goal = "Assist the user with email-related tasks such as reading, composing, and organizing emails.",
    backstory="Experienced in handling various email clients and proficient in email etiquette.",
    tools=[jt],
    verbose= True, #set to True to see the agent's thought process
    llm=llm,
)

original_email = """hey john, just wanted to check in and see if you got my last email about the meeting next week. let me know if you can make it.My tasks are in WIP, thanks! -sara"""

email_task = Task(
    description=f"""Take this original email and make it more professional, clear, and concise.
    {original_email}""",
    agent=email_assistant,
    expected_output="A revised version of the email that is professional, clear, and concise.",

)

crew = Crew(agents=[email_assistant],
            tasks=[email_task],
            verbose=True)

crew.kickoff()

