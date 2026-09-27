# HW02-1 冻结数据

所有 CSV 为公开接口快照，以 UTF-8 编码保存；代码通过相对路径读取。金额单位为元。完整接口参数、下载时间和 SHA256 见 `manifest.json`。分析不会实时取数。

| 文件 | 大小（字节） | 接口 / 用途 | 相对位置 |
|---|---:|---|---|
| 000651_hfq_factor.csv | 1262 | stock_zh_a_daily | `data/raw/000651_hfq_factor.csv` |
| 000651_profile.csv | 208 | eastmoney_company_profile | `data/raw/000651_profile.csv` |
| 000651_qfq.csv | 95024 | stock_zh_a_hist_tx | `data/raw/000651_qfq.csv` |
| 000651_qfq_factor.csv | 1241 | stock_zh_a_daily | `data/raw/000651_qfq_factor.csv` |
| 000651_raw.csv | 94610 | stock_zh_a_hist_tx | `data/raw/000651_raw.csv` |
| 000651_value.csv | 324206 | stock_value_em | `data/raw/000651_value.csv` |
| 000858_hfq_factor.csv | 1002 | stock_zh_a_daily | `data/raw/000858_hfq_factor.csv` |
| 000858_profile.csv | 202 | eastmoney_company_profile | `data/raw/000858_profile.csv` |
| 000858_qfq.csv | 99479 | stock_zh_a_hist_tx | `data/raw/000858_qfq.csv` |
| 000858_qfq_factor.csv | 984 | stock_zh_a_daily | `data/raw/000858_qfq_factor.csv` |
| 000858_raw.csv | 98323 | stock_zh_a_hist_tx | `data/raw/000858_raw.csv` |
| 000858_value.csv | 329380 | stock_value_em | `data/raw/000858_value.csv` |
| 002032_hfq_factor.csv | 862 | stock_zh_a_daily | `data/raw/002032_hfq_factor.csv` |
| 002032_profile.csv | 199 | eastmoney_company_profile | `data/raw/002032_profile.csv` |
| 002032_qfq.csv | 92285 | stock_zh_a_hist_tx | `data/raw/002032_qfq.csv` |
| 002032_qfq_factor.csv | 861 | stock_zh_a_daily | `data/raw/002032_qfq_factor.csv` |
| 002032_raw.csv | 91691 | stock_zh_a_hist_tx | `data/raw/002032_raw.csv` |
| 002032_value.csv | 318597 | stock_value_em | `data/raw/002032_value.csv` |
| 002142_profile.csv | 199 | eastmoney_company_profile | `data/raw/002142_profile.csv` |
| 002142_qfq.csv | 96045 | stock_zh_a_hist_tx | `data/raw/002142_qfq.csv` |
| 002142_raw.csv | 95905 | stock_zh_a_hist_tx | `data/raw/002142_raw.csv` |
| 002142_value.csv | 322602 | stock_value_em | `data/raw/002142_value.csv` |
| 600025_hfq_factor.csv | 349 | stock_zh_a_daily | `data/raw/600025_hfq_factor.csv` |
| 600025_profile.csv | 244 | eastmoney_company_profile | `data/raw/600025_profile.csv` |
| 600025_qfq.csv | 89187 | stock_zh_a_hist_tx | `data/raw/600025_qfq.csv` |
| 600025_qfq_factor.csv | 349 | stock_zh_a_daily | `data/raw/600025_qfq_factor.csv` |
| 600025_raw.csv | 89345 | stock_zh_a_hist_tx | `data/raw/600025_raw.csv` |
| 600025_value.csv | 321441 | stock_value_em | `data/raw/600025_value.csv` |
| 600276_hfq_factor.csv | 935 | stock_zh_a_daily | `data/raw/600276_hfq_factor.csv` |
| 600276_profile.csv | 199 | eastmoney_company_profile | `data/raw/600276_profile.csv` |
| 600276_qfq.csv | 97474 | stock_zh_a_hist_tx | `data/raw/600276_qfq.csv` |
| 600276_qfq_factor.csv | 932 | stock_zh_a_daily | `data/raw/600276_qfq_factor.csv` |
| 600276_raw.csv | 97200 | stock_zh_a_hist_tx | `data/raw/600276_raw.csv` |
| 600276_value.csv | 330999 | stock_value_em | `data/raw/600276_value.csv` |
| 600436_hfq_factor.csv | 889 | stock_zh_a_daily | `data/raw/600436_hfq_factor.csv` |
| 600436_profile.csv | 196 | eastmoney_company_profile | `data/raw/600436_profile.csv` |
| 600436_qfq.csv | 99985 | stock_zh_a_hist_tx | `data/raw/600436_qfq.csv` |
| 600436_qfq_factor.csv | 889 | stock_zh_a_daily | `data/raw/600436_qfq_factor.csv` |
| 600436_raw.csv | 98298 | stock_zh_a_hist_tx | `data/raw/600436_raw.csv` |
| 600436_value.csv | 326097 | stock_value_em | `data/raw/600436_value.csv` |
| 600519_hfq_factor.csv | 1009 | stock_zh_a_daily | `data/raw/600519_hfq_factor.csv` |
| 600519_profile.csv | 205 | eastmoney_company_profile | `data/raw/600519_profile.csv` |
| 600519_qfq.csv | 105777 | stock_zh_a_hist_tx | `data/raw/600519_qfq.csv` |
| 600519_qfq_factor.csv | 1009 | stock_zh_a_daily | `data/raw/600519_qfq_factor.csv` |
| 600519_raw.csv | 103080 | stock_zh_a_hist_tx | `data/raw/600519_raw.csv` |
| 600519_value.csv | 334524 | stock_value_em | `data/raw/600519_value.csv` |
| 600886_hfq_factor.csv | 1003 | stock_zh_a_daily | `data/raw/600886_hfq_factor.csv` |
| 600886_profile.csv | 244 | eastmoney_company_profile | `data/raw/600886_profile.csv` |
| 600886_qfq.csv | 93102 | stock_zh_a_hist_tx | `data/raw/600886_qfq.csv` |
| 600886_qfq_factor.csv | 985 | stock_zh_a_daily | `data/raw/600886_qfq_factor.csv` |
| 600886_raw.csv | 94281 | stock_zh_a_hist_tx | `data/raw/600886_raw.csv` |
| 600886_value.csv | 321857 | stock_value_em | `data/raw/600886_value.csv` |
| 600900_profile.csv | 244 | eastmoney_company_profile | `data/raw/600900_profile.csv` |
| 600900_qfq.csv | 95462 | stock_zh_a_hist_tx | `data/raw/600900_qfq.csv` |
| 600900_raw.csv | 95260 | stock_zh_a_hist_tx | `data/raw/600900_raw.csv` |
| 600900_value.csv | 329657 | stock_value_em | `data/raw/600900_value.csv` |
| 601009_hfq_factor.csv | 739 | stock_zh_a_daily | `data/raw/601009_hfq_factor.csv` |
| 601009_profile.csv | 199 | eastmoney_company_profile | `data/raw/601009_profile.csv` |
| 601009_qfq.csv | 91788 | stock_zh_a_hist_tx | `data/raw/601009_qfq.csv` |
| 601009_qfq_factor.csv | 739 | stock_zh_a_daily | `data/raw/601009_qfq_factor.csv` |
| 601009_raw.csv | 93640 | stock_zh_a_hist_tx | `data/raw/601009_raw.csv` |
| 601009_value.csv | 318218 | stock_value_em | `data/raw/601009_value.csv` |
| 601166_hfq_factor.csv | 739 | stock_zh_a_daily | `data/raw/601166_hfq_factor.csv` |
| 601166_profile.csv | 199 | eastmoney_company_profile | `data/raw/601166_profile.csv` |
| 601166_qfq.csv | 97113 | stock_zh_a_hist_tx | `data/raw/601166_qfq.csv` |
| 601166_qfq_factor.csv | 739 | stock_zh_a_daily | `data/raw/601166_qfq_factor.csv` |
| 601166_raw.csv | 96905 | stock_zh_a_hist_tx | `data/raw/601166_raw.csv` |
| 601166_value.csv | 327810 | stock_value_em | `data/raw/601166_value.csv` |
| calendar_sh000001.csv | 111817 | stock_zh_a_hist_tx | `data/raw/calendar_sh000001.csv` |

获取来源：[AKShare 文档](https://akshare.akfamily.xyz/data/stock/stock.html)、[腾讯证券](https://gu.qq.com/)、[新浪财经](https://finance.sina.com.cn/)、[东方财富](https://data.eastmoney.com/)。下载程序位于 `code/download.py`。本题不使用 CSMAR 受限数据。