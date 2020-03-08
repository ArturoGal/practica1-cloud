import keyvalue.parsetriples as ParseTriples
import keyvalue.stemmer as Stemmer
import keyvalue.dynamostorage as dynamo
from botocore.exceptions import ClientError

kv_labels = dynamo.DynamodbKeyValue('terms')
kv_images = dynamo.DynamodbKeyValue('images')

# Process Logic.
parse_images = ParseTriples.ParseTriples('./data/images.ttl')
parse_labels = ParseTriples.ParseTriples('./data/labels_en.ttl')

# Insert Images 
for i in range(10000):
    line = parse_images.getNext()
    category = line[0]
    B = line[1]
    imageURL = line[2]
    if B == 'http://xmlns.com/foaf/0.1/depiction':
        kv_images.put(category, i, imageURL)
		
	
# Insert Labels
for i in range(5000):
    line = parse_labels.getNext()
    category = line[0]
    B = line[1]
    terms = line[2]
    if B == 'http://www.w3.org/2000/01/rdf-schema#label':
        for token in terms.split(' '):
            stemmedWord = Stemmer.stem(token)
            kv_labels.put(stemmedWord, i, category)

