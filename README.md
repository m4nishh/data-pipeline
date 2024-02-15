to build 
```
docker login ghcr.io -u GITHUB_USERNAME
docker build -t ghcr.io/brand-os/data-pipeline:latest --platform linux/amd64 .
docker push ghcr.io/brand-os/data-pipeline:latest
docker run -p 8080:8080 ghcr.io/brand-os/data-pipeline:latest
```
user github personal access token (classic) for logging in 