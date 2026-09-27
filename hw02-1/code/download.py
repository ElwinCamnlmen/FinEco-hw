"""下载公开快照。分析 Notebook 只读快照，不在重跑时请求网络。"""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from zoneinfo import ZoneInfo
import argparse
import hashlib
import json
import platform
import time
import pandas as pd
import requests
import akshare as ak

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / 'data' / 'raw'
STOCKS = {
    '601166': ('兴业银行', '全国性银行，与区域银行比较，优先使用行情覆盖完整的样本'),
    '601009': ('南京银行', '区域银行，与兴业银行构成同行业比较'),
    '600519': ('贵州茅台', '白酒品牌企业，代表消费品商业模式'),
    '000858': ('五粮液', '白酒品牌企业，与贵州茅台构成同行业比较'),
    '000651': ('格力电器', '耐用消费品制造企业，关注制造业风险'),
    '002032': ('苏泊尔', '厨房电器企业，比较家电行业内部差异'),
    '600886': ('国投电力', '电力运营企业，与华能水电比较，优先使用行情覆盖完整的样本'),
    '600025': ('华能水电', '水电运营企业，与国投电力构成同行业比较'),
    '600276': ('恒瑞医药', '药品研发生产企业，代表医药业务'),
    '600436': ('片仔癀', '中药企业，与其他行业及医药企业比较'),
}

def eastmoney_company_profile(symbol):
    url='https://datacenter-web.eastmoney.com/api/data/v1/get'
    params=dict(reportName='RPT_F10_ORG_BASICINFO',columns='SECUCODE,SECURITY_CODE,SECURITY_NAME_ABBR,EM2016,LISTING_DATE,CSRC_INDUSTRY_NAME',filter=f'(SECURITY_CODE="{symbol}")',pageSize=10,pageNumber=1)
    response=requests.get(url,params=params,timeout=25)
    response.raise_for_status()
    return pd.DataFrame(response.json()['result']['data'])

def get_one(code):
    prefix = 'sh' if code.startswith('6') else 'sz'
    jobs = {
        'raw': (ak.stock_zh_a_hist_tx, dict(symbol=prefix+code, start_date='20201231', end_date='20260916', adjust='', timeout=25)),
        'qfq': (ak.stock_zh_a_hist_tx, dict(symbol=prefix+code, start_date='20201231', end_date='20260916', adjust='qfq', timeout=25)),
        'hfq_factor': (ak.stock_zh_a_daily, dict(symbol=prefix+code, adjust='hfq-factor')),
        'qfq_factor': (ak.stock_zh_a_daily, dict(symbol=prefix+code, adjust='qfq-factor')),
        'value': (ak.stock_value_em, dict(symbol=code)),
        'profile': (eastmoney_company_profile, dict(symbol=code)),
    }
    logs=[]
    for kind,(fn,params) in jobs.items():
        dest=RAW/f'{code}_{kind}.csv'
        if dest.exists():
            print(code,kind,'已有快照，未覆盖',flush=True)
            logs.append(dict(file=dest.name,symbol=code,interface=fn.__name__,parameters=params,rows=len(pd.read_csv(dest)),sha256=hashlib.sha256(dest.read_bytes()).hexdigest(),retrieved_at=datetime.fromtimestamp(dest.stat().st_mtime,ZoneInfo('Asia/Shanghai')).isoformat(),status='ok'))
            continue
        for attempt in range(2):
            try:
                df=fn(**params)
                if df.empty: raise ValueError('空数据')
                df.to_csv(dest,index=False,encoding='utf-8-sig')
                log=dict(file=dest.name, symbol=code, interface=fn.__name__,parameters=params,
                         rows=len(df),sha256=hashlib.sha256(dest.read_bytes()).hexdigest(),
                         retrieved_at=datetime.now(ZoneInfo('Asia/Shanghai')).isoformat(),status='ok')
                print(code,kind,len(df),flush=True)
                break
            except Exception as e:
                log=dict(symbol=code,interface=fn.__name__,parameters=params,status='failed',error=str(e)[:500])
                if attempt==0: time.sleep(1)
        logs.append(log)
    return logs

def main():
    RAW.mkdir(parents=True,exist_ok=True)
    # 给无默认超时的接口设置上限，不更改其返回数据或解析逻辑。
    original=requests.sessions.Session.request
    def bounded(self,*args,**kwargs):
        if kwargs.get('timeout') is None: kwargs['timeout']=25
        return original(self,*args,**kwargs)
    requests.sessions.Session.request=bounded
    logs=[]
    with ThreadPoolExecutor(max_workers=3) as pool:
        for future in as_completed([pool.submit(get_one,c) for c in STOCKS]): logs.extend(future.result())
    calendar=RAW/'calendar_sh000001.csv'
    if not calendar.exists():
        df=ak.stock_zh_a_hist_tx(symbol='sh000001',start_date='20201231',end_date='20260916',adjust='',timeout=25)
        df.to_csv(calendar,index=False,encoding='utf-8-sig')
        logs.append(dict(file=calendar.name,interface='stock_zh_a_hist_tx',parameters=dict(symbol='sh000001',start_date='20201231',end_date='20260916',adjust=''),rows=len(df),sha256=hashlib.sha256(calendar.read_bytes()).hexdigest(),retrieved_at=datetime.now(ZoneInfo('Asia/Shanghai')).isoformat(),status='ok'))
    manifest=ROOT/'data'/'manifest.json'
    prior=json.loads(manifest.read_text()) if manifest.exists() else {}
    prior.update(python=platform.python_version(),akshare=ak.__version__,pandas=pd.__version__,
                 entries=prior.get('entries',[])+logs,
                 source_docs='https://akshare.akfamily.xyz/data/stock/stock.html',
                 requested_start='2021-01-01',requested_end='2026-09-16',baseline='2020-12-31')
    manifest.write_text(json.dumps(prior,ensure_ascii=False,indent=2),encoding='utf-8')

if __name__=='__main__': main()
