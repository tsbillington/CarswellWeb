# CarswellWeb

Carswell Intelligent Designs Inc. — company portfolio site

Flask + Jinja2 + Tailwind CSS, served by gunicorn in Docker.

## Hosting

Hosted on an **Oracle Cloud Always Free** compute instance
(`VM.Standard.A1.Flex`, ARM Ampere, Ubuntu 22.04).

- **Runtime**: Docker + docker compose (`docker-compose.yml` maps port `8000:8000`)
- **Web server**: gunicorn bound to `0.0.0.0:8000`
- **Firewall**: ingress rules for TCP 8000 (and 80/443) configured on both the
  VCN security list and the instance's iptables
- **Secrets**: `.env` on the server only (gitignored) — see `.env.example`

## Access

```bash
ssh ubuntu@<instance-public-ip>
cd CarswellWeb
```

## Deploy / update

```bash
git pull
docker compose up -d --build
docker compose logs -f   # verify clean startup
```

Site is served at `http://<instance-public-ip>:8000`.

## Local development

```bash
docker compose up --build
# or without Docker:
pip install -r requirements.txt
flask --app app run
```

ssh ubuntu@<public-ip>
cd CarswellWeb
git pull
docker compose up -d --build
