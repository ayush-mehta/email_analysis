def main(event, context):
    
    return {
        'statusCode': 200,
        'body': 'Hello from Lambda!'
    }

if __name__ == "__main__":
    # For local testing, call main with dummy event and context
    result = main({}, {})
    print(result)