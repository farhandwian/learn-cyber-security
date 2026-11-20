# Chapter 16: Working with AI as a Security Operator

> **Goal.** After this chapter you can: explain how you would use an AI assistant for day-to-day security work, how you check its answers, and what must never go into an unapproved tool.
>
> **Time:** about 30 minutes. If your day job is mostly operating tools and asking AI, this is the skill an interviewer can probe.

---

## 1. Good uses

| Task | How AI helps | What you still do |
| --- | --- | --- |
| Explain an alert, log line or command | Plain-language summary | Confirm against the raw log and the tool's documentation |
| Explain a CVE | Impact, affected versions, fix | Check NVD or the vendor advisory, and whether you are affected |
| Triage | Suggest what to check next | Decide severity from asset value and exposure |
| Write a query or script | A first draft | Read it, run it on test data first, never run on production blind |
| Draft a report or ticket | Structure and wording | Check every fact and number |

## 2. How to check an AI answer

1. **Source:** can it point to a document, advisory or log line? Open it.
2. **Second opinion:** does the vendor documentation agree?
3. **Test:** run a harmless version in a lab.
4. **Blast radius:** if it is wrong, what breaks? The bigger the effect, the more checking.
5. **Know the limits:** models can invent CVE numbers, commands and package names, and sound confident.

## 3. Rules

- **No secrets or customer data** in tools your company has not approved (keys, tokens, personal data, internal incident details).
- **Treat pasted content as untrusted.** A log, email or web page can hide instructions that steer the assistant (prompt injection); do not let it act without approval.
- **Do not let an agent hold powerful credentials.** Scoped, short-lived, approval for risky actions (see Chapter 11).
- **You own the decision.** "The AI said so" is not an incident-report reason.
- **Stay in scope.** Never point scanning or attack tools, AI-assisted or not, at systems you do not have written permission to test.

## 4. Interview answer

> *"How would you use AI in a security role?"* "To speed up reading and drafting: explaining alerts, summarising CVEs, writing first-draft queries. I verify against the raw data and vendor advisories, test scripts in a lab, keep sensitive data out of unapproved tools, and keep a human decision on anything with real impact."

## Check yourself

1. Name two things you still do yourself when AI explains an alert.
2. What should never go into an unapproved AI tool?
3. How can pasted content attack an AI assistant?

**Answers** *(cover this until you have tried)*

1. Confirm against the raw log or source, and decide severity and action.
2. Secrets, customer or personal data, internal incident details.
3. Hidden instructions in it (prompt injection) can steer the assistant; treat it as untrusted and require approval for actions.

## Summary

- AI drafts and explains; you verify, test and decide.
- Keep sensitive data out of unapproved tools and treat inputs as untrusted.
