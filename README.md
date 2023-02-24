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
   
![diag2](https://user-images.githubusercontent.com/62388489/216341418-bb21d7d0-47ba-46eb-9041-5131894c01aa.png)

  A DAG foi desenvolvida para adicionar tasks cada vez que necessitar fazer buscas de uma hashtag diferente, salvando os dados seguindo o padrão indicado no fluxo acima.
  
  A solução pode ser utilizada com o comando `docker-compose up` e é processada localmente, o Ariflow na porta 8080 e o MinIO na 9000 (UI na porta 9001), o MinIO é acessado pelo AIrflow pelo pacote s3Hook, pois se assemelha ao produto AWS s3 se tratando de um armazenador de objetos. É necessário configurar uma nova conexão no Airflow, essa conexão está descrita no arquivo `airflow_conn.txt`.
  
# Propostas futuras

   - Organizar as pastas conforme aplicação
   - Criar uma classe externa com as devidas funcionalidades e importar no projeto
   - Criar classe de testes e utilizar o DockerFile para roda-los
