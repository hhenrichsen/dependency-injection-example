podman run --rm -v di-example-db-data:/var/lib/postgresql/data -v ./initdb:/docker-entrypoint-initdb.d:ro -p 5432:5432 -e POSTGRES_PASSWORD=hunter2 -e POSTGRES_DB=app --name di-example-db -d postgres:latest