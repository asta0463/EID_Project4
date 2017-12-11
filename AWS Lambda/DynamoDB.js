//A Node.js code to populate the DynamoDB table
//Reference : http://docs.aws.amazon.com/sdk-for-javascript/v2/developer-guide/dynamodb-example-table-read-write.html

'use strict';
var AWS = require("aws-sdk");
// Create the DynamoDB service object
var ddb = new AWS.DynamoDB({apiVersion: '2012-10-08'});

//Lambda function
exports.handler = (event, context, callback) => {
    console.log('Received event:', JSON.stringify(event, null, 2));  //logging the input into Cloudwatch logs
    console.log('Current temperature  =', event.Temperature)); 
    console.log('Current Humidity =', event.Humidity);
    console.log('Count =', event.Count);
    var t=parseFloat(event.Temperature);       //converting received String to object of type Float Number
    var h=parseFloat(event.Humidity);
    var count=parseFloat(event.Count);

    ddb.listTables(function(err, data) {       //list the tables
      console.log(JSON.stringify(data, null, '  '));
    });
var paramsdb = {
  TableName: 'TempHum',
  Item: {
    'COUNT' : {S:event.Count},
    'TEMPERATURE': {S: event.Temperature},
    'HUMIDITY' : {S: event.Humidity}
  }
};

//insert into table
ddb.putItem(paramsdb, function(err, data) {
  if (err) {
    console.log("Error", err);
  } else {
    console.log("Success-added", data);
  }
});
};
