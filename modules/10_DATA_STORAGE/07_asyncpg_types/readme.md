### Запуск Postgres

```bash
docker run --name postgres-15 \
  -e POSTGRES_PASSWORD=password \
  -e POSTGRES_USER=user \
  -e POSTGRES_DB=my_db \
  -p 5432:5432 \
  -v /data:/var/lib/postgresql/data \
  -d postgres:15
```