import os, itertools, subprocess

for (dn, sd, files) in itertools.chain(os.walk('backend-tests/'), os.walk('../example-code/')):
  for f in files:
    bn, ext = os.path.splitext(f)
    if ext == '.golden':
      subprocess.call(['diff', '-u', os.path.join(dn, bn + ext), os.path.join(dn, bn + '.golden_py3')])
