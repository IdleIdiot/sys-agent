from utils.log import FileLogger
from datetime import datetime, timedelta

from config.settings import database
from utils.common import singleton
from config.message import message_mapping
from elasticsearch import Elasticsearch, helpers

logger = FileLogger(__name__).get_logger()


@singleton
class ElasticsearchClient:

    def __init__(self):

        host = database["elasticsearch"]["ip"]
        port = database["elasticsearch"]["port"]
        elasticsearch_url = f"http://{host}:{port}"
        self.es = Elasticsearch(hosts=elasticsearch_url)

    def create_index(self, index_name):
        if not self.es.indices.exists(index=index_name):
            body = message_mapping[index_name]
            self.es.indices.create(index=index_name, body=body)
            logger.info(f"Index '{index_name}' created.")
        else:
            logger.info(f"Index '{index_name}' already exists.")

    def bulk_index_documents(self, index_name, documents):
        actions = [
            {
                "_index": index_name,
                "_source": doc,
            }
            for doc in documents
        ]
        helpers.bulk(self.es, actions)
        logger.info(f"Indexed {len(documents)} documents into '{index_name}'.")

    def index_document(self, index_name, document):
        self.es.index(index=index_name, body=document)
        logger.info(f"Document indexed into '{index_name}'.")

    def delete_old_data(self, index_name="resource", days_to_keep=3):

        # 计算3天前的日期
        cutoff_date = datetime.now() - timedelta(days=days_to_keep)
        cutoff_date = cutoff_date.strftime("%Y-%m-%d 00:00:00")
        # cutoff_timestamp = int(
        #     cutoff_date.timestamp() * 1000
        # )  # Elasticsearch的日期格式是毫秒级时间戳

        # 构建查询以获取3天前的文档
        query = {
            "range": {
                "agent_time": {  # 假设你的文档中有一个@timestamp字段记录了日期和时间
                    "lte": cutoff_date
                }
            },
        }

        # 执行搜索查询
        search_result = self.es.search(
            index=index_name,
            body={
                "query": query,
                "size": 10000,
            },
        )

        # 获取所有匹配的文档ID
        doc_ids = [hit["_id"] for hit in search_result["hits"]["hits"]]
        # 删除这些文档
        if doc_ids:
            delete_query = {"query": {"ids": {"values": doc_ids}}}
            self.es.delete_by_query(index=index_name, body=delete_query)
            logger.info(f"Deleted {len(doc_ids)} documents.")
        else:
            logger.debug("No documents to delete.")


# 使用示例
if __name__ == "__main__":
    client = ElasticsearchClient()
    client.delete_old_data()
    # index_name = "test_index"
    # client.create_index(index_name)

    # # 存储单个文档
    # document = {
    #     "title": "Example Document",
    #     "content": "This is an example document for Elasticsearch.",
    # }
    # client.index_document(index_name, document)

    # # 批量存储文档
    # documents = [
    #     {"title": "Document 1", "content": "Content for document 1"},
    #     {"title": "Document 2", "content": "Content for document 2"},
    #     {"title": "Document 3", "content": "Content for document 3"},
    # ]
    # client.bulk_index_documents(index_name, documents)
