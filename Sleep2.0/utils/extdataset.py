from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import Annoy
from langchain_text_splitters import CharacterTextSplitter
from transformers import AutoTokenizer, AutoModel
from langchain_core.output_parsers import StrOutputParser
from langchain.prompts import PromptTemplate
from langchain.llms import BaseLLM
from langchain.schema import LLMResult, Generation
from pydantic import PrivateAttr
import torch
import os


class TransformerEmbeddingGenerator:
    def __init__(self, model_name):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
        self.model = AutoModel.from_pretrained(model_name, trust_remote_code=True, output_hidden_states=True).to("cuda")

    def embed_text(self, text):
        inputs = self.tokenizer(text, return_tensors="pt", padding="max_length", truncation=True, max_length=2048).to("cuda")
        with torch.no_grad():
            outputs = self.model(**inputs)
            hidden_states = outputs.hidden_states[-1]
            embeddings = hidden_states.mean(dim=2)
        return embeddings.squeeze().cpu().numpy()

    # 若显存充足可以选择此函数实现
    # def embed_documents(self, documents):
    #     inputs = self.tokenizer(documents, return_tensors="pt", padding=True, truncation=True, max_length=2048).to("cuda")
    #     with torch.no_grad():
    #         outputs = self.model(**inputs)
    #         hidden_states = outputs.hidden_states[-1]
    #         embeddings = hidden_states.mean(dim=2)
    #     return embeddings.squeeze().cpu().numpy()
        

    def embed_documents(self, documents):
        ret = [self.embed_text(doc) for doc in documents]
        return ret
        # inputs = self.tokenizer(documents, return_tensors="pt", padding="max_length", truncation=True, max_length=2048).to("cuda")
        # keys = list(inputs.keys())
        # inputs_len = len(inputs[keys[0]])
        # embeddings = list()
        # for i in range(inputs_len):    # 显存不足，只能一个个处理
        #     sub_inputs = dict()
        #     for key in keys:
        #         sub_inputs[key] = inputs[key][i].reshape(1, -1)
        #     with torch.no_grad():
        #         outputs = self.model(**sub_inputs)
        #         hidden_states = outputs.hidden_states[-1]
        #         sub_embeddings = hidden_states.mean(dim=2)
        #     embeddings.append(sub_embeddings.squeeze().cpu().numpy())
        # print(len(embeddings[0]))
        # print(len(embeddings))
        # return embeddings

    def embed_query(self, query):
        return self.embed_text(query)

INSOMNIA_FOLDER = "dataset/insomnia"
APNEA_FOLDER = "dataset/apnea"
file_names = os.listdir(INSOMNIA_FOLDER)
documents = list()
for file_name in file_names:
    loader = TextLoader(os.path.join(INSOMNIA_FOLDER, file_name), encoding="utf8")
    document = loader.load()
    documents.extend(document)   # GOTO: 需要修改成包含多个文件的列表，使用extend方法
text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=0)
texts = text_splitter.split_documents(documents)
embeddings = TransformerEmbeddingGenerator(model_name="D:\git\ChatGLM2-6B-main\weights\ChatGLM2-6B-int4")
vectorstore = Annoy.from_documents(texts, embeddings)

retriever = vectorstore.as_retriever()
docs = retriever.invoke("如何治疗失眠？")
for doc in docs:
    print(doc)
    print(len(doc.page_content))


# 加载本地模型和tokenizer
class LocalLLM(BaseLLM):
    _model = PrivateAttr()
    _tokenizer = PrivateAttr()

    def __init__(self, model, tokenizer):
        super().__init__()
        self._model = model
        self._tokenizer = tokenizer
    
    @property
    def model(self):
        return self._model
    
    @property
    def tokenizer(self):
        return self._tokenizer

    def _llm_type(self) -> str:
        return f"{self.model}"

    def _generate(
        self, 
        prompts, 
        stop=None, 
        **kwargs
    ):
        # print("_generate call!")
        # 存储生成结果
        generations = []
        
        for prompt in prompts:
            print(prompt)
            generated_text, history = model.chat(tokenizer, prompt, history=[])
            generations.append([Generation(text=generated_text)])

        # 返回包含生成结果的LLMResult对象
        return LLMResult(generations=generations)

def extdata_template():    
    # 定义Langchain prompt模板
    template = """
    {srcdata}
    下面是一些你可以参考的信息：
    {extdata}
    """

    # 创建 Langchain PromptTemplate
    prompt = PromptTemplate(input_variables=["srcdata", "extdata"], template=template)
    return prompt

# 初始化 OpenAI LLM (请替换为你自己的 API 密钥)
model = AutoModel.from_pretrained("D:\git\ChatGLM2-6B-main\weights\ChatGLM2-6B-int4", trust_remote_code=True).cuda()
tokenizer = AutoTokenizer.from_pretrained("D:\git\ChatGLM2-6B-main\weights\ChatGLM2-6B-int4", trust_remote_code=True)
llm = LocalLLM(model=model, tokenizer=tokenizer)

# 使用 LLMChain 提取网页的关键信息
llm_chain = prompt | llm | StrOutputParser()

def summarize_webpage(webpage_content):
    # 使用 Langchain 模型处理网页内容
    summary = llm_chain.invoke({"web_content": webpage_content})
    return summary


