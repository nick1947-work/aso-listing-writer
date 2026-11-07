#!/usr/bin/env python3
"""Static pre-submission scan for Android and Flutter projects.

Usage:
    python scan_project.py <project-root> [--json] [--min-target 36]

What it does (static checks only, no build, no network):
  * target/compile/min SDK, applicationId, versionCode
  * manifest permissions, debuggable, cleartext traffic, exported components
  * SDKs that imply data collection (for Data safety / privacy policy)
  * leftovers: test ad IDs, debug signing in release, committed keystores,
    possible hard-coded secrets, plain http:// URLs
  * native code present (16 KB page-size reminder)

What it cannot do: see the merged manifest of library permissions, run the app,
or check anything in Play Console. Those appear under "needs a human".

Exit code: 1 if any FAIL, otherwise 0. WARN items are review prompts.
Rule values below were last verified 2026-11-07; see references/current-requirements.md.
"""
import argparse
import json
import os
import re
import sys
import xml.etree.ElementTree as ET

DEFAULT_MIN_TARGET = 36  # Play requirement for new apps/updates since 2026-08-31

ANDROID = "{http://schemas.android.com/apk/res/android}"
TOOLS = "{http://schemas.android.com/tools}"

SKIP_DIRS = {
    "build", ".git", ".gradle", "node_modules", ".idea", "intermediates",
    ".dart_tool", "Pods", ".pub-cache", "outputs", "generated",
}
SKIP_MANIFEST_SETS = ("/src/debug/", "/src/androidTest/", "/src/test/")
CODE_EXT = (".kt", ".java", ".dart", ".xml", ".gradle", ".kts", ".properties", ".json")
MAX_FILE_BYTES = 600_000

SENSITIVE_PERMS = {
    "android.permission.MANAGE_EXTERNAL_STORAGE": (
        "All files access needs a permission declaration and a core use (file manager, backup, antivirus).",
        "Use Storage Access Framework / MediaStore, or complete the declaration if it is core.",
    ),
    "android.permission.READ_MEDIA_IMAGES": (
        "Photo/video permissions must be core functionality.",
        "Use the system photo picker (no permission needed) unless broad access is core.",
    ),
    "android.permission.READ_MEDIA_VIDEO": (
        "Photo/video permissions must be core functionality.",
        "Use the system photo picker unless broad access is core.",
    ),
    "android.permission.READ_SMS": ("SMS access is restricted to default handlers and narrow exceptions.", "Use SMS Retriever / User Consent APIs."),
    "android.permission.RECEIVE_SMS": ("SMS access is restricted.", "Use SMS Retriever / User Consent APIs."),
    "android.permission.SEND_SMS": ("SMS access is restricted.", "Open the SMS app with an intent instead."),
    "android.permission.READ_CALL_LOG": ("Call log access is restricted.", "Remove unless you are the default handler."),
    "android.permission.ACCESS_BACKGROUND_LOCATION": (
        "Background location needs a declaration, in-app disclosure and a demo video.",
        "Use foreground location or the Geofence API.",
    ),
    "android.permission.ACCESS_FINE_LOCATION": (
        "Precise location must be justified; request the least precision needed (location button recommended).",
        "Use coarse location or the location button if precision is not essential.",
    ),
    "android.permission.READ_CONTACTS": (
        "Broad contacts access is governed by the Contacts permissions policy (Oct 2026).",
        "Use the Android Contact Picker, or submit the Play Developer Declaration.",
    ),
    "android.permission.QUERY_ALL_PACKAGES": ("Needs a declaration and a core use.", "Use <queries> for specific packages."),
    "android.permission.REQUEST_INSTALL_PACKAGES": ("Restricted: installing other apps.", "Remove unless core."),
    "android.permission.SYSTEM_ALERT_WINDOW": ("Overlay permission is often rejected.", "Use notifications or in-app UI."),
    "android.permission.USE_FULL_SCREEN_INTENT": ("Allowed only for calls/alarms.", "Use a normal notification."),
    "android.permission.SCHEDULE_EXACT_ALARM": ("Exact alarms are for alarm/calendar-type apps.", "Use WorkManager or inexact alarms."),
    "android.permission.USE_EXACT_ALARM": ("Exact alarms are for alarm/calendar-type apps.", "Use WorkManager or inexact alarms."),
}
AD_ID_PERM = "com.google.android.gms.permission.AD_ID"

# (regex over dependency text, label, data summary, flags)
GRADLE_SDKS = [
    (r"firebase-analytics|firebase-bom|play-services-measurement", "Firebase Analytics", "app interactions, device/other IDs, diagnostics", {"analytics"}),
    (r"firebase-crashlytics", "Firebase Crashlytics", "crash logs, diagnostics, installation IDs", {"crash"}),
    (r"firebase-auth|play-services-auth|androidx\.credentials|firebase-ui-auth", "Sign-in (Firebase Auth / Google Sign-In / Credential Manager)", "email, name, user IDs", {"accounts"}),
    (r"firebase-messaging|onesignal", "Push notifications (FCM/OneSignal)", "push token, device ID", {"push"}),
    (r"play-services-ads|com\.google\.android\.ump|user-messaging-platform", "AdMob / Google ads", "advertising ID, IP-derived location, ad interactions", {"ads"}),
    (r"com\.facebook\.android|facebook-android-sdk", "Meta (Facebook) SDK", "device IDs, events", {"ads", "analytics"}),
    (r"com\.android\.billingclient|billing-ktx", "Google Play Billing", "purchase history", {"billing"}),
    (r"play-services-location", "Google location services", "precise/approximate location", {"location"}),
    (r"com\.google\.mlkit", "ML Kit", "on-device unless a cloud API is used", set()),
    (r"generativeai|firebase-ai|firebase-vertexai|openai|anthropic", "Generative AI API", "prompts/content sent to a third-party AI provider", {"ai"}),
    (r"sentry", "Sentry", "crash logs, device info", {"crash"}),
    (r"mixpanel|amplitude|posthog", "Product analytics", "events, IDs", {"analytics"}),
    (r"appsflyer|com\.adjust|branch\.io|io\.branch", "Attribution SDK", "attribution, device IDs", {"analytics", "ads"}),
    (r"com\.razorpay|stripe|payu|cashfree", "Payment SDK", "payment details handled by provider", {"payments"}),
    (r"androidx\.room|androidx\.datastore", "Room / DataStore (local storage)", "stays on device unless synced", set()),
]
FLUTTER_SDKS = {
    "firebase_analytics": GRADLE_SDKS[0],
    "firebase_crashlytics": GRADLE_SDKS[1],
    "firebase_auth": GRADLE_SDKS[2],
    "google_sign_in": GRADLE_SDKS[2],
    "firebase_messaging": GRADLE_SDKS[3],
    "onesignal_flutter": GRADLE_SDKS[3],
    "google_mobile_ads": GRADLE_SDKS[4],
    "in_app_purchase": GRADLE_SDKS[6],
    "geolocator": GRADLE_SDKS[7],
    "location": GRADLE_SDKS[7],
    "google_mlkit_text_recognition": GRADLE_SDKS[8],
    "google_generative_ai": GRADLE_SDKS[9],
    "sentry_flutter": GRADLE_SDKS[10],
    "mixpanel_flutter": GRADLE_SDKS[11],
    "appsflyer_sdk": GRADLE_SDKS[12],
    "razorpay_flutter": GRADLE_SDKS[13],
    "flutter_stripe": GRADLE_SDKS[13],
    "isar": GRADLE_SDKS[14],
    "hive": GRADLE_SDKS[14],
}
FLUTTER_PERM_HINTS = {
    "permission_handler": "permission_handler present: check which permissions you request at runtime and declare only those in the manifest.",
    "camera": "camera plugin: disclose camera use; say whether media leaves the device.",
    "image_picker": "image_picker: uses the photo picker on modern Android; avoid adding broad media permissions.",
}

TEST_AD_ID = "ca-app-pub-3940256099942544"
SECRET_PATTERNS = [
    (re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"), "private key"),
    (re.compile(r"\bAKIA[0-9A-Z]{16}\b"), "AWS access key id"),
    (re.compile(r"\bsk-[A-Za-z0-9]{24,}\b"), "API secret key (sk-...)"),
    (re.compile(r"(?i)(?:api[_-]?key|secret|token)\s*[:=]\s*[\"'][A-Za-z0-9_\-]{24,}[\"']"), "hard-coded key/secret/token"),
]
HTTP_IGNORE = ("localhost", "127.0.0.1", "10.0.2.2", "schemas.android.com", "www.w3.org", "xmlns", "apache.org",
               "www.apache.org", "android.com", "example.com", "example.org", "schemas.microsoft.com", "maven", "dl.google.com")


class Report:
    def __init__(self):
        self.findings = []
        self.sdks = {}
        self.permissions = set()
        self.facts = {}

    def add(self, level, code, message, where="", fix=""):
        key = (level, code, message, where)
        if any((f["level"], f["code"], f["message"], f["where"]) == key for f in self.findings):
            return
        self.findings.append({"level": level, "code": code, "message": message, "where": where, "fix": fix})


def rel(path, root):
    return os.path.relpath(path, root)


def walk(root):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for name in filenames:
            yield os.path.join(dirpath, name)


def read(path):
    try:
        if os.path.getsize(path) > MAX_FILE_BYTES:
            return ""
        with open(path, encoding="utf-8", errors="ignore") as f:
            return f.read()
    except OSError:
        return ""


def scan_manifest(path, root, rep):
    where = rel(path, root)
    try:
        tree = ET.parse(path)
    except ET.ParseError as exc:
        rep.add("UNKNOWN", "manifest-parse", f"Could not parse manifest: {exc}", where)
        return
    r = tree.getroot()
    for tag in ("uses-permission", "uses-permission-sdk-23"):
        for el in r.findall(tag):
            name = el.get(ANDROID + "name")
            if not name or el.get(TOOLS + "node") == "remove":
                continue
            rep.permissions.add(name)
    app = r.find("application")
    if app is None:
        return
    if app.get(ANDROID + "debuggable", "").lower() == "true":
        rep.add("FAIL", "debuggable", "Manifest sets android:debuggable=\"true\".", where,
                "Remove it; release builds must not be debuggable.")
    if app.get(ANDROID + "usesCleartextTraffic", "").lower() == "true":
        rep.add("WARN", "cleartext", "Cleartext (HTTP) traffic is allowed.", where,
                "Use HTTPS only; scope any exception with a network security config.")
    rep.facts["allowBackup"] = app.get(ANDROID + "allowBackup", "(default true)")
    for comp in ("activity", "activity-alias", "service", "receiver", "provider"):
        for el in app.findall(comp):
            if el.find("intent-filter") is not None and el.get(ANDROID + "exported") is None:
                rep.add("WARN", "exported-missing",
                        f"<{comp} {el.get(ANDROID + 'name', '?')}> has an intent-filter but no android:exported.", where,
                        "Apps targeting Android 12+ must set android:exported explicitly.")
    for meta in app.findall("meta-data"):
        name = meta.get(ANDROID + "name", "")
        val = meta.get(ANDROID + "value", "")
        if name == "com.google.android.gms.ads.APPLICATION_ID":
            rep.facts["admob_app_id_present"] = True
            if TEST_AD_ID in val:
                rep.add("FAIL", "test-admob-app-id", "Manifest uses the AdMob TEST application ID.", where,
                        "Use your real AdMob app ID in release builds (keep test IDs for debug only).")


def int_or_none(s):
    try:
        return int(s)
    except (TypeError, ValueError):
        return None


def find_sdk_values(text, key):
    """Return (numeric value or None, raw string or None) for targetSdk/compileSdk/minSdk."""
    m = re.search(rf"\b{key}\s*\{{\s*version\s*=\s*release\((\d+)", text)
    if m:
        return int(m.group(1)), m.group(1)
    for pat in (rf"\b{key}(?:Version)?\s*=?\s*(\d+)\b", rf"\b{key}(?:Version)?\s*=?\s*([A-Za-z_][\w.]*)"):
        m = re.search(pat, text)
        if m:
            return int_or_none(m.group(1)), m.group(1)
    return None, None


def scan_gradle(path, root, rep, min_target):
    text = read(path)
    where = rel(path, root)
    is_app = bool(re.search(r"applicationId|com\.android\.application", text))
    if is_app:
        rep.facts["app_module"] = where
        t_num, t_raw = find_sdk_values(text, "targetSdk")
        c_num, c_raw = find_sdk_values(text, "compileSdk")
        mn_num, mn_raw = find_sdk_values(text, "minSdk")
        rep.facts.update({"targetSdk": t_raw, "compileSdk": c_raw, "minSdk": mn_raw})
        if t_num is not None:
            if t_num < min_target:
                rep.add("FAIL", "target-sdk", f"targetSdk is {t_num}; Play requires {min_target}+ for new apps and updates.", where,
                        f"Set targetSdk to {min_target} (or higher), then test behaviour changes.")
            else:
                rep.add("PASS", "target-sdk", f"targetSdk {t_num} meets the {min_target} requirement.", where)
        elif t_raw:
            rep.add("UNKNOWN", "target-sdk", f"targetSdk is set indirectly ({t_raw}); could not resolve the value.", where,
                    f"Confirm it resolves to {min_target}+ (for Flutter, check the Flutter SDK version or set targetSdk explicitly).")
        else:
            rep.add("UNKNOWN", "target-sdk", "No targetSdk found in the app module.", where,
                    f"Set targetSdk explicitly to {min_target}+.")
        if c_num is not None and t_num is not None and c_num < t_num:
            rep.add("WARN", "compile-sdk", f"compileSdk ({c_num}) is lower than targetSdk ({t_num}).", where,
                    "Set compileSdk to at least the target.")
        m = re.search(r"applicationId\s*=?\s*[\"']([^\"']+)[\"']", text)
        if m:
            rep.facts["applicationId"] = m.group(1)
            if m.group(1).startswith("com.example"):
                rep.add("FAIL", "package-name", f"applicationId '{m.group(1)}' starts with com.example, which Play rejects.", where,
                        "Choose a permanent package name you own, e.g. com.yourbrand.app, before the first upload.")
            else:
                rep.add("PASS", "package-name", f"applicationId is {m.group(1)}.", where)
        m = re.search(r"versionCode\s*=?\s*(\d+)", text)
        if m:
            rep.facts["versionCode"] = int(m.group(1))
        # release block checks
        for blk in re.finditer(r"\brelease\b\s*\{", text):
            seg = text[blk.end(): blk.end() + 900]
            if re.search(r"signingConfig\s*=?\s*signingConfigs\.(?:getByName\([\"']debug[\"']\)|debug\b)", seg):
                rep.add("FAIL", "debug-signing", "Release build type is signed with the debug key.", where,
                        "Sign release with your upload key; enable Play App Signing.")
            if re.search(r"\b(?:isDebuggable|debuggable)\s*=?\s*true", seg):
                rep.add("FAIL", "release-debuggable", "Release build type is debuggable.", where,
                        "Set debuggable false for release.")
        if re.search(r"\b(?:isMinifyEnabled|minifyEnabled)\s*=?\s*true", text):
            rep.add("PASS", "minify", "R8/minify is enabled in at least one build type.", where)
        else:
            rep.add("WARN", "minify", "No build type enables R8/minify (smaller, harder-to-reverse builds).", where,
                    "Enable minifyEnabled/isMinifyEnabled and shrinkResources for release; test thoroughly.")
    if re.search(r"externalNativeBuild|\bndk\s*\{|cmake|ndkBuild", text):
        rep.facts["native"] = True
    scan_deps(text, where, rep)


def scan_deps(text, where, rep):
    for pattern, label, data, flags in GRADLE_SDKS:
        if re.search(pattern, text, re.IGNORECASE):
            rep.sdks.setdefault(label, {"data": data, "flags": sorted(flags), "found_in": where})


def scan_pubspec(path, root, rep):
    text = read(path)
    where = rel(path, root)
    rep.facts["framework"] = "flutter"
    names = set(re.findall(r"^\s{2}([a-z0-9_]+):", text, re.MULTILINE))
    for pkg, entry in FLUTTER_SDKS.items():
        if pkg in names:
            _, label, data, flags = entry
            rep.sdks.setdefault(label, {"data": data, "flags": sorted(flags), "found_in": f"{where} ({pkg})"})
    for pkg, hint in FLUTTER_PERM_HINTS.items():
        if pkg in names:
            rep.add("INFO", f"flutter-{pkg}", hint, where)


def scan_source(path, root, rep):
    text = read(path)
    if not text:
        return
    where = rel(path, root)
    if TEST_AD_ID in text and not path.endswith("AndroidManifest.xml"):
        rep.add("WARN", "test-ad-id", "AdMob test ID found in source.", where,
                "Make sure release builds use your real ad unit IDs (test IDs only in debug).")
    for i, line in enumerate(text.splitlines(), 1):
        for rx, label in SECRET_PATTERNS:
            if rx.search(line):
                rep.add("WARN", "secret", f"Possible {label} in source (value not shown).", f"{where}:{i}",
                        "Move secrets out of the app; anything in an APK can be extracted. Rotate if it was real.")
                break
    if path.endswith((".kt", ".java", ".dart")):
        urls = []
        for m in re.finditer(r"http://[^\s\"')<>]+", text):
            u = m.group(0)
            if not any(ig in u for ig in HTTP_IGNORE):
                urls.append(u)
        if urls:
            rep.add("WARN", "http-url", f"Plain http:// URL(s) in code, e.g. {urls[0][:70]}", where,
                    "Use https:// (Android blocks cleartext by default for modern targets).")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("root")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--min-target", type=int, default=DEFAULT_MIN_TARGET)
    args = ap.parse_args()
    root = os.path.abspath(args.root)
    if not os.path.isdir(root):
        print(f"Not a directory: {root}", file=sys.stderr)
        sys.exit(2)

    rep = Report()
    manifests = gradles = 0
    has_so = False
    for path in walk(root):
        low = path.replace("\\", "/")
        name = os.path.basename(path)
        if name == "AndroidManifest.xml" and not any(s in low for s in SKIP_MANIFEST_SETS):
            manifests += 1
            scan_manifest(path, root, rep)
        elif name in ("build.gradle", "build.gradle.kts"):
            gradles += 1
            scan_gradle(path, root, rep, args.min_target)
        elif name == "libs.versions.toml" or name == "versions.toml":
            scan_deps(read(path), rel(path, root), rep)
        elif name == "pubspec.yaml":
            scan_pubspec(path, root, rep)
        if name.endswith((".jks", ".keystore")) or name in ("keystore.properties", "key.properties"):
            rep.add("WARN", "keystore-in-repo", "Signing key or key properties file is in the project tree.", rel(path, root),
                    "Keep keystores and passwords out of version control; add them to .gitignore. Rotate if already pushed.")
        if name.endswith(".so"):
            has_so = True
        if name.endswith(CODE_EXT) and not name.endswith(".json"):
            scan_source(path, root, rep)

    if manifests == 0:
        rep.add("UNKNOWN", "no-manifest", "No AndroidManifest.xml found. Is this the project root?", root)
    if has_so or rep.facts.get("native"):
        rep.add("INFO", "native-code", "Native code detected.", "",
                "Apps with native libraries that target Android 15+ must support 16 KB page sizes. Build with a recent NDK/AGP and verify alignment of .so files.")

    perms = rep.permissions
    for p in sorted(perms):
        if p in SENSITIVE_PERMS:
            why, fix = SENSITIVE_PERMS[p]
            rep.add("WARN", "sensitive-permission", f"{p.split('.')[-1]}: {why}", "AndroidManifest", fix)
    flags = {f for s in rep.sdks.values() for f in s["flags"]}
    if ("ads" in flags or "analytics" in flags) and AD_ID_PERM not in perms:
        rep.add("WARN", "ad-id", "Ad/analytics SDK detected but AD_ID permission is not declared.", "AndroidManifest",
                "If the app targets Android 13+ and uses the advertising ID, declare com.google.android.gms.permission.AD_ID (or confirm the SDK adds it).")
    if AD_ID_PERM in perms and not ({"ads", "analytics"} & flags):
        rep.add("INFO", "ad-id-unused", "AD_ID permission is declared but no ad/analytics SDK was detected.", "AndroidManifest",
                "Remove it if the advertising ID is unused.")
    if "ads" in flags:
        rep.add("WARN", "ads-declaration", "Ads detected.", "Play Console",
                "Declare ads in App content, disclose advertising data in Data safety and the privacy policy; use test ads only in debug.")
    if "accounts" in flags:
        rep.add("WARN", "account-deletion", "Sign-in SDK detected: the app likely lets users create accounts.", "Play Console / app",
                "Provide in-app account deletion and a public web deletion page; add the URL in Data safety.")
    if "ai" in flags:
        rep.add("WARN", "ai-user-data", "Generative AI API detected.", "app / policy",
                "Disclose what user content is sent to the AI provider, get consent where needed, and cover it in the privacy policy (Play User Data policy applies to third-party AI).")
    if "billing" in flags:
        rep.add("INFO", "billing-library", "Play Billing detected.", "",
                "Confirm you use a supported Billing Library version (Play enforces a minimum).")

    human = [
        "Privacy policy URL is public, not a PDF, and matches the app",
        "Data safety form matches the SDKs above",
        "Content rating and Target audience declared truthfully",
        "App access instructions / demo credentials (if any login)",
        "Permissions from libraries (check the merged manifest)",
        "Closed-test status (12 testers / 14 days) for new personal accounts",
        "Android developer verification: apps registered in Play Console",
        "Store listing is accurate (screenshots, title, description)",
    ]

    order = {"FAIL": 0, "WARN": 1, "UNKNOWN": 2, "INFO": 3, "PASS": 4}
    rep.findings.sort(key=lambda f: order[f["level"]])
    counts = {k: sum(1 for f in rep.findings if f["level"] == k) for k in order}

    if args.json:
        print(json.dumps({
            "root": root, "min_target": args.min_target, "counts": counts, "facts": rep.facts,
            "permissions": sorted(perms), "sdks": rep.sdks, "findings": rep.findings, "needs_a_human": human,
        }, indent=2))
    else:
        print(f"Scanned: {root}")
        print(f"Manifests: {manifests}   Gradle files: {gradles}   Min target required: {args.min_target}")
        print("Result: " + "  ".join(f"{k}={v}" for k, v in counts.items()))
        for level in ("FAIL", "WARN", "UNKNOWN", "INFO", "PASS"):
            items = [f for f in rep.findings if f["level"] == level]
            if not items:
                continue
            print(f"\n== {level} ==")
            for f in items:
                loc = f" [{f['where']}]" if f["where"] else ""
                print(f"- {f['message']}{loc}")
                if f["fix"]:
                    print(f"    fix: {f['fix']}")
        if rep.sdks:
            print("\n== SDKs implying data handling (use for Data safety + privacy policy) ==")
            for label, info in sorted(rep.sdks.items()):
                print(f"- {label}: {info['data']}  (found in {info['found_in']})")
        if perms:
            print("\n== Permissions in scanned manifests ==")
            for p in sorted(perms):
                print(f"- {p}")
        print("\n== Needs a human (not checkable here) ==")
        for h in human:
            print(f"- {h}")
    sys.exit(1 if counts["FAIL"] else 0)


if __name__ == "__main__":
    main()
