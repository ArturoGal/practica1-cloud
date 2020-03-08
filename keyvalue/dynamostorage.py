import boto3
from botocore.exceptions import ClientError

dynamodb = boto3.client('dynamodb')

class DynamodbKeyValue:
    def __init__(self, tableName):
        super().__init__()
        tables = dynamodb.list_tables()

        if tableName not in tables['TableNames']:
            self.createTable(tableName)
        else:
            print('Table ' + tableName + ' already exists')
            self._tableName = tableName

    def createTable(self, tableName):
        table = dynamodb.create_table(
                    TableName=tableName,
                    KeySchema=[
                        {
                            'AttributeName': 'key',
                            'KeyType': 'HASH'
                        },
                        {
                            'AttributeName': 'sort',
                            'KeyType': 'RANGE'
                        }
                    ],
                    AttributeDefinitions=[
                        {
                            'AttributeName': 'key',
                            'AttributeType': 'S'
                        },
                        {
                            'AttributeName': 'sort',
                            'AttributeType': 'N'
                        }
                    ],
                    ProvisionedThroughput={
                        'ReadCapacityUnits': 5,
                        'WriteCapacityUnits': 5
                    }
            )  
        self._tableName = tableName

    def put(self, key, sort, value):
        if not isinstance(key, str):
            raise TypeError('key must be of str type!')
        if not isinstance(sort, int):
            raise TypeError('sort must be of int type!')
        if not isinstance(value, str):
            raise TypeError('value must be of str type!')
        try:
            response = dynamodb.put_item(
                TableName=self._tableName,
                Item={
                    'key': {"S": key},
                    'sort': {"N": str(sort)},
                    'value': {"S": value}
                }
            )
        except ClientError as e:
            print(e.response['Error'])
            raise e
        return

    def get(self, key, sort):
        if not isinstance(key, str):
            raise TypeError('key must be of str type!')
        response = dynamodb.get_item(
            TableName=self._tableName,
            Key={
                'key': {"S": key},
                'sort': {"N": str(sort)}
            },
            ReturnConsumedCapacity='TOTAL',
        )
        return response