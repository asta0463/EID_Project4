//Code to store the incoming MQTT messages in an SQS queue along with the running average, minimum and maximum values. An intermediate queue is used to store the latest values which are fetched by the main queue before performing computations again   
'use strict';


var AWS = require("aws-sdk");

exports.handler = (event, context, callback) => {
    console.log('Count =', event.Count);
    var t=parseFloat(event.Temperature);
    var h=parseFloat(event.Humidity);
    var count=parseFloat(event.Count);
    var avg_temp;
    var max_temp;
    var min_temp;
    var latest_temp;
    var one;
    var message;
    var body;
    var avg_temp1;
    var max_temp1;
    var min_temp1;
    var avgtempn;
    var avg_tempm;
    var avg_hum;
    var max_hum;
    var min_hum;
    var latest_hum;
    var avg_hum1;
    var max_hum1;
    var min_hum1;
    var avghumn;
    var avg_humm;
    var queueURL1= "https://sqs.us-east-1.amazonaws.com/499557241041/P3_QUEUE";  //intermediate Q
    var queueURL2= "https://sqs.us-east-1.amazonaws.com/499557241041/P3_2";
    var sqs1 = new AWS.SQS();  ////intermediate Q
    var sqs2 = new AWS.SQS();  //main
    //if the count value is 1 , it is the first MQTT message- the average , minimum, max will all be equal to that value
    if(event.Count==1){
        avg_temp=t;
        max_temp=t;
        min_temp=t;
        avg_hum=h;
        max_hum=h;
        min_hum=h;
        var myObj = { 
            "AvgT":avg_temp, 
            "MaxT":max_temp,
            "MinT":min_temp, 
            "LatestT":t,
            "AvgH":avg_hum, 
            "MaxH":max_hum,
            "MinH":min_hum, 
            "LatestH":h,
        };
        var msg = JSON.stringify(myObj);
        console.log("Message to send: " + msg);
        var params = {
        DelaySeconds: 0,
        MessageAttributes: {
                       "CountVal":  {
                                    DataType: "String",
                                    StringValue:event.Count 
                                    },
                           },
        MessageBody: msg,
        QueueUrl: "https://sqs.us-east-1.amazonaws.com/499557241041/P3_QUEUE"  //intermediate queue
        };
        //Adding the above message in both queues
        sqs1.sendMessage(params, function(err, data) {
            if (err) {
                console.log("Error sending msg to P3_Q", err);
            } else {
                console.log("Success -data sent to P3_Q",msg);
            }
        });
        var params5 = {
        DelaySeconds: 0,
        MessageAttributes: {
                            "CountVal": {
                                        DataType: "String",
                                        StringValue:event.Count 
                                    },
                           },
        MessageBody: msg,
        QueueUrl: "https://sqs.us-east-1.amazonaws.com/499557241041/P3_2"
        };
        sqs2.sendMessage(params5, function(err, data) {
            if (err) {
                console.log("Error sending data to P3", err);
            } else {
                console.log("Success -data sent to P3 ", msg);
            }
         });
}
else if(event.Count>1){
        var params2 = {
        AttributeNames: [
        "SentTimestamp"
     ],
     MaxNumberOfMessages: 1,
     MessageAttributeNames: [
        "All"
     ],
     QueueUrl: queueURL1,
     VisibilityTimeout: 0,
     WaitTimeSeconds: 0
    };
    //retrieve and then delete the previous avg,etc from the intermediate queue, use it to compute the running average with the 2nd value(or current) of temp/hum and store the new value of avg,etc in both queues 
    sqs1.receiveMessage(params2, function(err, data) {
      if (err) {
        console.log("Receive Error", err);
      } else {
              console.log("msg extracted",data.Messages[0]);
              message = data.Messages[0];
              body = JSON.parse(message.Body);
              console.log("msg extracted is",body);
            avg_temp1=body.AvgT;
            max_temp1=body.MaxT;
            min_temp1=body.MinT;
            avg_hum1=body.AvgH;
            max_hum1=body.MaxH;
            min_hum1=body.MinH;
            one=1;
            avg_tempm=avg_temp1*(count-one);
            avgtempn=avg_tempm+t;
            avg_temp=avgtempn/count;
            console.log("avg is",avg_temp);
            if(t>max_temp1){
                max_temp=t;
            }else{
                max_temp=max_temp1;
            }
            if(t<min_temp1){
                min_temp=t;
            }else{
                min_temp=min_temp1;
            }


            avg_humm=avg_hum1*(count-one);
            avghumn=avg_humm+h;
            avg_hum=avghumn/count;
            console.log("avg is",avg_hum);
            if(h>max_hum1){
                max_hum=h;
            }else{
                max_hum=max_hum1;
            }
            if(h<min_hum1){
                min_hum=h;
            }else{
                min_hum=min_hum1;
            }
            var myObj2 = { 
                "AvgT":avg_temp, 
                "MaxT":max_temp,
                "MinT":min_temp, 
                "LatestT":t,
                "AvgH":avg_hum, 
                "MaxH":max_hum,
                "MinH":min_hum, 
                "LatestH":h
            };

            var msg2 = JSON.stringify(myObj2);
            var params3 = {
            DelaySeconds: 0,
            MessageAttributes: {
                                "CountVal": {
                                            DataType: "String",
                                            StringValue:event.Count 
                                        },
                               },
            MessageBody: msg2,
            QueueUrl: "https://sqs.us-east-1.amazonaws.com/499557241041/P3_2"
            };
            sqs2.sendMessage(params3, function(err, data) {
                if (err) {
                    console.log("Error", err);
                } else {
                    console.log("Success -data send to P3 ", msg2);
                }
            });
            var params4 = {
            DelaySeconds: 0,
            MessageAttributes: {
                                "CountVal": {
                                            DataType: "String",
                                            StringValue:event.Count 
                                        },

                                },
            MessageBody: msg2,
            QueueUrl: "https://sqs.us-east-1.amazonaws.com/499557241041/P3_QUEUE"
            };
            var deleteParams = {
            QueueUrl: queueURL1,
            ReceiptHandle: data.Messages[0].ReceiptHandle
            };
            sqs1.deleteMessage(deleteParams, function(err, data) {
                if (err) {
                    console.log("Delete Error", err);
                } else {
                    console.log("Message Deleted", data);
                }
            });
            sqs1.sendMessage(params4, function(err, data) {
                if (err) {
                    console.log("Error", err);
                } else {
                    console.log("Success data sent to P3_Q", msg2);
                }
            });
        }
    });
}
};
