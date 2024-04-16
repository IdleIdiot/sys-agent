from utils.log import FileLogger

from config.settings import database
from config.message import message_mapping
from elasticsearch import Elasticsearch, helpers

logger = FileLogger(__name__).get_logger()


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


# 使用示例
if __name__ == "__main__":
    client = ElasticsearchClient()
    index_name = "test_index"
    client.create_index(index_name)

    # 存储单个文档
    document = {
        "title": "Example Document",
        "content": "This is an example document for Elasticsearch.",
    }
    client.index_document(index_name, document)

    # 批量存储文档
    documents = [
        {"title": "Document 1", "content": "Content for document 1"},
        {"title": "Document 2", "content": "Content for document 2"},
        {"title": "Document 3", "content": "Content for document 3"},
    ]
    client.bulk_index_documents(index_name, documents)
