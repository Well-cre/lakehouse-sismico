# Databricks notebook source
# MAGIC %md
# MAGIC # 🌎 Lakehouse Sísmico
# MAGIC
# MAGIC ## Comparação entre USGS e EMSC
# MAGIC
# MAGIC ### Dashboard Analítica • Ano 2025
# MAGIC
# MAGIC Este dashboard apresenta a comparação dos eventos sísmicos obtidos através de duas fontes independentes:
# MAGIC
# MAGIC - 🇺🇸 USGS (United States Geological Survey)
# MAGIC - 🇪🇺 EMSC (European-Mediterranean Seismological Centre)
# MAGIC
# MAGIC Arquitetura implementada:
# MAGIC
# MAGIC API → Landing → Bronze → Delta Lake
# MAGIC
# MAGIC Objetivos:
# MAGIC
# MAGIC - Comparar a quantidade de eventos registrados por cada fonte
# MAGIC - Validar a consistência dos dados na camada Bronze
# MAGIC - Analisar diferenças mensais entre as APIs
# MAGIC - Demonstrar a integração de múltiplas fontes utilizando Auto Loader

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC SELECT
# MAGIC     'USGS' AS fonte,
# MAGIC     SUM(size(features)) AS eventos
# MAGIC FROM sismos.bronze.usgs_raw
# MAGIC
# MAGIC UNION ALL
# MAGIC
# MAGIC SELECT
# MAGIC     'EMSC',
# MAGIC     SUM(size(features))
# MAGIC FROM sismos.bronze.emsc_raw

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC     'USGS' AS fonte,
# MAGIC     COUNT(*) AS arquivos
# MAGIC FROM sismos.bronze.usgs_raw
# MAGIC
# MAGIC UNION ALL
# MAGIC
# MAGIC SELECT
# MAGIC     'EMSC' AS fonte,
# MAGIC     COUNT(*) AS arquivos
# MAGIC FROM sismos.bronze.emsc_raw

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC     regexp_extract(_source_file,'mes=([0-9]+)',1) AS mes,
# MAGIC     metadata.count AS diz_a_api,
# MAGIC     size(features) AS na_bronze,
# MAGIC     metadata.count = size(features) AS bate
# MAGIC FROM sismos.bronze.usgs_raw
# MAGIC ORDER BY mes

# COMMAND ----------

# MAGIC %sql
# MAGIC WITH usgs AS (
# MAGIC     SELECT
# MAGIC         regexp_extract(_source_file,'mes=([0-9]+)',1) mes,
# MAGIC         size(features) eventos_usgs
# MAGIC     FROM sismos.bronze.usgs_raw
# MAGIC ),
# MAGIC emsc AS (
# MAGIC     SELECT
# MAGIC         regexp_extract(_source_file,'mes=([0-9]+)',1) mes,
# MAGIC         size(features) eventos_emsc
# MAGIC     FROM sismos.bronze.emsc_raw
# MAGIC )
# MAGIC
# MAGIC SELECT
# MAGIC     u.mes,
# MAGIC     (e.eventos_emsc - u.eventos_usgs) AS diferenca
# MAGIC FROM usgs u
# MAGIC JOIN emsc e
# MAGIC ON u.mes = e.mes
# MAGIC ORDER BY u.mes

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC     regexp_extract(_source_file, 'mes=([0-9]+)', 1) AS mes,
# MAGIC     size(features) AS eventos
# MAGIC FROM sismos.bronze.usgs_raw
# MAGIC ORDER BY mes

# COMMAND ----------

# MAGIC %sql
# MAGIC WITH usgs AS (
# MAGIC     SELECT
# MAGIC         regexp_extract(_source_file,'mes=([0-9]+)',1) AS mes,
# MAGIC         size(features) AS eventos_usgs
# MAGIC     FROM sismos.bronze.usgs_raw
# MAGIC ),
# MAGIC
# MAGIC emsc AS (
# MAGIC     SELECT
# MAGIC         regexp_extract(_source_file,'mes=([0-9]+)',1) AS mes,
# MAGIC         size(features) AS eventos_emsc
# MAGIC     FROM sismos.bronze.emsc_raw
# MAGIC )
# MAGIC
# MAGIC SELECT
# MAGIC     u.mes,
# MAGIC     u.eventos_usgs,
# MAGIC     e.eventos_emsc,
# MAGIC     e.eventos_emsc - u.eventos_usgs AS diferenca
# MAGIC FROM usgs u
# MAGIC INNER JOIN emsc e
# MAGIC     ON u.mes = e.mes
# MAGIC ORDER BY u.mes;

# COMMAND ----------

# MAGIC %md
# MAGIC ## 📊 Comparação Mensal de Eventos
# MAGIC
# MAGIC A tabela abaixo apresenta a quantidade de eventos registrados mensalmente pelas duas APIs, permitindo identificar diferenças de cobertura e volume de registros entre as fontes.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC     regexp_extract(_source_file,'mes=([0-9]+)',1) AS mes,
# MAGIC     metadata.count AS api,
# MAGIC     size(features) AS bronze,
# MAGIC     metadata.count = size(features) AS validacao
# MAGIC FROM sismos.bronze.usgs_raw
# MAGIC ORDER BY mes;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC     regexp_extract(_source_file,'mes=([0-9]+)',1) AS mes,
# MAGIC     metadata.count AS api,
# MAGIC     size(features) AS bronze,
# MAGIC     metadata.count = size(features) AS validacao
# MAGIC FROM sismos.bronze.emsc_raw
# MAGIC ORDER BY mes;

# COMMAND ----------

# MAGIC %sql
# MAGIC WITH usgs AS (
# MAGIC     SELECT
# MAGIC         regexp_extract(_source_file,'mes=([0-9]+)',1) AS mes,
# MAGIC         size(features) AS eventos_usgs
# MAGIC     FROM sismos.bronze.usgs_raw
# MAGIC ),
# MAGIC emsc AS (
# MAGIC     SELECT
# MAGIC         regexp_extract(_source_file,'mes=([0-9]+)',1) AS mes,
# MAGIC         size(features) AS eventos_emsc
# MAGIC     FROM sismos.bronze.emsc_raw
# MAGIC )
# MAGIC
# MAGIC SELECT
# MAGIC     u.mes,
# MAGIC     u.eventos_usgs,
# MAGIC     e.eventos_emsc,
# MAGIC     (e.eventos_emsc - u.eventos_usgs) AS diferenca
# MAGIC FROM usgs u
# MAGIC JOIN emsc e
# MAGIC     ON u.mes = e.mes
# MAGIC ORDER BY u.mes;
# MAGIC

# COMMAND ----------

# MAGIC %sql
# MAGIC WITH usgs AS (
# MAGIC     SELECT
# MAGIC         regexp_extract(_source_file,'mes=([0-9]+)',1) AS mes,
# MAGIC         size(features) AS eventos_usgs
# MAGIC     FROM sismos.bronze.usgs_raw
# MAGIC ),
# MAGIC emsc AS (
# MAGIC     SELECT
# MAGIC         regexp_extract(_source_file,'mes=([0-9]+)',1) AS mes,
# MAGIC         size(features) AS eventos_emsc
# MAGIC     FROM sismos.bronze.emsc_raw
# MAGIC )
# MAGIC
# MAGIC SELECT
# MAGIC     u.mes,
# MAGIC     u.eventos_usgs,
# MAGIC     e.eventos_emsc,
# MAGIC     ROUND(
# MAGIC         (e.eventos_emsc * 100.0 / u.eventos_usgs),
# MAGIC         2
# MAGIC     ) AS percentual
# MAGIC FROM usgs u
# MAGIC JOIN emsc e
# MAGIC     ON u.mes = e.mes
# MAGIC ORDER BY u.mes;

# COMMAND ----------

# MAGIC %sql
# MAGIC WITH usgs AS (
# MAGIC     SELECT
# MAGIC         regexp_extract(_source_file,'mes=([0-9]+)',1) AS mes,
# MAGIC         size(features) AS eventos_usgs
# MAGIC     FROM sismos.bronze.usgs_raw
# MAGIC ),
# MAGIC emsc AS (
# MAGIC     SELECT
# MAGIC         regexp_extract(_source_file,'mes=([0-9]+)',1) AS mes,
# MAGIC         size(features) AS eventos_emsc
# MAGIC     FROM sismos.bronze.emsc_raw
# MAGIC )
# MAGIC
# MAGIC SELECT
# MAGIC     u.mes,
# MAGIC     u.eventos_usgs,
# MAGIC     e.eventos_emsc,
# MAGIC     (e.eventos_emsc - u.eventos_usgs) AS diferenca
# MAGIC FROM usgs u
# MAGIC JOIN emsc e
# MAGIC     ON u.mes = e.mes
# MAGIC ORDER BY diferenca DESC;

# COMMAND ----------

# MAGIC %md
# MAGIC ## ✅ Teste de Idempotência
# MAGIC
# MAGIC Após a primeira carga, os notebooks foram executados novamente.
# MAGIC
# MAGIC O Auto Loader utilizou os checkpoints já existentes e não reprocessou arquivos previamente carregados, evitando duplicidade na camada Bronze.

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE HISTORY sismos.bronze.emsc_raw

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE HISTORY sismos.bronze.usgs_raw

# COMMAND ----------

# MAGIC %md
# MAGIC ## ✅ Histórico Delta - EMSC
# MAGIC
# MAGIC O Delta Lake mantém o histórico completo de operações realizadas sobre a tabela.
# MAGIC
# MAGIC A consulta abaixo demonstra que a segunda execução do Auto Loader não adicionou novas linhas, comprovando a idempotência do processo através do checkpoint.

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE HISTORY sismos.bronze.emsc_raw

# COMMAND ----------

# MAGIC %md
# MAGIC ## ✅ Histórico Delta - USGS

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE HISTORY sismos.bronze.usgs_raw
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ### Resultado
# MAGIC
# MAGIC Após a reexecução dos notebooks Bronze:
# MAGIC
# MAGIC - Nenhum arquivo foi reprocessado.
# MAGIC - Nenhuma linha foi duplicada.
# MAGIC - Os checkpoints preservaram o estado da ingestão.
# MAGIC - O Delta Lake manteve a consistência das tabelas.
# MAGIC
# MAGIC Esse comportamento garante a idempotência do pipeline de dados.

# COMMAND ----------

# MAGIC %md
# MAGIC ## ✅ Conclusão
# MAGIC
# MAGIC Foram integradas duas fontes independentes de dados sísmicos:
# MAGIC
# MAGIC - USGS (United States Geological Survey)
# MAGIC - EMSC (European-Mediterranean Seismological Centre)
# MAGIC
# MAGIC Os dados foram extraídos de APIs públicas, armazenados em Landing Zone e processados na camada Bronze utilizando Auto Loader e Delta Lake.
# MAGIC
# MAGIC Resultados obtidos:
# MAGIC
# MAGIC - USGS: 29.323 eventos
# MAGIC - EMSC: 82.254 eventos
# MAGIC
# MAGIC A análise demonstrou diferenças significativas entre as fontes em todos os meses de 2025, evidenciando variações de cobertura e catalogação entre os provedores.