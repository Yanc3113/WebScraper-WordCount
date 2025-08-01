# Financial Report Crawler and Keyword Frequency Analysis (Based on CNINFO)

This project is based on [Word_frequency_of_finance](https://github.com/rongzhiy/Word_frequency_of_finance), with major modifications to support large-scale data crawling of financial reports from [CNINFO](http://www.cninfo.com.cn/) (巨潮资讯网), specifically annual reports of publicly listed companies in China.

## 🔍 Project Purpose

The goal of this project is to:

- Crawl **annual reports ** of financial companies listed on CNINFO
- Extract structured metadata such as company code, report title, and PDF URL
- (Planned) Download PDF files and perform **keyword frequency analysis**
- Provide cleaned data in `.csv` format for downstream NLP or econometrics tasks

## Features

- Read company information from `firm_message.csv` (including code, orgId, and short name)
- Query CNINFO’s announcement API to collect PDF links of annual reports
- Automatically filter out irrelevant files (e.g. summaries, explanations, notices)
- Logs errors and missing data in `error.xlsx`
- Outputs structured results into  `ndbg_data.csv`

