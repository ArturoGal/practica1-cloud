  var AWS = require('aws-sdk');
  AWS.config.loadFromPath('./config.json');

  var db = new AWS.DynamoDB();

  function keyvaluestore(table) {
    this.LRU = require("lru-cache");
    this.cache = new this.LRU({
      max: 500
    });
    this.tableName = table;
  };

  /**
   * Initialize the tables
   * 
   */
  keyvaluestore.prototype.init = function (whendone) {

    var tableName = this.tableName;
    var self = this;

    db.listTables(function (err, data) {
      for (var i = 0; i < data.TableNames.length; i++) {
        if (tableName == data.TableNames[i]) {
          whendone(); //Call Callback function.
          return;
        }
      }
    })
  };
  /**
   * Get result(s) by key
   * 
   * @param search
   * 
   * Callback returns a list of objects with keys "inx" and "value"
   */

  keyvaluestore.prototype.get = function (search, callback) {
    var self = this;

    if (self.cache.get(search))
      callback(null, self.cache.get(search));
    else {
      /*
       * 
       * La función QUERY debe generar un arreglo de objetos JSON son cada
       * una de los resultados obtenidos. (inx, value, key).
       * Al final este arreglo debe ser insertado al cache. Y llamar a callback
       * 
       * Ejemplo:
       *    var items = [];
       *    items.push({"inx": data.Items[0].inx.N, "value": data.Items[0].value.S, "key": data.Items[0].key});
       *    self.cache.set(search, items)
       *    callback(err, items);
       */
      let docClient = new AWS.DynamoDB.DocumentClient();
      let paramsItems = [];
      let paramsTerms = {
        TableName: this.tableName,
        KeyConditionExpression: "#k = :xxxx",
        ExpressionAttributeNames: {
          "#k": "key"
        },
        ExpressionAttributeValues: {
          ":xxxx": search
        }
      };
      docClient.query(paramsTerms, function (err, data) {
        if (err) {
          callback(err, null);
        } else {
          data.Items.forEach(function (item) {
            console.log(item)
            paramsItems.push({
              "sort": item.sort,
              "value": item.value,
              "key": item.key
            });
          });

          self.cache.set(search, paramsItems);
          callback(err, paramsItems);
        }
      });
    }
  };

  module.exports = keyvaluestore;