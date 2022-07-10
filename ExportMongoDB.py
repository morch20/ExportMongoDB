from math import ceil
from pymongo import MongoClient
from os import chdir, listdir
from json import load
from certifi import where


class ExportMongoDBTo:

    def __init__(self, uri: str):
        self._uri_type = self.__validate_uri_type(uri)
        self._uri = uri
        self._client = self.set_client(self._uri)

    def show_uri(self) -> str:
        return self._uri

    def set_client(self, uri: str):

        if self._uri_type == "Atlas":
            client = MongoClient(uri, tlsCAFile=where())
        else:
            client = MongoClient(uri)

        print("Connection to", uri, "was successful")
        return client

    def show_dbs(self) -> list:
        return self._client.list_database_names()

    def show_collections(self, db) -> list:
        return self._client[db].list_collection_names()

    def __export_db(self, uri: str, db_name: str):

        import_client = self.set_client(uri)

        import_db = import_client[db_name]
        export_db = self._client[db_name]

        i = 0
        total = len(self.show_collections(import_db))

        for coll in self.show_collections(import_db):
            ExportMongoDBTo.__status_bar(total, i)
            i += 1

            for doc in import_db[coll].find():
                export_db[coll].insert_one(doc)

    def __export_coll(self, uri: str, from_db: str, to_db: str, coll: str):

        import_client = self.set_client(uri)

        import_db = import_client[from_db]
        export_db = self._client[to_db]

        i = 0
        total = import_db[coll].count_documents({})

        for doc in import_db[coll].find():
            ExportMongoDBTo.__status_bar(total, i)
            i += 1
            export_db[coll].insert_one(doc)

    def __export_doc(self, uri: str, from_db: str, to_db: str, from_coll: str,
                     to_coll: str, properties: dict):

        import_client = self.set_client(uri)

        import_db = import_client[from_db]
        export_db = self._client[to_db]

        doc = import_db[from_coll].find_one(properties)
        export_db[to_coll].insert_one(doc)

        ExportMongoDBTo.__status_bar(10, 9)

    def __export_db_folder_type_1(self, path: str, db_name: str):

        chdir(path)
        db = self._client[db_name]

        i = 0
        total = len(listdir())
        for coll in listdir():
            ExportMongoDBTo.__status_bar(total, i)
            i += 1

            chdir(coll)
            for doc in listdir():
                with open(doc) as json_file:
                    data = load(json_file)
                    db[coll].insert_one(data)

            chdir(path)

    def __export_db_folder_type_2(self, path: str, db_name: str):

        chdir(path)
        db = self._client[db_name]

        i = 0
        total = len(listdir())
        for coll in listdir():
            ExportMongoDBTo.__status_bar(total, i)
            i += 1

            with open(coll) as json_file:
                data = load(json_file)
                for doc in data:
                    db[coll.split(".")[0]].insert_one(data[doc])

    def __export_coll_folder_type_1(self, path: str, to_db: str, coll: str):
        chdir(path)
        db = self._client[to_db]

        i = 0
        total = len(listdir())
        for doc in listdir():
            ExportMongoDBTo.__status_bar(total, i)
            i += 1

            with open(doc) as json_file:
                data = load(json_file)
                db[coll].insert_one(data)

    def __export_coll_folder_type_2(self, path: str, to_db: str, coll: str):

        chdir(path)
        db = self._client[to_db]

        with open(coll + ".json") as json_file:
            data = load(json_file)

            i = 0
            total = len(data)
            for doc in data:
                db[coll].insert_one(data[doc])

                ExportMongoDBTo.__status_bar(total, i)
                i += 1

    def __export_doc_folder_type_1(self, path: str, to_db: str, to_coll: str, name: str):

        chdir(path)
        db = self._client[to_db]

        with open(name + ".json") as json_file:
            data = load(json_file)
            db[to_coll].insert_one(data)

        ExportMongoDBTo.__status_bar(10, 9)

    def __export_doc_folder_type_2(self, path: str, to_db: str, to_coll: str, name: dict):

        chdir(path)
        db = self._client[to_db]

        with open(name["file"] + ".json") as json_file:
            data = load(json_file)
            db[to_coll].insert_one(data[name["name"]])

        ExportMongoDBTo.__status_bar(10, 9)

    # Export to Atlas from mongodb
    def export_database_from_mongodb(self, mongodb_uri: str, db_name: str):
        if self._uri_type != "Atlas":
            raise Exception("Error! You can only export to Atlas with this method")

        if ExportMongoDBTo.validate__mongodb_uri(mongodb_uri):
            self.__export_db(mongodb_uri, db_name)

        else:
            raise Exception("Invalid uri for local MongoDB")

    def export_collection_from_mongodb(self, mongodb_uri: str, from_db: str, to_db: str, coll: str):
        if self._uri_type != "Atlas":
            raise Exception("Error! You can only export to Atlas with this method")

        if ExportMongoDBTo.validate__mongodb_uri(mongodb_uri):
            self.__export_coll(mongodb_uri, from_db, to_db, coll)

        else:
            raise Exception("Invalid uri for local MongoDB")

    def export_document_from_mongodb(self, mongodb_uri: str, from_db: str, to_db: str, from_coll: str,
                                     to_coll: str, properties: dict):
        if self._uri_type != "Atlas":
            raise Exception("Error! You can only export to Atlas with this method")

        if ExportMongoDBTo.validate__mongodb_uri(mongodb_uri):
            self.__export_doc(mongodb_uri, from_db, to_db, from_coll,
                              to_coll, properties)

        else:
            raise Exception("Invalid uri for local MongoDB")

    # Export to mongodb from atlas
    def export_database_from_atlas(self, atlas_uri: str, db_name: str):
        if self._uri_type != "MongoDB":
            raise Exception("Error! You can only export to MongoDB with this method")

        if ExportMongoDBTo.validate__atlas_uri(atlas_uri):
            self.__export_db(atlas_uri, db_name)

        else:
            raise Exception("Invalid uri for local Atlas")

    def export_collection_from_atlas(self, atlas_uri: str, from_db: str, to_db: str, coll: str):
        if self._uri_type != "MongoDB":
            raise Exception("Error! You can only export to MongoDB with this method")

        if ExportMongoDBTo.validate__atlas_uri(atlas_uri):
            self.__export_coll(atlas_uri, from_db, to_db, coll)

        else:
            raise Exception("Invalid uri for local Atlas")

    def export_document_from_atlas(self, atlas_uri: str, from_db: str, to_db: str, from_coll: str,
                                   to_coll: str, properties: dict):
        if self._uri_type != "MongoDB":
            raise Exception("Error! You can only export to MongoDB with this method")

        if ExportMongoDBTo.validate__atlas_uri(atlas_uri):
            self.__export_doc(atlas_uri, from_db, to_db, from_coll,
                              to_coll, properties)

        else:
            raise Exception("Invalid uri for local Atlas")

    # Export from folders to mongodb or atlas
    def export_database_from_folders(self, path: str, database_name: str, path_type: int = 1):

        if self._uri_type == "Folders":
            raise Exception("Error! You can only export to MongoDB or Atlas with this method")

        if ExportMongoDBTo.validate__folders_uri(path):

            if path_type == 1:
                self.__export_db_folder_type_1(path, database_name)

            elif path_type == 2:
                self.__export_db_folder_type_2(path, database_name)

            else:
                raise Exception("Error! Parameter 'path_type' must be either 1 or 2")

        else:
            raise Exception("Invalid path to folders")

    def export_collection_from_folders(self, path: str, database_name: str, collection_name: str, path_type: int = 1):

        if self._uri_type == "Folders":
            raise Exception("Error! You can only export to MongoDB or Atlas with this method")

        if ExportMongoDBTo.validate__folders_uri(path):

            if path_type == 1:
                self.__export_coll_folder_type_1(path, database_name, collection_name)

            elif path_type == 2:
                self.__export_coll_folder_type_2(path, database_name, collection_name)

            else:
                raise Exception("Error! Parameter 'path_type' must be either 1 or 2")

        else:
            raise Exception("Invalid path to folders")

    def export_document_from_folders(self, path: str, to_db: str, to_coll: str, name: dict, path_type: int = 1):

        if self._uri_type == "Folders":
            raise Exception("Error! You can only export to MongoDB or Atlas with this method")

        if ExportMongoDBTo.validate__folders_uri(path):

            if path_type == 1:
                self.__export_doc_folder_type_1(path, to_db, to_coll, name["file"])

            elif path_type == 2:
                self.__export_doc_folder_type_2(path, to_db, to_coll, name)

            else:
                raise Exception("Error! Parameter 'path_type' must be either 1 or 2")

        else:
            raise Exception("Invalid path to folders")

    def __validate_uri_type(self, uri) -> str:

        if ExportMongoDBTo.validate__mongodb_uri(uri):

            return "MongoDB"

        elif ExportMongoDBTo.validate__atlas_uri(uri):
            return "Atlas"

        elif ExportMongoDBTo.validate__folders_uri(uri):
            return "Folders"

        else:
            raise Exception("Invalid URI\n URI must be for a database in your local MongoDB, Atlas, or a specified "
                            "path to JSON files")

    @staticmethod
    def __status_bar(total: int, i: int):
        i += 1
        dash = "---"
        percent = ceil(total * 0.1)

        if i == 1:
            print("Starting... --------------------|", end="\n   ")
            if total % 10 != 0:
                print(dash, end="")

        else:
            if i % percent == 0:
                print(dash, end="")

        if i == total:
            print("\nCompleted!! --------------------|")

    @staticmethod
    def validate__mongodb_uri(uri: str) -> bool:
        return "mongodb://" in uri

    @staticmethod
    def validate__atlas_uri(uri: str) -> bool:
        return "mongodb+srv://" in uri

    @staticmethod
    def validate__folders_uri(uri: str) -> bool:
        return "C:\\" in uri
