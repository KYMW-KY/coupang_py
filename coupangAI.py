from crewai import Crew, Agent, Task
from langchain_ollama import ChatOllama
from openai import OpenAI
import requests


url = 'http://localhost:8080/product/' + ''
response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    print(data)
    print(json.dump(data, indent=4))
else : 
    print("Reqeust failed with status code : ", 
          response.status_code)


llm = ChatOllama( # 어떠한 모델을 사용할지
    model='llama3.1',
    base_url='http://localhost:11434'   
)

user_question = input("원하시는 제품을 입력해주세요 : ")

shopping_agent = Agent(
    role = '고객이 원하는 상품을 추출',#어떤걸 수행할지
    goal = '고객이 원하는 상품을 쿠팡 플랫폼에서 추출해서 알려줘', # 어떠한 행동을 해야하는지
    backstory = '', # 두가지를 합쳐서 어떤 말을해야할지
    llm = llm
)

shopping_task = Task(
    description = user_question, # 고객의 질문
    expected_output = '고객이 원하는 ', #고객에게 어떻게 추출될지
    agent = shopping_agent, # 고객의 일을 수행할 ai
)

crew = Crew(
    agents = [shopping_agent],
    tasks = [shopping_task],
    verbose = True
)

result = crew.kickoff()

print(result)