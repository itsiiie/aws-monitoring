# 📊 AWS Free Tier Usage Monitor

A Python-based tool that monitors your **AWS Free Tier** usage and cost, alerts you when thresholds are exceeded, and generates reports — all automated with **GitHub Actions**.

---

## 🚀 Features

- **Service Cost Tracking**: Uses AWS Cost Explorer to retrieve up-to-date cost data
- **Usage Monitoring**:

  - 🖥️ EC2 running hours
  - 📦 S3 storage usage
  - 🧠 Lambda compute time
  - 🗃️ RDS instance hours

- **Alerts**:

  - Define your own thresholds
  - Sends alerts to **Discord** using a webhook

- **Reporting**:

  - Saves reports as **JSON** and **CSV**
  - Easy to integrate into dashboards or future analysis

- **Automation**:

  - Scheduled to run **every hour** via GitHub Actions
  - Also runs **on every push** or manually from GitHub UI

---

## 🧱 Project Structure

```bash
aws-ftum/
├── main.py                     # Main script
├── requirements.txt            # Python dependencies
├── .env.example                # Sample environment variables
├── reports/                    # Auto-generated usage reports
├── services/
│   ├── cost_usage.py           # AWS Cost Explorer functions
│   ├── usage_tracker.py        # S3, EC2, Lambda, RDS usage
├── utils/
│   ├── formatter.py            # Report formatting
│   ├── report_generator.py     # Save JSON/CSV reports
│   ├── alert.py                # Load/check alert thresholds
│   ├── discord_notify.py       # Send alerts to Discord
└── .github/
    └── workflows/
        └── monitor.yml         # GitHub Actions workflow
```

---

## ⚙️ Setup Instructions

### 1. 🔁 Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/aws-ftum.git
cd aws-ftum
```

### 2. 🐍 Create Virtual Environment (optional but recommended)

```bash
python3 -m venv myenv
source myenv/bin/activate
```

### 3. 📦 Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. 🔑 Configure `.env` File

Create a copy from the template:

```bash
cp .env.example .env
```

Edit `.env` and add your credentials:

```env
AWS_ACCESS_KEY_ID=your_aws_key
AWS_SECRET_ACCESS_KEY=your_aws_secret
AWS_REGION=us-east-1
ALERT_THRESHOLD=0.01
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/...
```

> ⚠️ Never commit your real `.env` file to version control!

### 5. ▶️ Run the Monitor Script Locally

```bash
python main.py
```

Reports will be saved to the `reports/` directory.

---

## 🤖 GitHub Actions Workflow

### ✅ Triggers:

- Every hour: `cron: "0 * * * *"`
- On every push to main
- Manually via GitHub UI

### 🔐 Secrets to Add in GitHub:

In your GitHub repository, go to **Settings > Secrets > Actions**, and add:

- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `DISCORD_WEBHOOK_URL`

### 📝 Workflow File: `.github/workflows/monitor.yml`

```yaml
name: AWS Free Tier Monitor

on:
  push:
  schedule:
    - cron: "0 * * * *"
  workflow_dispatch:

jobs:
  run-monitor:
    runs-on: ubuntu-latest

    env:
      AWS_REGION: us-east-1
      ALERT_THRESHOLD: 0.01
      AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
      AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
      DISCORD_WEBHOOK_URL: ${{ secrets.DISCORD_WEBHOOK_URL }}

    steps:
      - name: 📥 Checkout code
        uses: actions/checkout@v3

      - name: 🐍 Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: "3.11"

      - name: 📦 Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: 🧪 Run monitor script
        run: python main.py

      - name: 💾 Upload usage reports
        uses: actions/upload-artifact@v4
        with:
          name: usage-reports
          path: reports/
```

---

## 📬 Discord Alerts

When a threshold is breached, the monitor sends a message to your Discord channel:

```
⚠️ AWS Free Tier Alert(s) Triggered:

S3 usage exceeded threshold!
RDS usage exceeded threshold!

Current Cost: $0.07
```

---

## 📁 Reports

Each run will save two files to `reports/`:

- `YYYY-MM-DD_usage_report.json`
- `YYYY-MM-DD_usage_report.csv`

These files contain:

```json
{
  "EC2": "30 / 750 hrs",
  "S3": "4.2 / 5 GB",
  "Lambda": "20000 / 400000 GB-sec",
  "RDS": "100 / 750 hrs"
}
```

---

## 📌 Roadmap / Future Improvements

- [ ] Add email alerting support
- [ ] Build a Streamlit dashboard for historical trends
- [ ] Support more AWS services (CloudFront, DynamoDB, etc.)
- [ ] Export charts/images for reports

---

## 📜 License

MIT License. See `LICENSE` file for details.

---

## 🙌 Author

**Shashank**
🎓 4th Year B.Tech CSE | Cloud & DevOps Enthusiast
🔗 [LinkedIn](https://linkedin.com/in/YOUR_PROFILE) • [GitHub](https://github.com/YOUR_USERNAME)

---

> ⭐ If you like this project, give it a star!
