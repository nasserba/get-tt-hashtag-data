import pandas as pd
import boto3
import moto
# import pytest
from botocore.exceptions import ClientError
from io import BytesIO

# dataframe mockado para fins de teste
df_mock_s3 = pd.DataFrame(data = {'test': [1,2,3,4]})

# funcao adaptada do codigo fonte da lib s3Hook do airflow
def check_for_bucket(s3, bucket_name):
    """
    Check if bucket_name exists.

    :param bucket_name: the name of the bucket
    :type bucket_name: str
    """
    try:
        s3.head_bucket(Bucket=bucket_name)
        return True
    except ClientError as e:
        return False

@mock_s3
def test_create_bucket(bucket_name):
    s3 = boto3.client('s3')
    
    bucket_exists = check_for_bucket(s3=s3, bucket_name=bucket_name)
    
    if not bucket_exists:
        s3.create_bucket(Bucket=bucket_name)
    else:
        print('bucket already exists')
        pass
    
    bucket_assert = check_for_bucket(s3=s3, bucket_name=bucket_name)
    try:
        assert bucket_assert == True
        print('test_create_bucket: success')
    except:
        print('test_create_bucket: assert failed')


@mock_s3
def test_upload_parquet_to_minio(df, bucket_name, filename, hashtag_name):
    s3_conn = boto3.client('s3')
    s3 = boto3.resource('s3')
    
    out_buffer = BytesIO()
    out_buffer.seek(0)
    df.to_parquet(out_buffer, index=False, compression=None)
    
    s3_conn.create_bucket(Bucket=bucket_name) # adicional para o teste
    s3_conn.put_object(Bucket=bucket_name, Body=out_buffer.getvalue(), Key=f'{hashtag_name}/{filename}.parquet')
    out_buffer.close()

    parquet_object = s3.Object(bucket_name=bucket_name, key=f'{hashtag_name}/{filename}.parquet')
    
    try:
        assert parquet_object.key == f'{hashtag_name}/{filename}.parquet'
        print('test_upload_parquet_to_minio: success')
    except:
        print('test_upload_parquet_to_minio: assert failed')

test_create_bucket('test-moto-bucket')
test_upload_parquet_to_minio(df_mock_s3, 'test-mock-s3','test-mock-s3','test')
