import base64
import json
import pysftp
from google.cloud import storage
from google.cloud import biquery

bucket_name = "storage_project_bucket"  # this is the bucket from storage bucket.Good to take it from env varible
prefix = "20221006/"  # this is the prefix from storage bucket.Good to take it from env varible
table_id='test'
# bucket_name=os.environ.get('bucket_name', 'storage_project_bucket')
# prefix=os.environ.get('prefix', 'Source_prefix is not present')
# project_number=os.environ.get('project_number', 'project_number is not present')
# secret_id=os.environ.get('secret_id', 'secret_id is not present')

def write_to_bq(event):
    row={
        'file_name':event['name']
    }
    bq_client=bigquery.Client()
    return bq_client.insert_rows_json(table_id,[row])

def read_bytes_from_gcs(gcs_client, bucket, file_name):
    bucket = gcs_client.get_bucket(bucket)
    blob = bucket.blob(file_name)
    if blob.exists():
        return blob.download_as_string()
    return None


def upload_to_outbound_sftp(gcs, bucket_name, file_name):
    ftp_host = None
    ftp_user = None
    ftp_pass = None
    ftp_port = 22
    destination_ftp_site=ftp_host
    source_bucket=bucket_name
    destination_file_path = "/tmp/"+file_name.split("/")[1] # change as per your required path
    print('Start uploading from {}/{} to {}/{}'.format(source_bucket, file_name, destination_ftp_site,
                                                         destination_file_path))
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None
    sftp = pysftp.Connection(ftp_host, port=ftp_port, username=ftp_user, password=ftp_pass, cnopts=cnopts)
    data = read_bytes_from_gcs(gcs,source_bucket, file_name)
    f = sftp.open(destination_file_path, 'wb')
    try:
        f.write(data)
        f.flush()
    finally:
        f.close()
    if sftp != None:
        sftp.close()
        sftp = None

    print('Upload completed from {}/{} to {}/{}'.format(source_bucket, file_name, destination_ftp_site,
                                                           destination_file_path))

def main(event, context):
    print(event)
    response = CloudSecret(project_number, secret_id)
    key = response.get_secret_value()
    json_data_dict = json.loads(key)
    gcs = storage.Client()
    bucket_name=event["bucket"]
    file_name=event["name"]
    upload_to_outbound_sftp(gcs,bucket_name,file_name=file_name)

    return f'file uploaded On SFTP server successfully'
