// PM2 process file for production on the VPS. See docs/DEPLOY.md.
// APP_DIR defaults to the directory this file lives in.
const path = require("path");

const appDir = process.env.APP_DIR || __dirname;
const backendDir = path.join(appDir, "backend");
const venvBin = path.join(backendDir, ".venv", "bin");

module.exports = {
  apps: [
    {
      name: "frontend",
      cwd: path.join(appDir, "frontend"),
      script: "node_modules/next/dist/bin/next",
      args: "start --port 3000",
      env: { NODE_ENV: "production" },
    },
    {
      name: "backend",
      cwd: backendDir,
      script: path.join(venvBin, "uvicorn"),
      args: "app.main:app --host 127.0.0.1 --port 8000 --workers 2",
      interpreter: "none",
    },
    {
      name: "worker",
      cwd: backendDir,
      script: path.join(venvBin, "python"),
      args: "-m app.worker",
      interpreter: "none",
    },
  ],
};
