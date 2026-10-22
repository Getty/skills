#!/usr/bin/env python3
"""Offline source-register review. Does not fetch law or determine legal effect."""
import argparse
import datetime as dt
import json
from pathlib import Path
import re
import sys

def unique_pairs(items):
    out={}
    for k,v in items:
        if k in out: raise ValueError('duplicate JSON key: '+k)
        out[k]=v
    return out

def date_value(value,label):
    if not isinstance(value,str) or not re.fullmatch(r'\d{4}-\d{2}-\d{2}',value):
        raise ValueError(label+': expected YYYY-MM-DD')
    return dt.date.fromisoformat(value)

def check(register,as_of,horizon):
    if not isinstance(register,dict) or type(register.get('schema_version')) is not int or register.get('schema_version')!=1:
        raise ValueError('expected source-register schema_version 1')
    rows=register.get('sources')
    if not isinstance(rows,list) or not rows: raise ValueError('sources must be a nonempty list')
    findings=[];ids=set();result=[]
    if register.get('adoption_status')!='reviewed':
        findings.append({'id':'REGISTER','kind':'not_adopted','detail':'Register has not been reviewed for the actual platform scope.'})
    for row in rows:
        if not isinstance(row,dict): raise ValueError('source must be an object')
        sid=row.get('id')
        if not isinstance(sid,str) or not sid.strip() or sid in ids: raise ValueError('missing or duplicate source ID')
        ids.add(sid)
        for key in ['title','url','issuer','version','owner']:
            if not isinstance(row.get(key),str) or not row[key].strip(): raise ValueError(sid+': missing '+key)
        status=row.get('status')
        if status not in ['enacted_law','proposal','draft_guidance','final_guidance','standard','case_law','contract']:
            raise ValueError(sid+': invalid source status')
        checked=date_value(row.get('checked_on'),sid+' checked_on')
        review=date_value(row.get('next_review_on'),sid+' next_review_on')
        if review < checked: raise ValueError(sid+': review date precedes check')
        if checked > as_of: findings.append({'id':sid,'kind':'future_check','detail':'Check date is in the future.'})
        if review < as_of: findings.append({'id':sid,'kind':'review_overdue','detail':review.isoformat()})
        elif review <= as_of+dt.timedelta(days=horizon): findings.append({'id':sid,'kind':'review_due_soon','detail':review.isoformat()})
        verification=row.get('verification')
        if verification not in ['full_text','official_reproduction','official_indexed_text','official_summary','limited','unavailable']:
            raise ValueError(sid+': invalid verification mode')
        if verification in ['limited','unavailable']:
            findings.append({'id':sid,'kind':'source_verification_gap','detail':verification})
        reviewed_hash=row.get('reviewed_content_sha256')
        current_hash=row.get('observed_content_sha256')
        for hash_value in [reviewed_hash,current_hash]:
            if hash_value is not None and (not isinstance(hash_value,str) or not re.fullmatch(r'[0-9a-f]{64}',hash_value)):
                raise ValueError(sid+': invalid content hash')
        if reviewed_hash is not None and current_hash is not None and reviewed_hash!=current_hash:
            findings.append({'id':sid,'kind':'content_changed','detail':'Semantic/legal review needed; hash difference alone does not establish a rule change.'})
        events=row.get('events',[])
        if not isinstance(events,list): raise ValueError(sid+': events must be a list')
        for event in events:
            if not isinstance(event,dict): raise ValueError(sid+': invalid event')
            typ=event.get('type')
            if typ not in ['application','transition_deadline','consultation_end','proposed_date','internal_target']:
                raise ValueError(sid+': invalid event type')
            if status in ['proposal','draft_guidance'] and typ in ['application','transition_deadline']:
                raise ValueError(sid+': proposal/draft cannot have an operative application or transition event')
            when=date_value(event.get('on'),sid+' event date')
            if not isinstance(event.get('scope'),str) or not event['scope'].strip(): raise ValueError(sid+': event needs scope')
            if event.get('disposition') not in ['unreviewed','action_planned','no_platform_effect','completed']:
                raise ValueError(sid+': event needs a valid disposition')
            if when <= as_of+dt.timedelta(days=horizon) and event['disposition']=='unreviewed':
                findings.append({'id':sid,'kind':'event_review_required','event_type':typ,'on':when.isoformat(),'scope':event['scope'],'note':'Assess applicability; this is not automatically a deadline for this platform.'})
        result.append({'id':sid,'status':status,'verification':verification,'checked_on':checked.isoformat(),'next_review_on':review.isoformat()})
    return {'result':'review_attention_required' if findings else 'register_checks_passed','as_of':as_of.isoformat(),'sources':result,'findings':findings,'limitations':['No network calls were made. No source content was fetched or interpreted.','No new law, amendment, case or omitted source can be discovered from this register alone.','This is an internal review schedule; dates do not calculate statutory incident clocks or authorise action.']}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('register',type=Path)
    parser.add_argument('--as-of',default=dt.date.today().isoformat())
    parser.add_argument('--horizon-days',type=int,default=30)
    args=parser.parse_args()
    try:
        if args.horizon_days < 0 or args.horizon_days > 3660: raise ValueError('horizon-days must be between 0 and 3660')
        register=json.loads(args.register.read_text(encoding='utf-8'),object_pairs_hook=unique_pairs)
        result=check(register,date_value(args.as_of,'as-of'),args.horizon_days)
        print(json.dumps(result,indent=2))
        return 2 if result['findings'] else 0
    except (OSError,ValueError,TypeError,UnicodeError) as exc:
        print(json.dumps({'result':'invalid_input','error':str(exc)},indent=2));return 1

if __name__=='__main__': sys.exit(main())
