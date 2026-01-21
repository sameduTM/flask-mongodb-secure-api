from mongoengine import connect

connect(
    db="secure_mongo_db",
    host='db',
    port=27017,
    alias='default',
    uuidRepresentation='standard')
