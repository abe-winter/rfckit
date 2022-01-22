#!/usr/bin/env python3
import argparse
import yaml
from spec import Spec
from build_diag import render_spec

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--spec', default='./samples/oauth.yml', help="path to protocol spec file")
    p.add_argument('--out')
    args = p.parse_args()

    spec = Spec.parse_obj(yaml.load(open(args.spec), Loader=yaml.Loader))
    body = '\n'.join(render_spec(spec).render(lines=['<!DOCTYPE html>']))
    if args.out:
        open(args.out, 'w').write(body)
    else:
        print(body)

if __name__ == '__main__': main()
