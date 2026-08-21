# PipeFish Labs — Make.com, Slack, Obsidian & Marketing Suite Integration Guide

This document provides step-by-step instructions to connect your PipeFish Labs website (`https://pipefishlabs.io`) with **Make.com**, **Slack**, **Obsidian**, **Supabase / PostgreSQL**, **Google Analytics 4**, **Google Tag Manager**, **Meta Ads**, and **LinkedIn Ads**.

---

## 1. Make.com Webhook & Multi-Tool Automation Hub

Your contact form (`/book-a-demo-contact/`) is already programmed to capture form data, UTM parameters (`utm_source`, `utm_campaign`, etc.), URL referrers, and timestamps, and post them to a Make.com Webhook.

### Step 1.1: Create a Make.com Webhook
1. Log into your [Make.com](https://www.make.com) account and create a new Scenario.
2. Add the **Webhooks** module → select **Custom Webhook**.
3. Click **Add** and copy the generated Webhook URL (e.g., `https://hook.us1.make.com/xxxxxxxxx`).

### Step 1.2: Connect Webhook to Your Site
You can activate your webhook on your site in 2 ways:
- **Option A (HTML Global Variable)**: Place `<script>window.MAKE_WEBHOOK_URL = "https://hook.us1.make.com/xxxxxxxxx";</script>` in your page head.
- **Option B (Cloudflare Worker Environment Variable)**: Proxy requests or configure header redirects.

---

### Step 1.3: Add Automated Actions in Make.com

#### 💬 A. Slack Notifications
- Add **Slack** → **Create a Message** module.
- Channel: `#inbound-leads`
- Message text:
  ```text
  🚨 NEW PIPEFISH LABS STRATEGY SESSION REQUEST
  • Name: {{1.name}}
  • Email: {{1.email}}
  • Phone: {{1.phone}}
  • Company: {{1.company}}
  • Size: {{1.size}}
  • Industry: {{1.discipline}}
  • Challenge: {{1.pain}}
  • Budget: {{1.budget}}
  • Source: {{1.utm.utm_source}} / {{1.utm.utm_campaign}}
  ```

#### 🐘 B. Supabase / PostgreSQL Database Insertion
- Add **Supabase** → **Insert a Row** module.
- Table: `leads`
- Map fields: `email`, `name`, `company`, `size`, `pain`, `submitted_at`.

#### 📝 C. Obsidian Markdown Note Generation
- Add **Google Drive** / **Dropbox** → **Upload a File** module (or use the Obsidian Local REST API plugin).
- Destination: `/Vault/Leads/2026-08-21-{{1.company}}.md`
- File Content:
  ```markdown
  # Lead Record: {{1.company}}
  - **Contact**: {{1.name}} ({{1.email}} | {{1.phone}})
  - **Date**: {{1.timestamp}}
  - **Discipline**: {{1.discipline}}
  - **Team Size**: {{1.size}}
  - **Operational Pain**: {{1.pain}}
  ```

#### 💼 D. Server-Side Ads Retargeting (Meta CAPI & LinkedIn Conversions API)
- Add **Meta Conversions API** → **Send Event** (`Lead`).
- Add **LinkedIn Conversions API** → **Send Conversion Event**.

---

## 2. Google Analytics 4 (GA4) & Google Tag Manager (GTM) Setup

### Step 2.1: Add GTM Container Snippet
Paste your Google Tag Manager script snippet into the `<head>` of your pages:
```html
<!-- Google Tag Manager -->
<script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
})(window,document,'script','dataLayer','GTM-XXXXXXX');</script>
<!-- End Google Tag Manager -->
```

### Step 2.2: Automated Conversion Events
Your contact form pushes custom events to GTM `dataLayer` automatically:
- Event Name: `generate_lead`
- Data Variables: `lead_type`, `company_size`

---

## 3. Fast Revenue Generation Execution Blueprint

1. **Cold Email / LinkedIn Outbound Sequence**:
   - Target COOs, VPs of Operations, and CTOs at 50-500 person companies.
   - Core Offer: *"Free 90-Minute Operational Audit & Documented Multi-Agent Automation Roadmap."*
2. **Agency White-Labeling & Reseller Program**:
   - Recruit IT MSPs and consultancy partners offering 20% recurring referral fees or 35% white-label margins (`/affiliates-corporate-partnerships/`).
3. **Interactive Demo Video Content**:
   - Share 90-second screen recordings of the **Live Interactive Demo** (`/#demo`) on LinkedIn & X to showcase real-time 8-agent state handoffs.
