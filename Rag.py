from langchain.vectorstores import Chroma
from langchain.chat_models import ChatOllama
from langchain.embeddings import FastEmbedEmbeddings
from langchain.schema.output_parser import StrOutputParser
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema.runnable import RunnablePassthrough
from langchain.prompts import PromptTemplate
from langchain.vectorstores.utils import filter_complex_metadata

class ChatPDF:
    vector_store = None
    retriever = None
    chain = None

    def __init__(self):
        self.model = ChatOllama(model="mistral")  # OLLAMA의 mistral 모델 이용
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1024, chunk_overlap=100) # PDF 텍스트 분할
        self.prompt = PromptTemplate.from_template(
            """
            <s> [INST] You are an assistant for question-answering tasks. Use the following pieces of retrieved context 
            to answer the question. If you don't know the answer, just say that you don't know. Use three sentences
            maximum and keep the answer concise. [/INST] </s> 
            [INST] Question: {question} 
            Context: {context} 
            Answer: [/INST]
            """
        )

    def ingest(self, pdf_file_path: str):
        docs = PyPDFLoader(file_path=pdf_file_path).load()  # 랭체인의 PDF 모듈 이용해 문서 로딩
        chunks = self.text_splitter.split_documents(docs) # 문서를 청크로 분할
        chunks = filter_complex_metadata(chunks)  

        vector_store = Chroma.from_documents(documents=chunks, embedding=FastEmbedEmbeddings())  # 임메딩 벡터 저장소 생성 및 청크 설정
        self.retriever = vector_store.as_retriever(search_type="similarity_score_threshold",
            search_kwargs={
                "k": 3,
                "score_threshold": 0.5,
            },
        )  # 유사도 스코어 기반 벡터 검색 설정

        self.chain = ({"context": self.retriever, "question": RunnablePassthrough()} | self.prompt | self.model | StrOutputParser()) # 프롬프트 입력에 대한 모델 실행, 출력 파서 방법 설정

    def ask(self, query: str):  # 질문 프롬프트 입력 시 호출
        if not self.chain:
            return "Please, add a PDF document first."
        return self.chain.invoke(query) 

    def clear(self):  # 초기화
        self.vector_store = None
        self.retriever = None
        self.chain = None 