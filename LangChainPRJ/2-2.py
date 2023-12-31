#.env 파일의 API KEY를 사용하기 위한 패키지 로드
from dotenv import load_dotenv
#.env 파일의 변수 불러오는 함수 실행
load_dotenv()

# langchain 제공 loader 중 pyPDFLoader 로드
from langchain.document_loaders import PyPDFLoader
# langchain 제공 splitter 중 RecursiveCharacterTextSplitter 로드
from langchain.text_splitter import RecursiveCharacterTextSplitter
# langchain 제공 vectorDB 중 오픈소스인 ChromaDB 로드
from langchain.vectorstores import Chroma
# langchain 제공 embedding 객체 중 OpenAI의 Embedding 모듈 로드
from langchain.embeddings import OpenAIEmbeddings
# langchain 제공하는 ChatGPT의 채팅모드 패키지 로드
from langchain.chat_models import ChatOpenAI
# langchain 제공 retriever 중 MultilQueryRetriever 패키지 로드
from langchain.retrievers.multi_query import MultiQueryRetriever


#Loader
loader = PyPDFLoader("unsu.pdf")
pages = loader.load_and_split()

#Split
text_splitter = RecursiveCharacterTextSplitter(
    # Set a really small chunk size, just to show.
    chunk_size = 300,
    chunk_overlap  = 20,
    length_function = len,
    is_separator_regex = False,
)
texts = text_splitter.split_documents(pages)

#Embedding. API-KEY를 통해 OpenAI 제공 임베딩 모델 로드, 비용 발생
embeddings_model = OpenAIEmbeddings()

#ChromaDB에 Split된 데이터 texts를 OpenAI Embedding 모델로 벡터화하여 저장함(메모리 적재)
db = Chroma.from_documents(texts, embeddings_model)


#Question
question = "아내가 먹고 싶어하는 음식은 무엇이야?"
#ChatGPT 대화 모듈 로드 temperature 값이 1에 가까울 수록 창의적인 답변 제공
llm = ChatOpenAI(temperature=0)
#db에 질의에 대한 응답을 가져올 MultiQueryRetriever 객체 할당.
retriver_from_llm = MultiQueryRetriever.from_llm(
    retriever=db.as_retriever(), llm=llm
)
# MultiQueryRetriever 객체를 통해, 질문과 연관있는 문서를 db로부터 가져와서 변수 docs에 저장함
docs = retriver_from_llm.get_relevant_documents(query=question)
print(len(docs)) # 질문과 연관성 높은 문서의 개수 출력
# 해당 문서 전체 출력
for doc in docs :
    print(doc)
