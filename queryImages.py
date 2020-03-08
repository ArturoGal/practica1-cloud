import keyvalue.sqlitekeyvalue as KeyValue
import keyvalue.parsetriples as ParseTripe
import keyvalue.stemmer as Stemmer
import sys


# Make connections to KeyValue
kv_labels = KeyValue.SqliteKeyValue("local_db/sqlite_labels.db","labels",sortKey=True)
kv_images = KeyValue.SqliteKeyValue("local_db/sqlite_images.db","images")

# Process Logic
args = sys.argv

for i in range(1, len(args)):
    arg = args[i]
    stemmedWord = Stemmer.stem(arg)
    category = kv_labels.get(stemmedWord)
    images = kv_images.get(category)
    print(images)

# Close KeyValues Storages
kv_labels.close()
kv_images.close()







