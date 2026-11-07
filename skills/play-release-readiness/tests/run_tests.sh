#!/usr/bin/env sh
# Smoke tests for scripts/scan_project.py. Run from anywhere: sh tests/run_tests.sh
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
SCAN="$HERE/../scripts/scan_project.py"
fail=0

check() { # name expected_exit path [grep_pattern]
  name="$1"; want="$2"; path="$3"; pat="${4:-}"
  out="$(python3 "$SCAN" "$path" 2>&1)"; got=$?
  if [ "$got" -ne "$want" ]; then echo "FAIL $name: exit $got, wanted $want"; fail=1; return; fi
  if [ -n "$pat" ] && ! printf '%s' "$out" | grep -q "$pat"; then echo "FAIL $name: missing '$pat'"; fail=1; return; fi
  echo "ok   $name"
}

check "bad project is blocked"          1 "$HERE/fixture_bad"     "targetSdk is 34"
check "bad project: debug signing"      1 "$HERE/fixture_bad"     "signed with the debug key"
check "bad project: com.example"        1 "$HERE/fixture_bad"     "com.example"
check "good project passes"             0 "$HERE/fixture_good"    "targetSdk 36 meets"
check "flutter project scans"           0 "$HERE/fixture_flutter" "AdMob"
exit $fail
