# HW02-2 数据获取与本地位置

**目前尚未收到 CSMAR 数据。以下为输入约定，不是数据已经存在的声明。**

数据获取入口：https://data.csmar.com/ 。需要学校有效订阅及授权登录；本地原始文件不上传公开仓库。实际下载日期、文件名、大小、表名、版本和字段说明将在文件到位后登记。

| 标准化文件 | 主要内容 | 相对位置 |
|---|---|---|
| company_year.csv | 历史公司年度身份、上市状态、行业版本 | data/normalized/company_year.csv |
| ownership_year.csv | 历史实际控制人性质与四分类 | data/normalized/ownership_year.csv |
| balance.csv | 2004—2015 年末合并资产负债表字段 | data/normalized/balance.csv |
| income.csv | 2005—2015 年度合并净利润 | data/normalized/income.csv |
| loans.csv | 2005—2015 年末短期及长期银行借款 | data/normalized/loans.csv |
| field_mapping.csv | 原字段、定义、单位、转换和依据文件 | data/normalized/field_mapping.csv |
| source_manifest.json | 来源、筛选条件、规则说明、核验状态和文件指纹 | data/normalized/source_manifest.json |

原始下载 ZIP/CSV/XLSX 和字段说明放 `data/raw/`，按原名保存，不修改。合并后的公司级记录写入 `data/private_derived/`。以上三类目录均由 `.gitignore` 排除。原始数据尚未提供时，不应手工填写 manifest 的“已核验”标志为 true。

字段对应表列：table, raw_field, raw_definition, raw_unit, analysis_variable, conversion, evidence_file。所有金额统一为人民币元，主键为六位证券代码字符串和年份。历史上市状态和行业映射必须从真实年度记录或事件记录构造，不能按今天的名单填充。

完整下载清单在本作业交付目录的 `CSMAR下载清单.md`。授权用户应依据实际 CSMAR 导出版本确认字段定义，然后完成原始到标准化转换；程序 `code/panel_analysis.py` 不替代这一步。

教师受控获取方式：待依据学校和 CSMAR 授权确定。若不能转交数据，提供完整下载条件、字段清单与代码，并明确所需订阅权限，不能以公开链接规避授权。
