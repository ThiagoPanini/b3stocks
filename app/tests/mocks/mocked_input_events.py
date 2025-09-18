# Input event for streaming DynamoDB data
MOCKED_DYNAMODB_STREAM_EVENT = {
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
                    "owner_mail": {
                        "S": "panini.development@gmail.com"
                    }
                },
                "NewImage": {
                    "owner_name": {
                        "S": "Thiago Panini"
                    },
                    "updated_at": {
                        "S": "2025-09-10T18: 08: 01.310809+00: 00"
                    },
                    "owner_mail": {
                        "S": "panini.development@gmail.com"
                    },
                    "created_at": {
                        "S": "2025-09-10T17: 43: 42.823630+00: 00"
                    },
                    "source_url": {
                        "S": "s3: //b3stocks-artifacts-596533897380-sa-east-1/investment_portfolios/b3_investment_portfolio.yaml"
                    },
                    "stocks": {
                        "S": '[{"company_name": "VALE S.A.", "ticker_code": "VALE3", "stock_type": "ON", "notify_on_threshold": true, "variation_thresholds": {"upper_bound": 0.02, "lower_bound": 0.02}}, {"company_name": "BRASKEM", "ticker_code": "BRKM5", "stock_type": "PNA", "notify_on_threshold": true, "variation_thresholds": {"upper_bound": 0.02, "lower_bound": 0.02}}]'
                    }
                },
                "OldImage": {
                    "owner_name": {
                        "S": "Thiago Panini"
                    },
                    "updated_at": {
                        "S": "2025-09-10T18:06:52.131675+00:00"
                    },
                    "owner_mail": {
                        "S": "panini.development@gmail.com"
                    },
                    "created_at": {
                        "S": "2025-09-10T17:43:42.823630+00:00"
                    },
                    "source_url": {
                        "S": "s3://b3stocks-artifacts-259068869404-us-east-1/investment_portfolios/b3_investment_portfolio.yaml"
                    },
                    "stocks": {
                        "S": '[{"company_name": "VALE S.A.", "ticker_code": "VALE3", "stock_type": "ON", "notify_on_threshold": true, "variation_thresholds": {"upper_bound": 0.02, "lower_bound": 0.02}}, {"company_name": "BRASKEM", "ticker_code": "BRKM5", "stock_type": "PNA", "notify_on_threshold": true, "variation_thresholds": {"upper_bound": 0.02, "lower_bound": 0.02}}]'
                    }
                },
                "SequenceNumber": "114700001686381119587164",
                "SizeBytes": 1238,
                "StreamViewType": "NEW_AND_OLD_IMAGES"
            },
            "eventSourceARN": "arn:aws:dynamodb:us-east-1:259068869404:table/tbl_b3stocks_investment_portfolio/stream/2025-09-10T17:33:14.049"
        }
    ]
}