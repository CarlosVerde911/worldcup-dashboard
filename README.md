# ⚽ 2026 FIFA World Cup Stats Dashboard

A full-stack Python/Flask app tracking the 2026 FIFA World Cup group standings, match fixtures and top scorers - updates every 3 hours - deployed and hosted on Azure App Service (always on & publicly accessible) with an automated CI/CD pipeline via GitHub Actions.

🔗 **[Live App →](https://worldcup-dashboard-bagphxeefvbtf6db.centralus-01.azurewebsites.net)**

---

## Stack

| Layer | Technology |
|---|---|
| Backend | Python, Flask |
| Hosting | Azure App Service |
| CI/CD | GitHub Actions |
| Deployment | Azure CLI |

---

## How It's Deployed

The app runs on Azure App Service. Deployments are fully automated — every push to `main` triggers a GitHub Actions workflow that builds and ships to production.

Initial setup (resource group, App Service plan, and web app) was done via the Azure Portal. Due to GitHub authorization issues with the portal-based deployment, the initial code deployment was pushed through the Azure CLI:

```bash
az webapp up --name worldcup-dashboard --resource-group rg-worldcup-dashboard --runtime "PYTHON:3.11"
```

Once the app was live, GitHub Actions was then connected through the Azure Portal - Web App Deployment Center to authorize automated deployments, generating the GitHub Actions workflow in `.github/workflows/`.

---

## Run Locally

```bash
git clone https://github.com/CarlosVerde911/world-cup-dashboard.git
cd world-cup-dashboard
pip install -r requirements.txt
flask run
```

---

## What I Learned

- Deploying a Python web app to Azure App Service end-to-end using the CLI
- Diagnosing and resolving deployment failures between portal-based and CLI-based GitHub Actions setup
- Wiring a CI/CD pipeline so that `git push` is the only step needed to ship to production
- Reading Azure deployment logs to trace runtime status and resolve production template errors
- Storing API tokens securely using GitHub Action secrets for the CI/CD pipeline and configuring the database path and API token as environment variables directly in Azure App Service - keeping all credentials out of the source code

---

**Carlos Verde** — [LinkedIn](https://linkedin.com/in/carloseverde) · [GitHub](https://github.com/CarlosVerde911)
