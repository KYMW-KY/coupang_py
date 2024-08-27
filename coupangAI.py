from crewai import Crew, Agent, Task
from langchain_ollama import ChatOllama
from openai import OpenAI
from responseData import response
import json
import os
from PyQt5.QtWidgets import QApplication, QTextBrowser, QLineEdit, QVBoxLayout, QWidget
from PyQt5.QtGui import QIcon, QFont
import sys

class Window(QWidget) : 
    def __init__ (self) :
        super().__init__()

        self.title = "Chat"
        self.top = 400
        self.left = 400
        self.width = 400
        self.height = 600

        self.setStyleSheet('border-top:black')
        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)
        self.Ui()

    def Ui(self):
        self.browser = QTextBrowser()
        self.lineEdit = QLineEdit()

        vbox = QVBoxLayout()
        vbox.addWidget(self.browser)
        vbox.addWidget(self.lineEdit)

        self.setLayout(vbox)
        self.lineEdit.returnPressed.connect(self.updateBrowser)
    
    def updateBrowser(self) : 
        llm = ChatOllama( # 어떠한 모델을 사용할지
            model='llama3.1',
            base_url='http://localhost:11434'
        )

        user_question = str(self.lineEdit.text())
        category = ''
        responseData = response()
        product_data = responseData.get_products_by_category("")
        product_list = []
        for product in product_data:
            name = product.get('name', '이름 없음')  # 'name'이 없으면 '이름 없음'으로 대체
            price = product.get('price', '가격 없음')  # 'price'가 없으면 '가격 없음'으로 대체
            category=product.get('productCategory', 'NOT')
            rating = product.get('productRating', '점수 없음')
            product_list.append(f"이름: {name}, 가격: {price}, 카테고리 : {category}, 평점 : {rating}")

        pd = "\n".join(product_list)

        shopping_agent = Agent(
            role = '고객이 원하는 상품을 추출',#어떤걸 수행할지
            goal = '고객이 원하는 답에서 카테고리 중에 비슷한걸 찾아서 제공해줘', # 어떠한 행동을 해야하는지
            backstory = '그중에서 가격이 낮은것을 알려줘(한국어로 말해줘야해)', # 두가지를 합쳐서 어떤 말을해야할지
            llm = llm
        )
        #카테고리를 정하고
        shopping_task = Task(
            description = f"{user_question}\n 제품목록 :{pd}", # 고객의 질문
            expected_output = '고객이 원하는 제품 추천', #고객에게 어떻게 추출될지
            agent = shopping_agent, # 고객의 일을 수행할 ai
        )

        crew = Crew(
            agents = [shopping_agent],
            tasks = [shopping_task],
            verbose = True
        )

        result = crew.kickoff()

        self.browser.append("user : ", user_question)
        self.browser.append("chatbot : ", str(result))
        self.lineEdit.clear()

app = QApplication(sys.argv)
window = Window()
window.show()
app.exec()