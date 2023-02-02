from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from datetime import datetime
from pandas import DataFrame
from io import BytesIO
import pandas as pd
import snscrape.modules.twitter as sntwitter

# conexao utilizada para interagir com o MinIO
# detalhes da conexao no arquivo 'airflow_conn.txt'
s3 = S3Hook("minio_s3_docker")

# declarando variaveis a serem utilizadas como padrao
# now -> utilizada para padrao de nomenclatura do arquivo .parquet
# today -> utilizada como padrao para data final de buscas dos tweets
now = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
today = datetime.today().strftime('%Y-%m-%d')

# utiliza as funcoes criadas [search_hashtags, create_bucket, upload_parquet_to_minio]
# para gerar o DataFrame(pandas) com os tweets, criar o bucket desejado(caso nao exista)
# e salvar o arquivo em formato parquet
# @param bucket -> nome do bucket que sera usado no processo
# @param hashtag -> hashtag a ser buscada
# @param num_tweets -> numero de tweets a serem salvos
# @param since_date -> data inicial da busca
# @param hashtag_name -> data final da busca (default = hoje['yyyy-mm-dd'])
def process_all(bucket: str, hashtag: str, num_tweets: int, since_date: str, until_date: str=today):

    df_tweets = search_hashtag(hashtag, num_tweets, since_date, until_date)

    create_bucket(bucket)

    upload_parquet_to_minio(df_tweets, bucket, now, hashtag)

# Faz a busca da hashtag e retorna um DataFrame contendo as infos de cada tweet
# @param hashtag -> hashtag a ser buscada
# @param num_tweets -> numero de tweets a serem salvos
# @param since_date -> data inicial da busca
# @param hashtag_name -> data final da busca
def search_hashtag(hashtag: str, num_tweets: int, since_date: str, until_date: str):

    tweet_count = num_tweets
    text_query = hashtag
    since_date = since_date
    until_date = until_date
    query_hash = f'{text_query} since:{since_date} until:{until_date}'

    tweets_list = []
    for i,tweet in enumerate(sntwitter.TwitterSearchScraper(query_hash).get_items()):
        if i >= tweet_count:
            break

        tweets_list.append([tweet.date, tweet.rawContent, tweet.renderedContent, tweet.hashtags])

    df_from_tweets_list = pd.DataFrame(tweets_list, columns=['date', 'content', 'rendered_content', 'hashtags'])

    return df_from_tweets_list

# Salva o arquivo .parquet no bucket indicado, em uma estrutura de pasta e arquivo
# @param df -> DataFrame(pandas) criado a partir da busca pelos tweets
# @param bucket -> Nome do bucket em que o arquivo sera salvo
# @param filename -> Nome do arquivo .parquet
# @param hashtag_name -> Valor buscado na hashtag
def upload_parquet_to_minio(df: DataFrame, bucket: str, filename: str, hashtag_name: str): 
    s3_conn = s3.get_conn()

    out_buffer = BytesIO()
    out_buffer.seek(0)
    df.to_parquet(out_buffer, index=False)
    s3_conn.put_object(Bucket=bucket, Body=out_buffer.getvalue(), Key=f'{hashtag_name}/{filename}.parquet')
    out_buffer.close()

# Cria o bucket caso ainda não exista um com o nome indicado
# @param bucket -> Nome desejado para o Bucket
def create_bucket(bucket: str):
    bucket_exists = s3.check_for_bucket(bucket_name=bucket)

    if not bucket_exists:
        s3.create_bucket(bucket_name=bucket)
    else:
        print('bucket already exists')
        pass

default_args = {
    'owner': 'Bassam',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 28),
    'schedule_interval': None
}

with DAG(
    dag_id='minio_s3_dag',
    default_args=default_args,
    start_date=datetime(2023, 1, 28),
    catchup=False
) as dag:
    pass
    t1 = PythonOperator(
        task_id='search_tt_covid',
        python_callable=process_all,
        op_args = ["twitter-search", "#covid19", 6, "2023-01-01"]
    )
    t2 = PythonOperator(
        task_id='search_tt_serasa',
        python_callable=process_all,
        op_args = ["twitter-search", "#serasa", 6, "2023-01-01"]
    )

t1 >> t2
