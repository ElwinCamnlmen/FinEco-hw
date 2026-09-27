"""HW02-2 年度面板分析。只接受经字段说明确认的标准化本地输入。

标准化不是下载：须先保留原始 CSMAR 导出及说明，并在 field_mapping.csv
记录原字段、定义、单位和转换。不能用字段名猜银行借款或历史身份。
"""
from pathlib import Path
import hashlib
import json
import numpy as np
import pandas as pd

KEY=['stock_code','year']
YEARS=pd.Index(range(2005,2016),name='year')
OWNERS=['国有','民营','其他','不明']
METRICS={'leverage':'资产负债率','bankloan':'银行借款占比','short_debt':'短期负债占比',
         'ROA':'ROA','ROE':'ROE','Cash_TA':'现金持有'}
SCHEMAS={
    'company_year':KEY+['name','is_a_share','listed_eoy','is_real_estate','industry_code','industry_standard'],
    'ownership_year':KEY+['ownership','controller_nature_raw'],
    'balance':KEY+['total_assets','total_liabilities','current_liabilities','total_equity','cash'],
    'income':KEY+['net_income'],
    'loans':KEY+['short_bank_loan','long_bank_loan'],
}

def require_unique(df,label):
    if df[KEY].isna().any().any(): raise ValueError(f'{label}: 公司/年度主键缺失')
    dup=df.duplicated(KEY,keep=False)
    if dup.any(): raise ValueError(f'{label}: {int(dup.sum())} 行主键重复，须回查报表口径/版本，不能取第一行')

def check_numeric(df,columns,label):
    for c in columns:
        if c in KEY: continue
        raw=df[c]
        converted=pd.to_numeric(raw,errors='coerce')
        if (raw.notna() & converted.isna()).any(): raise ValueError(f'{label}.{c}: 非数字内容，须核对单位/表头')
        if np.isinf(converted).any(): raise ValueError(f'{label}.{c}: 无穷值')
        df[c]=converted

def load_inputs(folder):
    folder=Path(folder)
    needed=[folder/f'{name}.csv' for name in SCHEMAS]+[folder/'source_manifest.json',folder/'field_mapping.csv']
    missing=[str(p.name) for p in needed if not p.is_file()]
    if missing: raise FileNotFoundError('待准备经核验的 CSMAR 标准表：'+', '.join(missing))
    manifest=json.loads((folder/'source_manifest.json').read_text(encoding='utf-8'))
    for flag in ['historical_industry_verified','historical_controller_verified','year_end_listing_verified',
                 'annual_consolidated_verified','bank_loan_definitions_verified','includes_delisted_firms']:
        if manifest.get(flag) is not True: raise ValueError(f'来源核验未完成：{flag}')
    if manifest.get('amount_unit')!='CNY': raise ValueError('须按字段说明将金额统一为人民币元')
    for key in ['retrieved_at','industry_mapping','ownership_mapping','report_version_rule','source_tables','files']:
        if not manifest.get(key): raise ValueError(f'缺少来源说明：{key}')
    fieldmap=pd.read_csv(folder/'field_mapping.csv')
    required={'table','raw_field','raw_definition','raw_unit','analysis_variable','conversion','evidence_file'}
    if not required.issubset(fieldmap.columns): raise ValueError('字段对应表列不完整')
    if fieldmap[list(required)].isna().any().any(): raise ValueError('字段定义/单位/证据说明不能留空')
    tables={}
    for name,fields in SCHEMAS.items():
        path=folder/f'{name}.csv'
        expected=manifest['files'].get(path.name,{}).get('sha256')
        if not expected or hashlib.sha256(path.read_bytes()).hexdigest()!=expected:
            raise ValueError(f'{name}: 来源清单中的 SHA256 缺失或不符')
        df=pd.read_csv(path,dtype={'stock_code':str})
        missing_cols=set(fields)-set(df.columns)
        if missing_cols: raise ValueError(f'{name} 缺字段：{sorted(missing_cols)}')
        df=df[fields].copy()
        if not df.stock_code.str.fullmatch(r'\d{6}').fillna(False).all(): raise ValueError(f'{name}: 证券代码必须为六位字符串')
        yr=pd.to_numeric(df.year,errors='coerce')
        if yr.isna().any() or not (yr%1==0).all(): raise ValueError(f'{name}: 年度不合法')
        df['year']=yr.astype(int)
        if not df.year.between(2004,2015).all(): raise ValueError(f'{name}: 研究及分母支持期以外记录应在标准化阶段另存')
        require_unique(df,name)
        if name in ['balance','income','loans']: check_numeric(df,fields,name)
        if name=='company_year':
            for flag in ['is_a_share','listed_eoy','is_real_estate']:
                if df[flag].isna().any() or not df[flag].isin([0,1,True,False]).all():
                    raise ValueError(f'{flag} 必须由历史信息明确判定为 0 或 1')
        if name=='ownership_year' and not df.ownership.isin(OWNERS).all():
            raise ValueError('产权必须分为国有/民营/其他/不明；不能把其他产权改成民营')
        tables[name]=df
    if 2004 not in set(tables['balance'].year): raise ValueError('缺少 2004 年末分母支持数据')
    return tables,manifest,fieldmap

def build_panel(tables):
    """先建历史样本，再左连接；财务缺失不改变公司数量。"""
    for name,df in tables.items(): require_unique(df,name)
    stages=[]
    def record(label,df): stages.append({'阶段':label,'公司数':df.stock_code.nunique(),'企业年度数':len(df)})
    for name,df in tables.items(): record('标准化输入：'+name,df)
    universe=tables['company_year']
    sample=universe.loc[universe.year.between(2005,2015)&universe.is_a_share.eq(1)&universe.listed_eoy.eq(1)&universe.is_real_estate.eq(1)].copy()
    record('当年年末房地产A股样本',sample)
    if sample.empty: raise ValueError('样本为空，请核对历史身份筛选')
    if not set(YEARS).issubset(set(sample.year)): raise ValueError('2005—2015 年并非每年都有样本，先核对下载范围')
    unmatched=[]
    for name in ['ownership_year','balance','income','loans']:
        sample=sample.merge(tables[name],on=KEY,how='left',validate='one_to_one',indicator=f'_merge_{name}')
        unmatched.append(sample.groupby('year')[f'_merge_{name}'].apply(lambda x:int(x.eq('left_only').sum())).rename(name))
        record('左连接：'+name,sample)
    sample['ownership']=sample.ownership.fillna('不明')
    # 让上年记录的年份加一后合并：缺 2006 不会把 2005 当 2007 的上期。
    prior=tables['balance'][KEY+['total_assets','total_equity']].copy()
    prior['year']=prior['year']+1
    prior=prior.rename(columns={'total_assets':'assets_lag','total_equity':'equity_lag'})
    sample=sample.merge(prior,on=KEY,how='left',validate='one_to_one',indicator='_merge_prior')
    record('连接相邻上年末分母',sample)
    return sample,pd.DataFrame(stages),pd.concat(unmatched,axis=1).reindex(YEARS,fill_value=0)

def make_metrics(panel):
    """主分析不缩尾。无效分母只影响对应指标，不删除公司年度。"""
    p=panel.copy()
    ta=p.total_assets.where(p.total_assets.gt(0))
    tl=p.total_liabilities.where(p.total_liabilities.gt(0))
    p['avg_assets']=(p.total_assets+p.assets_lag)/2
    p['avg_equity']=(p.total_equity+p.equity_lag)/2
    avgta=p.avg_assets.where(p.total_assets.gt(0)&p.assets_lag.gt(0))
    avgeq=p.avg_equity.where(p.total_equity.gt(0)&p.equity_lag.gt(0))
    p['leverage']=p.total_liabilities.where(p.total_liabilities.ge(0))/ta
    # 加总保留任一借款字段的缺失，不把空白认作无银行借款。
    bank=p[['short_bank_loan','long_bank_loan']].sum(axis=1,min_count=2)
    bank=bank.where(p.short_bank_loan.ge(0)&p.long_bank_loan.ge(0))
    p['bankloan']=bank/tl
    p['short_debt']=p.current_liabilities.where(p.current_liabilities.ge(0))/tl
    p['ROA']=p.net_income/avgta
    p['ROE']=p.net_income/avgeq
    p['Cash_TA']=p.cash.where(p.cash.ge(0))/ta
    # ROE敏感性：允许符号分母，但排除零和缺失，不把正比率等同盈利。
    p['ROE_signed']=p.net_income/p.avg_equity.where(p.avg_equity.ne(0))
    flags={
      '总资产非正':p.total_assets.le(0),'总负债非正':p.total_liabilities.le(0),
      '任一相邻年权益非正':p.total_equity.le(0)|p.equity_lag.le(0),
      '上年资产缺失':p.assets_lag.isna(),'上年权益缺失':p.equity_lag.isna(),
      '任一银行借款字段缺失':p[['short_bank_loan','long_bank_loan']].isna().any(axis=1),
      '流动负债大于总负债':p.current_liabilities.gt(p.total_liabilities),
      '银行借款大于总负债':bank.gt(p.total_liabilities),
      '货币资金大于总资产':p.cash.gt(p.total_assets),
      '资产不等于负债加权益':(p.total_assets-p.total_liabilities-p.total_equity).abs().gt(p.total_assets.abs()*0.001+1),
    }
    audit=pd.DataFrame({k:v.groupby(p.year).sum().astype(int) for k,v in flags.items()}).reindex(YEARS)
    for k,v in flags.items(): p['flag_'+k]=v
    audit_missing=p.groupby('year')[list(METRICS)].apply(lambda d:d.isna().sum()).reindex(YEARS)
    return p,audit,audit_missing

def summarize(p):
    counts=p.groupby(['year','ownership']).stock_code.nunique().unstack(fill_value=0).reindex(index=YEARS,columns=OWNERS,fill_value=0)
    counts['总数']=counts[OWNERS].sum(axis=1)
    counts['国有占比']=counts['国有']/counts['总数']; counts['民营占比']=counts['民营']/counts['总数']
    counts['其他或不明占比']=(counts['其他']+counts['不明'])/counts['总数']
    long=p.melt(id_vars=KEY+['ownership'],value_vars=list(METRICS),var_name='metric',value_name='value')
    overall=long.groupby(['year','metric']).value.agg(['count','mean','median']).reset_index()
    groups=long.groupby(['year','ownership','metric']).value.agg(['count','mean','median']).reset_index()
    # 保留缺席产权组的零有效样本量，而不是让该行静默消失。
    fullidx=pd.MultiIndex.from_product([YEARS,OWNERS,list(METRICS)],names=['year','ownership','metric'])
    groups=groups.set_index(['year','ownership','metric']).reindex(fullidx).reset_index()
    groups['count']=groups['count'].fillna(0).astype(int)
    return counts,overall,groups,long

def sensitivity(p):
    # 每年每指标 1%/99% 缩尾只作为对照；不足 20 个有效观测不缩尾。
    rows=[]
    for year,g in p.groupby('year'):
        for key in METRICS:
            v=g[key].dropna(); n=len(v)
            low,high=v.quantile([.01,.99]) if n>=20 else (-np.inf,np.inf)
            clipped=v.clip(low,high)
            rows.append({'year':year,'metric':key,'n':n,'raw_mean':v.mean(),'winsor_mean':clipped.mean(),
                         'raw_median':v.median(),'winsor_median':clipped.median(),
                         'affected':int(v.ne(clipped).sum())})
    roe=p.groupby('year')[['ROE','ROE_signed']].agg(['count','mean','median'])
    # 进入/退出/产权变更诊断：退出是从房地产样本退出，不直接等同退市。
    movement=[]
    for year in range(2006,2016):
        before=p[p.year.eq(year-1)].set_index('stock_code'); now=p[p.year.eq(year)].set_index('stock_code')
        common=before.index.intersection(now.index)
        changes=(before.loc[common,'ownership']!=now.loc[common,'ownership']).sum()
        movement.append({'year':year,'进入本年房地产样本':len(now.index.difference(before.index)),
                         '退出本年房地产样本':len(before.index.difference(now.index)),
                         '连续两年在样本的公司':len(common),'产权分类变化':int(changes)})
    return pd.DataFrame(rows),roe,pd.DataFrame(movement)
