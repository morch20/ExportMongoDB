# ExportMongoDB
Export MongoDB databases from your local machine, Atlas, or specifically organized JSON files.

<br>
<br>

---

# Contents

- [Installation Requirements](#installation-requirements)
- [Quick Installation using pip](#quick-installation-using-pip)
- [Export Database](#export-database)
- [Export Collection](#export-collection)
- [Export Document](#export-document)
- [JSON Folders Structure](#json-folders-structure)

<br>

# Installation Requirements
---

You must have the following libraries in order for the code to work properly 

- [PyMongo](https://pymongo.readthedocs.io/en/stable/installation.html)
- [certifi](https://pypi.org/project/certifi/)
- [dnspython](https://pypi.org/project/dnspython/)  

<br>

##### Quick Installation using pip

Mac
`python3 -m pip install pymongo certifi dnspython`  

Windows
`py -m pip install pymongo dnspython certifi`

<br>

# Export Database
---

Make sure ExportMongoDB file is in the same directory as your project and imported

<br>

First initialize a ExportMongoDBTo object

```python
from ExportMongoDB import ExportMongoDBTo

# for MongoDB database in your local machine
# uri = 'mongodb://localhost:27017' 

# for MongoDB Atlas
# uri = 'mongodb+srv://<username>:<password>@cluster...'

# initialize object
export = ExportMongoDBTo(uri)

```
<br>

Export from Atlas

```python
# uri to Atlas to export from
uri = 'mongodb+srv://<username>:<password>@cluster...'

# name of the database to export from
db_name = 'myDataBase'

# export database
export.export_database_from_atlas(atlas_uri, db_name)
```

<br>
Export from local machine

```python
# uri to Atlas to export from
uri = 'mongodb://localhost:27017' 

# name of the database to export from
db_name = 'myDataBase'

# export database
export.export_database_from_mongodb(atlas_uri, db_name)
```

<br>

Export from JSON Folders

```python
# Absolute path to folder representing a database
path = 'C:\\Users\\user\\Desktop\\myDatabaseFolder'

# name of the database to export from
database_name = 'myDataBaseFolder'

# export folders structure 1
export.export_database_from_folders(path, database_name)

# export folders structure 2
export.export_database_from_folders(path, database_name, 2)
```

<br>

# Export Collection
---

<br>

# Export Document
---

<br>

# JSON Folders Structure
---

<br>

