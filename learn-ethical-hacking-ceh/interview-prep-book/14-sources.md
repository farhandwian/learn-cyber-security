# Sources and Further Reading

> **A note on accuracy.** Incident figures (people affected, cards stolen, dates) are *reported estimates* and differ between sources; the book rounds them and says "about" or "roughly". Security guidance also changes (the OWASP list was updated in 2025). Check the primary sources below before quoting a number in an interview, and say "reported" if you are unsure.

## Standards and reference

- **OWASP Top 10:2025**: https://top10.owasp.org/2025 (the category list, the 2025 changes, and the new A03 and A10).
- **OWASP Cheat Sheet Series**: https://cheatsheetseries.owasp.org (practical prevention guidance for SQL injection, XSS, CSRF, password storage, authentication and more).
- **MITRE CWE**: https://cwe.mitre.org (weakness categories such as CWE-89 and CWE-79).
- **NVD (National Vulnerability Database)**: https://nvd.nist.gov (CVE records and CVSS scores; used in Lab 5).
- **FIRST CVSS calculator and specification**: https://www.first.org/cvss
- **CISA Known Exploited Vulnerabilities catalog**: https://www.cisa.gov/known-exploited-vulnerabilities-catalog
- **NIST SP 800-61** (Computer Security Incident Handling Guide): the incident-response lifecycle that Chapter 9 summarizes.
- **Nmap reference guide**: https://nmap.org/book/man.html, and the practice target https://scanme.nmap.org

## Practice platforms (all free to start)

- **PortSwigger Web Security Academy**: https://portswigger.net/web-security
- **TryHackMe**: https://tryhackme.com
- **OWASP Juice Shop**: https://owasp.org/www-project-juice-shop/
- **Wireshark documentation**: https://www.wireshark.org/docs/

## Incident case studies used in this book

- **Equifax (2017):** an unpatched Apache Struts flaw (CVE-2017-5638). https://www.esecurityplanet.com/networks/unpatched-open-source-software-flaw-blamed-for-massive-equifax-breach/ and https://www.bankinfosecurity.com/equifax-us-breach-victim-tally-stands-at-1466-million-a-10985 (the affected count was revised several times; most reports say roughly 145-148 million).
- **Capital One (2019):** reported SSRF against a misconfigured web application firewall to reach the cloud metadata service. https://krebsonsecurity.com/2019/08/what-we-can-learn-from-the-capital-one-hack/ and https://www.techtarget.com/cybersecurity/news/252467901/Capital-One-hack-highlights-SSRF-concerns-for-AWS (the exact technical path is partly reconstructed from filings).
- **SolarWinds (2020):** a compromised build process delivered tampered Orion updates. SolarWinds' FY2020 annual report: https://www.sec.gov/Archives/edgar/data/1739942/000173994221000043/swi-20201231.htm (the "fewer than 18,000 customers" figure is an upper estimate of who could have installed an affected version).
- **LinkedIn (2012, leaked 2016):** unsalted SHA-1 password hashes. https://techcrunch.com/2016/05/18/117-million-linkedin-emails-and-passwords-from-a-2012-hack-just-got-posted-online
- **Heartland Payment Systems:** SQL injection leading to about 130 million card numbers. https://www.csoonline.com/article/2124279/u-s--says-sql-injection-caused-major-breaches.html and https://www.darkreading.com/attacks-breaches/hacker-indicted-for-stealing-130-million-credit-cards (sources differ on the exact dates, so the book gives none).
- **WannaCry (2017):** patch MS17-010 released 14 March 2017; outbreak from 12 May 2017. https://www.csoonline.com/article/563017/wannacry-explained-a-perfect-ransomware-storm.html
- **Target (2013):** stolen vendor credentials and weak segmentation; about 40 million cards. https://www.csoonline.com/article/2601021/11-steps-attackers-took-to-crack-target.html (how the vendor's credentials were obtained is reported differently by different sources).

**Not re-verified for this edition:** the Mirai/Dyn outage (2016) and the Log4Shell CVSS score of 10.0 come from general knowledge; Lab 5 has you confirm the second one on the NVD yourself, and a quick search will confirm the first.

## Your Indonesian book

*Ethical Hacking dari Nol: Buku Ajar* is a full CEH-oriented course. Use it as a deeper companion for any chapter above (the chapter map is in [00-start-here.md](00-start-here.md)); skip its Linux, Bash, Python and exam-simulation chapters for this one-month goal.
