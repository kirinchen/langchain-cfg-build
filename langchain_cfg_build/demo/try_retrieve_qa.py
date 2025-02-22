from pathlib import Path
from typing import List

from langchain_core.documents import Document
from py_common_utility.utils import env_utils

from langchain_cfg_build import langchain_cfg_build_app
from langchain_cfg_build.embed_db.embed_db_loader import EmbedDbLoader
from langchain_cfg_build.rag import rag_service


def generate_document_list() -> List[Document]:
    documents = [
        Document(id="t1", page_content="Tom is a sunflower", metadata=rag_service.trim_metadata_dict(
            {"booktitle": "Magical summer rainy day", "location": {"x": 10, "y": 9}})),
        Document(id="t2",page_content="BigCoCo is a water monster", metadata={"booktitle": "Magical summer rainy day"}),
        Document(id="t3", page_content="BigCoCo weighs 150 kg.", metadata={"booktitle": "Magical summer rainy day"})
    ]
    # Add your document generation logic here
    return documents


def invoke_query(db_loader: EmbedDbLoader,query: str):
    d_list = generate_document_list()
    rag_service.save_embed_db(db_loader, iter([d_list]))
    return "embed test"
    # db_loader = EmbedDbLoader(local_path=db_path)
    # resp = embed_db_query_service.retrieve_qa(db_loader=db_loader, llm=EnumLLM.gpt_4o_mini,
    #                                           query=query)
    # return resp


if __name__ == '__main__':
    env_path = Path(__file__).parent.parent.parent
    langchain_cfg_build_app.initialize(str(env_path))
    e_db_loader = EmbedDbLoader(
        collection_name="try_show_embeddings",
        connection=env_utils.env('PGVECTOR_TEST_CONNECTION')
    )
    resp = invoke_query(db_loader=e_db_loader,query='BigCoCo 是什麼?')
    # print(resp)

    # tool= tool_utils.gen_tool(name="Magical summer rainy day 小說資料庫",
    #                     desc="可以給定query,查詢Magical summer rainy day 小說的詳細資訊",
    #                     func=lambda x: invoke_query(query=x ))
    #
    # agent_builder = AgentBuilder(
    #     EnumLLM.gpt_4o,
    #     [],
    #     "hwchase17/react"
    # )
    # agent_builder.add_tool(tool)
    # agent_executor = agent_builder.build_executor()
    # query = '請用*Magical summer rainy day"* 書中的 *BigCoCo* 腳色,寫一個牠的故事'
    # # query = 'What is the main focus of this project?'
    # result = agent_executor.invoke({"input": query})
    # print(result)
