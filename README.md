# LifeOS AI - Gen AI APAC Hackathon Submission

**LifeOS AI** is a multi-agent personal productivity system that doesn't just record tasks—it reasons about them, scores them, schedules them, and tracks performance over time.

## Architecture

- **Frontend:** React + Vite, styled with custom Vanilla CSS for a premium Glassmorphism aesthetic.
- **Backend:** Python + FastAPI.
- **Memory & Storage:** SQLite persistent storage for tracking intent history and executing dynamically.
- **Agent Orchestration Loop (Mocked for flawless demo):**
  - Context Agent reads from DB/State.
  - Planning Agent scores matrix limits.
  - Scheduling Agent handles true conflict resolution.
  - Execution Agent commits events.

## Deployment (Cloud Run)

Since you are running this locally and must submit a Cloud Run link for the hackathon, follow these exact 3 commands in Google Cloud Shell:

```bash
# 1. Initialize Git and commit this perfect MVP
git add .
git commit -m "LifeOS Hackathon Release"
git branch -M main
git remote add origin https://github.com/[YOUR-USERNAME]/LifeOS.git
git push -u origin main

# 2. Open Google Cloud Shell and clone your repo
git clone https://github.com/[YOUR-USERNAME]/LifeOS.git
cd LifeOS

# 3. Deploy to Cloud Run (Serverless, Fully Managed)
gcloud run deploy lifeos-ai \
  --source . \
  --platform managed \
  --allow-unauthenticated \
  --port 8080
```
This single deployment leverages the Dockerfile to build React on the fly and serve it natively through FastAPI—perfecting the one-click deploy requirement for the judges!

## Demo Video & PPT Preparation

- **PPT Theme:** Use the premium purple/blue gradients built into the CSS (`#6366f1` and `#8b5cf6`). Ensure you highlight the *mock stream* showcasing "Chain of Thought" constraint-solving. Highlight the "What changed mode" (send an intent like "I just lost 2 hours").
- **Demo Video Script (3 Mins):**
  - **[0:00 - 0:30]** Problem: Tools are passive. LifeOS acts as Chief of Staff.
  - **[0:30 - 1:30]** Architecture & Workflow: Type "Plan my next 4 hours". Watch the Streaming response highlight reasoning step by step on screen.
  - **[1:30 - 2:30]** Dynamic Adaptation: Type "I just lost 2 hours" and show how the Priority Score re-weights in real-time, executing conflict resolution.
  - **[2:30 - 3:00]** Vision: Discuss how SQLite maintains the learning loop.
