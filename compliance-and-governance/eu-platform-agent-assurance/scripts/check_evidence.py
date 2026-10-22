#!/usr/bin/env python3
"""Check a declared evidence package, not legal compliance. Standard library only."""
import argparse
import datetime as dt
import hashlib
import json
from pathlib import Path
import re
import sys

class Invalid(ValueError):
    pass

def pairs(items):
    out = {}
    for key, value in items:
        if key in out:
            raise Invalid('duplicate JSON key: ' + key)
        out[key] = value
    return out

def read_json(path):
    with path.open(encoding='utf-8') as stream:
        value = json.load(stream, object_pairs_hook=pairs)
    if not isinstance(value, dict):
        raise Invalid(str(path) + ': expected JSON object')
    return value

def nonempty(value):
    return isinstance(value, str) and bool(value.strip())

def day(value, label):
    if not isinstance(value, str) or not re.fullmatch(r'\d{4}-\d{2}-\d{2}', value):
        raise Invalid(label + ': expected YYYY-MM-DD')
    try:
        return dt.date.fromisoformat(value)
    except ValueError as exc:
        raise Invalid(label + ': invalid date') from exc

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def local_file(base, name):
    if not nonempty(name) or Path(name).is_absolute():
        raise Invalid('evidence path must be a nonempty relative path')
    target = (base / name).resolve()
    if not target.is_relative_to(base) or not target.is_file():
        raise Invalid('evidence path missing or outside evidence root: ' + name)
    return target

def validate(scope, report, scope_hash, base, as_of, release, environment, max_bytes):
    errors = []
    def require(ok, message):
        if not ok:
            errors.append(message)
    require(type(scope.get('schema_version')) is int and scope.get('schema_version') == 1, 'scope.schema_version must be 1')
    require(type(report.get('schema_version')) is int and report.get('schema_version') == 1, 'report.schema_version must be 1')
    for label, obj in [('scope',scope), ('report',report)]:
        for key in ['profile_id','profile_revision','release_id','environment']:
            require(nonempty(obj.get(key)), label + '.' + key + ' is required')
        require(obj.get('release_id') == release, label + ': release mismatch')
        require(obj.get('environment') == environment, label + ': environment mismatch')
    for key in ['profile_id','profile_revision']:
        require(scope.get(key) == report.get(key), key + ': scope/report mismatch')
    require(report.get('scope_sha256') == scope_hash, 'scope hash mismatch')
    approval = scope.get('review', {})
    require(isinstance(approval,dict), 'scope.review must be an object')
    if isinstance(approval,dict):
        require(approval.get('status') == 'reviewed', 'scope is not marked reviewed')
        require(nonempty(approval.get('reviewer')), 'scope reviewer missing')
        try:
            reviewed=day(approval.get('reviewed_on'),'scope reviewed_on')
            due=day(approval.get('review_due'),'scope review_due')
            require(reviewed <= as_of <= due, 'scope review is future-dated or expired')
            require(reviewed <= due, 'scope review dates inverted')
        except Invalid as exc:
            errors.append(str(exc))
    expected=scope.get('required_control_ids')
    require(isinstance(expected,list) and bool(expected), 'required_control_ids must be a nonempty list')
    if not isinstance(expected,list):
        expected=[]
    require(all(nonempty(x) for x in expected), 'required control IDs must be nonempty strings')
    expected_valid=[x for x in expected if nonempty(x)]
    require(len(expected_valid)==len(set(expected_valid)), 'duplicate required control IDs')
    controls=report.get('controls')
    require(isinstance(controls,list) and bool(controls), 'controls must be a nonempty list')
    if not isinstance(controls,list):
        controls=[]
    found={}
    for index,c in enumerate(controls):
        if not isinstance(c,dict):
            errors.append('control '+str(index)+': expected object'); continue
        cid=c.get('id')
        if not nonempty(cid):
            errors.append('control '+str(index)+': missing id'); continue
        if cid in found:
            errors.append(cid+': duplicate control'); continue
        found[cid]=c
    require(set(found)==set(expected_valid), 'declared controls differ from reviewed required_control_ids')
    applicable_count=0
    for cid,c in found.items():
        prefix=cid+': '
        for key in ['owner','applicability_reason','reviewer']:
            require(nonempty(c.get(key)),prefix+key+' missing')
        require(c.get('normative_type') in ['binding_law','contract','internal_policy','guidance','standard'],prefix+'invalid normative_type')
        try:
            review_day=day(c.get('reviewed_on'),prefix+'reviewed_on')
            require(review_day <= as_of,prefix+'control review is in the future')
        except Invalid as exc:
            errors.append(str(exc)); review_day=as_of
        source=c.get('source')
        if not isinstance(source,dict):
            errors.append(prefix+'source must be an object'); source={}
        for key in ['reference','provision','version']:
            require(nonempty(source.get(key)),prefix+'source.'+key+' missing')
        try:
            checked=day(source.get('verified_on'),prefix+'source.verified_on')
            due=day(source.get('review_due'),prefix+'source.review_due')
            require(checked <= as_of <= due,prefix+'source is future-dated or stale')
            require(checked <= due,prefix+'source dates inverted')
            require(checked <= review_day,prefix+'source verification postdates control review')
        except Invalid as exc:
            errors.append(str(exc))
        applicability=c.get('applicability')
        if applicability == 'not_applicable':
            require(c.get('status')=='not_applicable',prefix+'excluded control has inconsistent status')
            require(nonempty(c.get('exclusion_evidence_ref')),prefix+'exclusion evidence reference missing')
        elif applicability != 'applicable':
            errors.append(prefix+'unresolved applicability'); continue
        else:
            applicable_count+=1
            require(c.get('status')=='verified',prefix+'implementation is not verified')
        evidence=c.get('evidence')
        if not isinstance(evidence,list) or not evidence:
            errors.append(prefix+'no evidence supplied'); continue
        for index,item in enumerate(evidence):
            label=prefix+'evidence['+str(index)+'] '
            if not isinstance(item,dict):
                errors.append(label+'expected object'); continue
            require(item.get('outcome')=='pass',label+'outcome is not pass')
            require(item.get('release_id')==release,label+'release mismatch')
            require(item.get('environment')==environment,label+'environment mismatch')
            require(nonempty(item.get('method')),label+'method missing')
            try:
                observed=day(item.get('observed_on'),label+'observed_on')
                expiry=day(item.get('expires_on'),label+'expires_on')
                require(observed <= as_of <= expiry,label+'evidence is future-dated or expired')
                require(observed <= review_day,label+'evidence postdates control review')
            except Invalid as exc:
                errors.append(str(exc))
            sha=item.get('sha256')
            require(isinstance(sha,str) and re.fullmatch(r'[0-9a-f]{64}',sha) is not None,label+'invalid sha256')
            try:
                path=local_file(base,item.get('path'))
                require(path.stat().st_size <= max_bytes,label+'evidence file exceeds configured size limit')
                if path.stat().st_size <= max_bytes:
                    require(digest(path)==sha,label+'content hash mismatch')
            except (Invalid,OSError) as exc:
                errors.append(label+str(exc))
    require(applicable_count > 0,'all controls excluded; no positive evidence package')
    return errors

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--scope',required=True,type=Path,help='Reviewed applicability selection chosen outside this report')
    p.add_argument('--report',required=True,type=Path)
    p.add_argument('--evidence-root',required=True,type=Path)
    p.add_argument('--release',required=True)
    p.add_argument('--environment',required=True)
    p.add_argument('--as-of',default=dt.date.today().isoformat())
    p.add_argument('--max-file-bytes',type=int,default=16*1024*1024)
    args=p.parse_args()
    try:
        if args.max_file_bytes <= 0:
            raise Invalid('max-file-bytes must be positive')
        base=args.evidence_root.resolve()
        if not base.is_dir():
            raise Invalid('evidence root is not a directory')
        scope=read_json(args.scope)
        report=read_json(args.report)
        errors=validate(scope,report,digest(args.scope),base,day(args.as_of,'as-of'),args.release,args.environment,args.max_file_bytes)
        print(json.dumps({'result':'evidence_consistency_failed' if errors else 'evidence_consistency_passed','as_of':args.as_of,'release_id':args.release,'environment':args.environment,'errors':errors,'limitations':['Does not determine legal applicability, authenticate reviewers or assess whether evidence contents prove a control.','Reviewed scope, checker and CI invocation require an independent trust boundary.','Passing does not authorise release or certify compliance.']},indent=2))
        return 2 if errors else 0
    except (Invalid,OSError,json.JSONDecodeError,TypeError,UnicodeError) as exc:
        print(json.dumps({'result':'invalid_input','error':str(exc)},indent=2))
        return 1

if __name__=='__main__':
    sys.exit(main())
