import gzip
import base64
import urllib3

def lambda_handler(event, context):
    compressed_data = event['awslogs']['data']

    # Assuming base64 encoding and gzip compression
    decoded_data = base64.b64decode(compressed_data)
    decompressed_data = gzip.decompress(decoded_data)

    # Decode the decompressed data as UTF-8
    log_lines = decompressed_data.decode('utf-8').splitlines()

    # Concatenate all log lines into a single string
    concatenated_log = ''.join(log_lines)

    # Send the concatenated log to the external HTTP endpoint
    http = urllib3.PoolManager()
    response = http.request(
        'POST',
        'URL',
        body=concatenated_log.encode('utf-8')
    )

    if response.status == 200:
        print('Data sent to external endpoint successfully')
    else:
        print('Error sending data to external endpoint:', response.status)

    return {
        'statusCode': 200,
        'body': 'Data concatenated and sent successfully'
    }
