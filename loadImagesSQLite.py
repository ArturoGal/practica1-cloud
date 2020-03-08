import keyvalue.parsetriples as ParseTriples
import keyvalue.stemmer as Stemmer
import keyvalue.sqlitekeyvalue as sqlite
from botocore.exceptions import ClientError

# Make connections to KeyValue
kv_labels = sqlite.SqliteKeyValue('./local_db/sqlite_labels.db', 'labels', sortKey=True)
kv_images = sqlite.SqliteKeyValue('./local_db/sqlite_images.db', 'images')

# Process Logic.
parse_images = ParseTriples.ParseTriples('./data/images.ttl')
parse_labels = ParseTriples.ParseTriples('./data/labels_en.ttl')

# Insert Images 
for i in range(100000):
    line = parse_images.getNext()
    category = line[0]
    B = line[1]
    imageURL = line[2]
    if B == 'http://xmlns.com/foaf/0.1/depiction':
        print('Added: ' + category + ', ' + imageURL + '	' + str(count))
        kv_images.put(category, imageURL)

print()
print()
print()
print()
print()

# Insert Labels
for i in range(100000):
    line = parse_labels.getNext()
    category = line[0]
    B = line[1]
    terms = line[2]
    findImage = kv_images.get(category)
    if B == 'http://www.w3.org/2000/01/rdf-schema#label' and findImage is not None:
        for token in terms.split(' '):
            stemmedWord = Stemmer.stem(token)
            kv_labels.putSort(stemmedWord, str(i), category)
    else:
        i = i - 1

# Close KeyValues Storages
kv_labels.close()
kv_images.close()
