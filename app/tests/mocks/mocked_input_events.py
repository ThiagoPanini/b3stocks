# Input event for streaming DynamoDB data
MOCKED_DYNAMODB_STREAMS_EVENT_FOR_ACTIVE_STOCKS_TABLE = {
    "Records": [
        {
            "eventID": "5fdc13396c35cc4306767ecf8920e014",
            "eventName": "MODIFY",
            "eventVersion": "1.1",
            "eventSource": "aws:dynamodb",
            "awsRegion": "sa-east-1",
            "dynamodb": {
                "ApproximateCreationDateTime": 1757527681.0,
                "Keys": {
                    "code": {
                        "S": "AMBV4"
                    }
                },
                "NewImage": {
                    "company_name": {
                        "S": "AMBEV"
                    },
                    "created_at": {
                        "S": "2025-09-26T22:29:03.193669-03:00"
                    },
                    "request_config": {
                        "S": '{ "headers" : { "M" : { "User-Agent" : { "S" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36" } } }, "retry_config" : { "M" : { "backoff_factor" : { "N" : "0.1" }, "num_retries" : { "N" : "3" }, "status_forcelist" : { "L" : [ { "N" : "500" }, { "N" : "502" }, { "N" : "503" }, { "N" : "504" } ] } } }, "url" : { "S" : "https://www.fundamentus.com.br/resultado.php" }, "timeout" : { "N" : "10" }, "request_kwargs" : { "M" : {  } } } }'
                    },
                    "updated_at": {
                        "S": "2025-09-26T22:29:03.193775-03:00"
                    }
                },
                "NewImage": {
                    "company_name": {
                        "S": "AMBEV"
                    },
                    "created_at": {
                        "S": "2025-09-26T22:29:03.193669-03:00"
                    },
                    "request_config": {
                        "S": '{ "headers" : { "M" : { "User-Agent" : { "S" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36" } } }, "retry_config" : { "M" : { "backoff_factor" : { "N" : "0.1" }, "num_retries" : { "N" : "3" }, "status_forcelist" : { "L" : [ { "N" : "500" }, { "N" : "502" }, { "N" : "503" }, { "N" : "504" } ] } } }, "url" : { "S" : "https://www.fundamentus.com.br/resultado.php" }, "timeout" : { "N" : "10" }, "request_kwargs" : { "M" : {  } } } }'
                    },
                    "updated_at": {
                        "S": "2025-09-26T22:29:03.193775-03:00"
                    }
                },
                "SequenceNumber": "114700001686381119587164",
                "SizeBytes": 1238,
                "StreamViewType": "NEW_AND_OLD_IMAGES"
            },
            "eventSourceARN": "arn:aws:dynamodb:us-east-1:259068869404:table/tbl_b3stocks_active_stocks/stream/2025-09-10T17:33:14.049"
        }
    ]
}

# Input event for SQS messages
MOCKED_SQS_EVENT_FOR_ACTIVE_STOCKS_QUEUE = {
    "Records": [
        {
            "messageId": "e17c9ead-b344-4ccc-b3b9-6ffb364f08d1",
            "receiptHandle": "AQEBVTD8KKnWQ7+Yi/uF9w5X/FM1WG/C3ujDRM36GQpvVth5Jryrj4AA5Fbx91+orXCt6K75XWHUDqyWrgiTyTS22a9BQ/UjM4gOKv3v9P5n5WyfS4LDvV514TzLo47aYVQyoyzPJDFysA4hZAtjSC/sN5r40krbsV0NeG3xT2D9RYxL6N1PF98EABLPbzMmYqsFJukTmYOVdWKW/LrdA3+WsAWuLDDX3TzZwN2rHAYI7uTpc9/5QVPvP0q4xke7PK1tzEtp4e3f1BsxRNVEQVQ5aztwRgiuuvhjjtQmMwsoZzvCxtjTziQnHep9VvXivagPoFRsy84ntTZG5QuUPRqRNKiQJHTxeYAYqi7sBMk8s5/tzCffRWiwxwkpQ5qs1XeU6WtFi6OLapYVk5zoBA1jOc5LPtsbeQ4uKqYiq9L/SRc=",
            "body": "{\n  \"Type\" : \"Notification\",\n  \"MessageId\" : \"1d13ae0d-ed5b-5bd1-aa2a-cf4b9867a119\",\n  \"TopicArn\" : \"arn:aws:sns:sa-east-1:596533897380:b3stocks-active-stocks\",\n  \"Message\" : \"{\\\"code\\\": \\\"VALE3\\\",\\\"total_expected_messages\\\": \\\"991\\\"}\",\n  \"Timestamp\" : \"2025-09-18T21:00:44.444Z\",\n  \"SignatureVersion\" : \"1\",\n  \"Signature\" : \"RinNEcLNZ9zGcqwctJrTbBzIWUlMqRSknj/U0B7aocCsjm2YpSUZIghNYsYW94uGbQ08A/jW83Rd3AMw8VkYTQi4JW0MwVN6V5aAOdyp8XNlH3b+5ZZprAtAUToFRTmUczN/sa2W+bJEy5VF0bLRB8Dp+KDBjlYjtIvtyW1zEYahPAA+aP/cITyO2MO0WGLfxL/3qAXItpYs0bHyHQuMgG5TqOmb0ubQkd6vXNWso+iyLC5uK6WqN89XBefQUFfwmei1F/OBl/LvwGCQcKk4zh4njgPocAIsTYiVRRTptF59tJ74g8TIjxSlDbXsMftOXxfvX2U5ny9oexLG5fd0OA==\",\n  \"SigningCertURL\" : \"https://sns.sa-east-1.amazonaws.com/SimpleNotificationService-6209c161c6221fdf56ec1eb5c821d112.pem\",\n  \"UnsubscribeURL\" : \"https://sns.sa-east-1.amazonaws.com/?Action=Unsubscribe&SubscriptionArn=arn:aws:sns:sa-east-1:596533897380:b3stocks-active-stocks:02f6f99d-8ecc-4262-8797-d8ae28b73922\"\n}",
            "attributes": {
                "ApproximateReceiveCount": "1",
                "AWSTraceHeader": "Root=1-68cc72de-271c395f0346036f561b2fa3;Parent=3e25f64c0d58a38a;Sampled=0;Lineage=1:98b02273:0",
                "SentTimestamp": "1758229244474",
                "SenderId": "AIDAIOA2GYWSHW4E2VXIO",
                "ApproximateFirstReceiveTimestamp": "1758229244476"
            },
            "messageAttributes": {},
            "md5OfMessageAttributes": "None",
            "md5OfBody": "d38152ce3de9636ae235cb5e3c3b3987",
            "eventSource": "aws:sqs",
            "eventSourceARN": "arn:aws:sqs:sa-east-1:596533897380:b3stocks-fundamentus-eod-stock-metrics",
            "awsRegion": "sa-east-1"
        },
        {
            "messageId": "382b491f-c088-4bfb-8459-f355ec09ae51",
            "receiptHandle": "AQEBO6bMVcrQ4I/zJcEPoB7eK1bwrCWHe6CET/Sz0wNQtYhBH3pANglt0uygnA399lvf/nhZCh5zJffMi4fneNwVuaIj2vAlVQIxHUGMsPvYXlYcLWl9dsjrSPljIdYRg039ql5NruKpLigZuVIRpdtNOZhSzyh7XNK5Pf5FsbJkXWDeBwbwNf975VervLpBpkaJlQ2oc2+z3gFbLncfjdqn8JFh/F6amTRvVJwv/IIQSiTwrCfzOBayS6mQq4qkTNRX5yu31L9QMumGzMhnQt3Syz5cGdTAHJIwaRq4NOSTGNyW3MMmhqIOpWTBpMVCd3J4qd9Gsls854gmyya8hDUoJvXyzhPfso5ncMak8VMNEW70Y6Yc1jRbxG2HlXayflYWBV8E1zznFe9dgm2eg88iG1ssdgf/Rj8vOeXOg473zMM=",
            "body": "{\n  \"Type\" : \"Notification\",\n  \"MessageId\" : \"f0a84c44-d366-528a-9385-2d02a65a7842\",\n  \"TopicArn\" : \"arn:aws:sns:sa-east-1:596533897380:b3stocks-active-stocks\",\n  \"Message\" : \"{\\\"code\\\": \\\"ITUB4\\\",\\\"total_expected_messages\\\": \\\"991\\\"}\",\n  \"Timestamp\" : \"2025-09-18T21:00:44.444Z\",\n  \"SignatureVersion\" : \"1\",\n  \"Signature\" : \"st7CG5JW9NF3wPrQZNmkYamFmOqiPOZA67b3cqDbIOU1OFatyWxCSObtxE9FFc/+vU+eN3k/iY05A52e7m/1fUQHzoyhrceyzSmLIxoRUpb8aO+bC01ni13hb94rEuuUA8ZgSjEhaRro9WHtlgMlrbRt6JqAU6NxRnH6xBOoO92Sau4HxRUlShkrfIGSoiN21IDHVUb3vYSUOUkLZWYx2a8JiGSO5FzP6tW7lqM2xVrKwwISaM8cNLecXF7ik/GBF+Ez6Upr8aa3TI1ZnDFpOrXeBslwtOTm9NfAB9i3JJVxUVmg3mXdG+C/efdLQrkCLaa4yAnpP6LfESPVlvG7lQ==\",\n  \"SigningCertURL\" : \"https://sns.sa-east-1.amazonaws.com/SimpleNotificationService-6209c161c6221fdf56ec1eb5c821d112.pem\",\n  \"UnsubscribeURL\" : \"https://sns.sa-east-1.amazonaws.com/?Action=Unsubscribe&SubscriptionArn=arn:aws:sns:sa-east-1:596533897380:b3stocks-active-stocks:02f6f99d-8ecc-4262-8797-d8ae28b73922\"\n}",
            "attributes": {
                "ApproximateReceiveCount": "1",
                "AWSTraceHeader": "Root=1-68cc72de-271c395f0346036f561b2fa3;Parent=3e25f64c0d58a38a;Sampled=0;Lineage=1:98b02273:0",
                "SentTimestamp": "1758229244481",
                "SenderId": "AIDAIOA2GYWSHW4E2VXIO",
                "ApproximateFirstReceiveTimestamp": "1758229244483"
            },
            "messageAttributes": {},
            "md5OfMessageAttributes": "None",
            "md5OfBody": "dd5faa48ade458892e6421378ba9f38b",
            "eventSource": "aws:sqs",
            "eventSourceARN": "arn:aws:sqs:sa-east-1:596533897380:b3stocks-fundamentus-eod-stock-metrics",
            "awsRegion": "sa-east-1"
        }
    ]
}

# Input event for streaming DynamoDB data
MOCKED_DYNAMODB_STREAMS_EVENT_FOR_BATCH_PROCESS_CONTROL_TABLE = {
   "Records":[
      {
         "eventID":"4c961926dd63a1dafe6a49dcbf1c956e",
         "eventName":"MODIFY",
         "eventVersion":"1.1",
         "eventSource":"aws:dynamodb",
         "awsRegion":"sa-east-1",
         "dynamodb":{
            "ApproximateCreationDateTime":1758839339.0,
            "Keys":{
               "process_name":{
                  "S":"PROCESS_FUNDAMENTUS_EOD_STOCK_METRICS"
               },
               "execution_date":{
                  "S":"2025-09-25"
               }
            },
            "NewImage":{
               "finished_at":{
                  "NULL":"true"
               },
               "processed_items":{
                  "N":"0"
               },
               "updated_at":{
                  "S":"2025-09-25T19:28:57.728243-03:00"
               },
               "execution_date":{
                  "S":"2025-09-25"
               },
               "process_name":{
                  "S":"PROCESS_FUNDAMENTUS_EOD_STOCK_METRICS"
               },
               "process_status":{
                  "S":"COMPLETED"
               },
               "created_at":{
                  "S":"2025-09-25T19:28:57.728242-03:00"
               },
               "total_items":{
                  "N":"991"
               }
            },
            "OldImage":{
               "finished_at":{
                  "S":"2025-09-25T18:42:43.909507-03:00"
               },
               "processed_items":{
                  "N":"991"
               },
               "updated_at":{
                  "S":"2025-09-25T18:42:43.789892-03:00"
               },
               "execution_date":{
                  "S":"2025-09-25"
               },
               "process_name":{
                  "S":"PROCESS_FUNDAMENTUS_EOD_STOCK_METRICS"
               },
               "process_status":{
                  "S":"COMPLETED"
               },
               "created_at":{
                  "S":"2025-09-25T18:36:32.968172-03:00"
               },
               "total_items":{
                  "N":"991"
               }
            },
            "SequenceNumber":"4392400001347320812525114",
            "SizeBytes":552,
            "StreamViewType":"NEW_AND_OLD_IMAGES"
         },
         "eventSourceARN":"arn:aws:dynamodb:sa-east-1:596533897380:table/tbl_b3stocks_batch_process_control/stream/2025-09-25T16:44:53.750"
      }
   ]
}

