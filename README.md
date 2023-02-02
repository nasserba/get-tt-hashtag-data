# get-tt-hashtag-data

# Overview

  De forma geral, temos como finalidades para o projeto:
   - Realizar buscas de hashtags no Twitter
   - Possuir a possibilidade de agendar esse fluxo
   - Armazenar os dados em uma estrutura de Datalake
   
# Implementação
 
  Para a implementação, foram utilizadas as seguintes tecnologias:
   - Motor de busca da hashtag (extração, tratamento e carga de dados): Python
   - Orquestração: Airflow
   - Armazenamento: MinIO (hospedado local)
   - Deploy: docker-compose
   
# Desenvolvimento

   - Busca pela Hashtag: utilizando o pacote `snscrape` do Python, foi possível acessar o Twitter e os tweets sem a necessidade do uso da API
   - Orquestração: utilizando a imagem docker, a configuração inicial do Airflow foi realizada
   - Armazenamento: utilizando a imagem docker, MinIO foi configurado para armazenar os dados no caminho `minio/datalake`
   
   A solução está contida no arquivo `solution.py`, que já possui todos os passos para a extração e carga de dados. Utilizando `snscrape.modules.twitter`, possibilitou o acesso aos dados de tweets, após extrair existe um passo simples de organização das informações extraídas, e por fim a carga dos dados no MinIO transformando o arquivo em `.parquet`. A organização dos arquivos dentro do MinIO foi feita da seguinte maneira:
