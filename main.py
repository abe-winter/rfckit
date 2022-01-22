#!/usr/bin/env python3
import argparse
import yaml
from spec import Spec

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--spec', default='./samples/oauth.yml', help="path to protocol spec file")
    args = p.parse_args()

    spec = Spec.parse_obj(yaml.load(open(args.spec), Loader=yaml.Loader))
    print(spec)

if __name__ == '__main__': main()
