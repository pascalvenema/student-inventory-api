import os

# import tempfile
# from functools import reduce

# from tinydb import TinyDB, Query

from pymongo import MongoClient
from bson.objectid import ObjectId


# db_dir_path = tempfile.gettempdir()
# db_file_path = os.path.join(db_dir_path, "students.json")
# student_db = TinyDB(db_file_path)

mongo_uri = os.environ.get("MONGO_URI")
client = MongoClient(mongo_uri)

db = client.student_db
students_collection = db.students


def add(student=None):
    # queries = []
    # query = Query()
    # queries.append(query.first_name == student.first_name)
    # queries.append(query.last_name == student.last_name)
    # query = reduce(lambda a, b: a & b, queries)
    # res = student_db.search(query)
    # if res:
    #     return "already exists", 409
    existing_student = students_collection.find_one(
        {"first_name": student.first_name, "last_name": student.last_name}
    )
    if existing_student:
        return "already exists", 409

    # doc_id = student_db.insert(student.to_dict())
    # student.student_id = doc_id
    # print(student)
    # return student.student_id

    result = students_collection.insert_one(student.to_dict())
    student.student_id = str(result.inserted_id)
    print(student)
    return student.student_id


def get_by_id(student_id=None, subject=None):
    # student = student_db.get(doc_id=int(student_id))
    # if not student:
    #     return "not found", 404
    try:
        student = students_collection.find_one({"_id": ObjectId(student_id)})
    except Exception:
        return "not found", 404
    if not student:
        return "not found", 404

    # student["student_id"] = student_id
    # print(student)
    # return student
    student["student_id"] = str(student["_id"])
    # del student["_id"]
    print(student)
    return student


def delete(student_id=None):
    # student = student_db.get(doc_id=int(student_id))
    # if not student:
    #     return "not found", 404
    # student_db.remove(doc_ids=[int(student_id)])
    # return student_id
    try:
        result = students_collection.delete_one({"_id": ObjectId(student_id)})
    except Exception:
        return "not found", 404

    if result.deleted_count == 0:
        return "not found", 404

    return student_id
