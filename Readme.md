## Inspiration
Cloud waste isn’t just a cost problem—it’s a **carbon problem**. While working with GCP environments, we discovered that teams often over-provision resources "just to be safe," leading to **sky-high bills and unnecessary CO₂ emissions**. Worse, optimizing manually is slow and error-prone.  

We built **GreenOps** to automate sustainability. Our vision: **an AI team that continuously audits, forecasts, and optimizes cloud infrastructure**

## What it does

Imagine typing a question like:

> *“How can I reduce cost and emissions in us-central1?”*

GreenOps activates. Here’s what happens:

* The **GreenOps Agent**, our commander-in-chief, kicks into action.
* It routes the query to a sequence of **expert sub-agents**—each trained for a precise role: scout, analyze, recommend, forecast, automate, summarize.
* Within moments, you get:
  * Detailed infrastructure recommendations
  * Forecasted resource + carbon usage
  * Execution plan (if it’s safe)
  * Weekly report in **Google Docs**
  * Downloadable **Presentation deck**

## 🧠 How Each Agent Works (Short & Sweet)

![Agent Flow](Files/AgentFlow.png)

🔎 `optimization_advisor_agent`

The strategist. Executes a three-agent relay:

1. **infra_scout_agent** – Builds & runs BigQuery SQLs for region data
2. **workload_profiler_agent** – Detects idle resources, forecasts emissions with **Climatiq**
3. **recommender_agent** – Crafts a clean recommendation deck

![OptimizationRecommendations](Files/OptimizationRecommendations.png)

---

📈 `forecasting_tool_agent`

Predicts CPU, memory, and carbon emissions. Uses **BigQuery ML models** under the hood and returns formatted results.

![ForecastingAgent](Files/ForecastingAgent.png)

---

⚖️ `impact_calculator_agent`

"What if we moved from E2 to N2 in europe-west1?"
This agent answers using **cost and carbon deltas**.

![ImpactCalculator](Files/ImpactCalculator.png)

---

🛡️ `safe_executor_agent`

Before executing changes, it **forecasts risks**.
If safe, it:

* Stops instance
* Modifies type
* Restarts instance
  Autopilot meets green governance.

---

📊 `summary_generator_agent`

Gathers regional data → Runs forecasts → Gets recommendations
➡ Generates **beautiful Google Docs reports**, including:

* Carbon trend charts
* CPU vs Carbon overlays
* Regional underutilization maps

---

🖼️ `presentation_generator_agent`

Auto-summarizes reports and generates **slide decks** (with visuals!) using `python-pptx`, uploaded to **Google Drive**.

🧠 It’s your executive briefing... automated.

---
### **Auto Generated Content**

**Summary Report**: [Click Here](https://docs.google.com/document/d/1zra8pWlp3OfJKFdDU_06zYSp2Z61vKFMFBuQ9JiDRvk/edit)

**Presentation Deck**: [Click Here](https://drive.usercontent.google.com/download?id=1I0o59TXComCik9pAzzYC602FPoGQvUDL)
(Microsoft Office Format, or ONLYOFFICE.app for MAC)

---

## How we built it
We used the **Google ADK** to build modular, memory-aware agents that pass data between each other like a well-run team. ADK’s `SequentialAgent` and `ToolAgent` features allowed us to manage complex flows with simplicity.

### Technologies Used:

## System Architecture

```mermaid
flowchart LR
    U[User] --> FE[Streamlit Frontend]
    FE -->|Session and run APIs| ADK[Google ADK Agent Service]
    ADK --> ROOT[GreenOps Root Agent<br/>Gemini 2.0 Flash]

    ROOT --> OPT[Optimization Advisor]
    ROOT --> FORE[Forecasting Agent]
    ROOT --> IMP[Impact Calculator]
    ROOT --> EXEC[Safe Executor]
    ROOT --> SUM[Weekly Summary Agent]

    OPT --> SCOUT[Infra Scout]
    SCOUT --> BQ[(BigQuery Metrics)]
    OPT --> PROF[Workload Profiler]
    PROF --> PRICE[Sparecores Pricing]
    PROF --> CLIM[Climatiq Carbon API]
    PROF --> REC[Recommender]

    FORE --> BQML[(BigQuery ML<br/>ARIMA_PLUS)]
    EXEC --> BQML
    EXEC --> GCE[Compute Engine]

    SUM --> CHARTS[Chart Generator]
    CHARTS --> DRIVE[Google Drive]
    SUM --> DOCS[Google Docs]
    SUM --> PPT[Presentation Agent]
    PPT --> DRIVE

    SCHED[Cloud Scheduler] --> SNAPSHOT[Snapshot and Retraining Function]
    SNAPSHOT --> BQ
    SNAPSHOT --> BQML
```

* **Google ADK** – Core multi-agent framework
* **Vertex AI** – Smart LLM-driven decision-making
* **BigQuery** – Data storage + forecasting ML models
* **Climatiq** – Emissions API
* **Cloud Run** – Serverless deployment of backend + agents
* **Streamlit** – Frontend interface
* **Google Docs + Drive APIs** – Auto-generated reports and slides
* **Google Secret Manager** – Secure API key storage

## Challenges we ran into
1. **True multi-agent logic**: Designing agents that not only talk to each other but **understand the sequence and context**.
2. **Forecast before action**: We wanted safety-first automation. That meant building forecast-aware logic for each recommended change.
3. **Dynamic document generation**: Building reports and slides **that don’t look like they came from a bot**.
4. **Chaining LLM outputs**: Ensuring agent-to-agent memory passed correctly, especially in sequential chains with deeply nested outputs.

## Accomplishments that we're proud of
* **Production-ready multi-agent orchestration** (not just a demo)
* **Cross-agent memory**, forecasting, and safe execution logic
* **Climate-conscious AI**—bridging DevOps and sustainability
* **Dynamic document + slide generation** with AI
* **Completely autonomous workflows**, from question → insight → execution

## What we learned

* **Good agents = good architecture**: Clear responsibilities, tight loops, and minimal memory leaks.
* **Forecasts are critical**: We can’t trust AI to make infra changes without good predictive signals.
* **Presentation generation with python-pptx is awesome but tricky**: Especially when blending LLM text and chart data dynamically.
* **ADK unlocks real-world agent coordination**: It's more than a playground—it's a production-ready toolkit.

## What's next for GreenOps
* **FinOps Agent**: Detect budget anomalies and alert teams.
* **Agent Self-Training**: Use past optimization data to refine future decisions.
* 🧠 **New agents**:
  * `security_auditor_agent` → for compliance and exposure risks
  * `cost_anomaly_detector_agent` → alert on sudden usage spikes

---

## Deployment

GreenOps consists of a Streamlit frontend, a Google ADK agent service, BigQuery resources, and a daily snapshot/model-training Cloud Function.

### 1. Prerequisites

- A Google Cloud project with billing enabled
- `gcloud` CLI installed and authenticated
- Docker installed for local builds
- Required APIs enabled:
  - Vertex AI
  - BigQuery
  - Compute Engine
  - Cloud Run
  - Cloud Scheduler
  - Secret Manager
  - Google Docs and Google Drive APIs

```bash
gcloud auth login
gcloud config set project YOUR_PROJECT_ID
gcloud services enable \
  aiplatform.googleapis.com \
  bigquery.googleapis.com \
  compute.googleapis.com \
  run.googleapis.com \
  cloudscheduler.googleapis.com \
  secretmanager.googleapis.com \
  docs.googleapis.com \
  drive.googleapis.com
```

### 2. Configure secrets

Create the Climatiq API key and service-account credentials in Secret Manager:

```bash
echo -n "YOUR_CLIMATIQ_API_KEY" | \
  gcloud secrets create CLIMATIQ_API_KEY --data-file=- \
  --replication-policy="automatic"

gcloud secrets create SERVICE_ACCOUNT_KEY --data-file=- \
  --replication-policy="automatic"
```

Upload the complete JSON service-account key with:

```bash
gcloud secrets versions add SERVICE_ACCOUNT_KEY --data-file=service-account.json
```

Grant the deployed service account access to Secret Manager, BigQuery, Compute Engine, Google Docs, and Google Drive according to the resources it must manage.

### 3. Prepare BigQuery

Create the `gcp_server_details` dataset and tables in BigQuery:

- `server_metrics`
- `server_metrics_timeseries`

The snapshot function in `Cloud Scheduler/Daily_Data_Snapshot_Model_Training/daily_data_snapshot.py` appends metric samples and creates or replaces:

- `server_cpu_forecast_model`
- `server_mem_forecast_model`
- `server_carbon_forecast_model`

Deploy the function:

```bash
cd "Cloud Scheduler/Daily_Data_Snapshot_Model_Training"

gcloud functions deploy greenops-daily-snapshot \
  --gen2 \
  --runtime=python312 \
  --region=us-central1 \
  --source=. \
  --entry-point=run_daily_snapshot_model_retrain \
  --trigger-http \
  --no-allow-unauthenticated
```

Create a Cloud Scheduler job to call the function on a daily schedule:

```bash
gcloud scheduler jobs create http greenops-daily-snapshot \
  --location=us-central1 \
  --schedule="0 2 * * *" \
  --uri="YOUR_FUNCTION_URL" \
  --oidc-service-account-email="YOUR_SERVICE_ACCOUNT"
```

### 4. Deploy the ADK agent service

The agent service is in `greenops_agent/`. Build and deploy it as a Cloud Run container after adding the appropriate container entrypoint for the Google ADK API server.

For example, from a container that serves the package over the ADK API:

```bash
gcloud run deploy greenops-agent-service \
  --source=greenops_agent \
  --region=us-central1 \
  --allow-unauthenticated
```

The deployed service URL must expose:

- `POST /apps/{app_name}/users/{user_id}/sessions/{session_id}`
- `POST /run`

Update `API_BASE_URL` in `Frontend/app.py` with the deployed agent service URL.

### 5. Deploy the Streamlit frontend

Build and deploy the existing frontend container:

```bash
cd Frontend

gcloud run deploy greenops-ui \
  --source=. \
  --region=us-central1 \
  --allow-unauthenticated \
  --port=8080
```

### 6. Verify deployment

1. Open the Cloud Run URL returned for `greenops-ui`.
2. Select **Create session**.
3. Submit a forecast or infrastructure recommendation request.
4. Confirm that the agent service can access BigQuery and Secret Manager.
5. Test the weekly report flow and presentation generation.

### 7. Run locally

Install frontend dependencies and start the UI:

```bash
cd Frontend
python -m pip install -r requirements.txt
python -m streamlit run app.py --server.port=8501
```

Open `http://127.0.0.1:8501`.

Keep VM execution disabled or restricted until the deployed agent service has a service account with only the minimum Compute Engine permissions and the UI has explicit execution approval.

## IN ACTION: [LIVE HERE](https://greenops-ui-273345197968.us-central1.run.app/)


## 🏆 Final Words

GreenOps isn’t just smart—it’s **strategic, sustainable, and scalable**.

With Google ADK as the brain, GCP as the spine, and AI as the soul, we’ve built something **your cloud deserves**.

Let’s make DevOps greener, together. 🌍⚡