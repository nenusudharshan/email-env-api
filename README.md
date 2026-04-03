# 📧 Email Triage OpenEnv Environment

## 🚀 Overview

This project implements an **OpenEnv-style reinforcement learning environment** for email triage.

An agent receives emails and must decide:

* 📂 Category → spam / important / normal
* ⚡ Action → reply / ignore / schedule
* 🔥 Priority → low / medium / high

The environment evaluates the agent based on correctness and difficulty.

---

## 🧠 Environment Design

### 🔹 Difficulty Levels

* **Easy** → Only category matters
* **Medium** → Category + Action
* **Hard** → Category + Action + Priority

---

## 🔁 API Endpoints

### POST `/reset`

Returns a new email task

### POST `/step`

Takes agent action and returns reward

### GET `/state`

Returns current environment state

### GET `/tasks`

Lists all available tasks

### GET `/baseline`

Runs rule-based baseline agent

---

## 🤖 Agents

### 1. AI Agent

Uses OpenAI to classify emails

### 2. Rule-Based Agent (Fallback)

Keyword-based classification:

* "free", "win" → spam
* "meeting" → important
* "payment" → important

---

## 🐳 Running with Docker

```bash
docker build -t email-env .
docker run -p 8000:8000 email-env
```

---

## 🧪 Example Flow

```bash
POST /reset
→ get email

POST /step
→ send action

→ receive reward
```

---

## 🏆 Key Features

* RL-style environment
* Difficulty-based scoring
* API-first design
* Dockerized deployment
* AI + rule-based agent

---

## 📌 Future Improvements

* Add more complex tasks
* Multi-step episodes
* Better reward shaping
* UI dashboard

---

## 👨‍💻 Author

Sudharshan Reddy
