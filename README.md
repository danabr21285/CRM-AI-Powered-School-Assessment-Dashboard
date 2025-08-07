# 🧠 AI-Powered School Assessment Dashboard (CRM Simulation)

An AI-augmented dashboard concept built inside CRM to support admissions recruitment strategy. Using dynamic scoring logic, it evaluates historical applicant funnel data and assigns a school priority badge (Top, Medium, Low) with an auto-generated summary and debug notes.

> ⚠️ *This is a conceptual showcase. No real student data or proprietary schema is included.*

---

#### 🔍 Features
- GPT-generated summary of school funnel performance (Applications, Accepts, Confirms, Inquiries)
- Priority scoring based on defined thresholds
- Automatic badge assignment (e.g., ![Top Priority School](https://img.shields.io/badge/Top%20Priority%20School-forestgreen))
- Toggleable scoring and debug breakdowns
- Supports strategic recruitment planning for admissions officers

---
🧠 *Project Status:* Internal prototype (not deployed). Prompt logic, scoring system, and badge mechanics authored and maintained by Dana Brooks.
---

## ⚙️ Scoring Logic Summary

- Confirms ≥ 10 → +8 pts, 6–8 → +6, 1–5 → +4  
- Accepts ≥ 30 → +4 pts, 10–29 → +3, 1–9 → +2, 0 → −1  
- Applications ≥ 40 → +3, 1–39 → +2, 0 → −1  
- Inquiries ≥ 30 → +3, 1–29 → +2, 0 → −1  
- If visited in past 4 years → +1  
- If in MM, AS, DC, PR, or UK → +2  
- If no org contact exists → −1  

---

## 🏷️ Badge Assignment

| Range | Badge |
|-------|--------|
| 18–28 | ![Top Priority](https://img.shields.io/badge/Top%20Priority%20School-forestgreen) |
| 13–17 | ![Medium Priority](https://img.shields.io/badge/Medium%20Priority%20School-yellow) |
| 0–12  | ![Low Priority](https://img.shields.io/badge/Low%20Priority%20School-red) |

---

## 🛠️ Technologies Used

- CRM Custom Dashboards  
- Prompt Engineering for AI Output  
- Conditional Logic & Query Parameters  
- Badge Rendering via Shields.io  

---

## 👩‍💼 Author

**Dana Brooks**  
📧 danatallent@yahoo.com  
🔗 [LinkedIn](https://linkedin.com/in/dana-tallent-brooks-a15977a0)

---

> “Turning raw funnel data into strategic recruitment intelligence.”
