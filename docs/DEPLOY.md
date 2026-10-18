# Deploy (production VPS)

Target: OVH VPS, Debian, 8 GB RAM. Processes run under **PM2**; PostgreSQL 17 (+ pgvector),
Redis and Nginx run as system services. Docker is for local development only.

Replace `example.com` with the real domain once it is chosen (DECISIONS.md #21).

## 1. First-time server setup (as root)

```bash
apt update && apt install -y git curl ca-certificates gnupg nginx certbot python3-certbot-nginx redis-server

# PostgreSQL 17 + pgvector from the PGDG repo (same major version as dev)
install -d /usr/share/postgresql-common/pgdg
curl -fsSL -o /usr/share/postgresql-common/pgdg/apt.postgresql.org.asc \
  https://www.postgresql.org/media/keys/ACCC4CF8.asc
echo "deb [signed-by=/usr/share/postgresql-common/pgdg/apt.postgresql.org.asc] https://apt.postgresql.org/pub/repos/apt $(. /etc/os-release; echo $VERSION_CODENAME)-pgdg main" \
  > /etc/apt/sources.list.d/pgdg.list
apt update && apt install -y postgresql-17 postgresql-17-pgvector

# Node.js 24 LTS and PM2
curl -fsSL https://deb.nodesource.com/setup_24.x | bash -
apt install -y nodejs
npm install -g pm2

# App user
adduser --disabled-password --gecos "" autoexam
```

Create the database (pick a strong password):

```bash
sudo -u postgres psql -c "CREATE USER autoexam WITH PASSWORD 'CHANGE_ME'"
sudo -u postgres psql -c "CREATE DATABASE autoexam OWNER autoexam"
sudo -u postgres psql -d autoexam -c "CREATE EXTENSION IF NOT EXISTS vector"
```

## 2. Install the app (as `autoexam`)

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh      # provides Python 3.13 on any Debian
git clone https://github.com/kavishkashehan726-sudo/AutoExam.git ~/app
cd ~/app
cp .env.example .env    # then edit: APP_ENV=production, DATABASE_URL, GEMINI_API_KEY, LLM_MODEL, ...

cd backend
uv venv -p 3.13 .venv && uv pip install -p .venv .
.venv/bin/alembic upgrade head

cd ../frontend
npm ci && npm run build

cd ..
pm2 start ecosystem.config.js
pm2 save
pm2 startup systemd     # run the command it prints, as root
```

## 3. Nginx and HTTPS (as root)

`/etc/nginx/sites-available/autoexam`:

```nginx
server {
    server_name example.com;

    location /api/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location / {
        proxy_pass http://127.0.0.1:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

```bash
ln -s /etc/nginx/sites-available/autoexam /etc/nginx/sites-enabled/
nginx -t && systemctl reload nginx
certbot --nginx -d example.com
```

## 4. Release (as `autoexam`)

Releases come from `main`. Tag each release first (`git tag vX.Y.Z && git push --tags`).

```bash
cd ~/app
git fetch --tags && git checkout vX.Y.Z
(cd backend && uv pip install -p .venv . && .venv/bin/alembic upgrade head)
(cd frontend && npm ci && npm run build)
pm2 reload ecosystem.config.js
curl -fsS http://127.0.0.1:8000/api/health
```

## 5. Rollback

```bash
cd ~/app
# If the bad release added migrations, first downgrade to the previous release's revision:
(cd backend && .venv/bin/alembic downgrade <previous_revision>)
git checkout vPREVIOUS
(cd backend && uv pip install -p .venv .)
(cd frontend && npm ci && npm run build)
pm2 reload ecosystem.config.js
```

Back up the database before any release that includes migrations:
`pg_dump -Fc autoexam > ~/backups/autoexam-$(date +%F).dump`.
