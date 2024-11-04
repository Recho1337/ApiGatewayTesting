def lambda_handler(event, context):
    try:
        message = f"{event['message']}!"
        return {
            'message': message
        }
    except KeyError:
        return {
            'message': "Error: 'message' key not found in event."
        }