from flask import Flask, render_template, request, jsonify
from playwright.sync_api import sync_playwright
import traceback

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/run-test", methods=["POST"])
def run_test():
    data = request.json
    base_url = data.get("base_url", "").strip()
    valid_email = data.get("valid_email", "").strip()
    valid_password = data.get("valid_password", "").strip()
    login_btn = data.get("login_btn", "").strip()

    results = []

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)

            # ── TC-001: Valid Login ──────────────────────────
            try:
                page = browser.new_page()
                page.goto(base_url, timeout=15000)
                page.fill("#email", valid_email)
                page.fill("#password", valid_password)
                page.click(f"xpath={login_btn}" if not login_btn.startswith("xpath=") else login_btn)
                page.wait_for_load_state("networkidle", timeout=10000)
                result_url = page.url
                passed = result_url != base_url
                results.append({
                    "id": "TC-LOGIN-001",
                    "name": "Valid Login Test",
                    "email": f"{valid_email} [CORRECT]",
                    "password": f"{valid_password} [CORRECT]",
                    "expected": "Redirect to dashboard",
                    "result": f"Redirected to {result_url}" if passed else "Still on login page",
                    "status": "PASS" if passed else "FAIL"
                })
                page.close()
            except Exception as e:
                results.append({
                    "id": "TC-LOGIN-001",
                    "name": "Valid Login Test",
                    "email": f"{valid_email} [CORRECT]",
                    "password": f"{valid_password} [CORRECT]",
                    "expected": "Redirect to dashboard",
                    "result": f"Error: {str(e)}",
                    "status": "ERROR"
                })

            # ── TC-002: Wrong Email ──────────────────────────
            try:
                page = browser.new_page()
                page.goto(base_url, timeout=15000)
                page.fill("#email", "wrong@gmail.com")
                page.fill("#password", valid_password)
                page.click(f"xpath={login_btn}" if not login_btn.startswith("xpath=") else login_btn)
                page.wait_for_load_state("networkidle", timeout=10000)
                result_url = page.url
                passed = result_url == base_url or "login" in result_url.lower()
                results.append({
                    "id": "TC-LOGIN-002",
                    "name": "Wrong Email Test",
                    "email": "wrong@gmail.com [WRONG]",
                    "password": f"{valid_password} [CORRECT]",
                    "expected": "Stay on login page",
                    "result": f"Stayed on {result_url}" if passed else f"Unexpected redirect to {result_url}",
                    "status": "PASS" if passed else "FAIL"
                })
                page.close()
            except Exception as e:
                results.append({
                    "id": "TC-LOGIN-002",
                    "name": "Wrong Email Test",
                    "email": "wrong@gmail.com [WRONG]",
                    "password": f"{valid_password} [CORRECT]",
                    "expected": "Stay on login page",
                    "result": f"Error: {str(e)}",
                    "status": "ERROR"
                })

            # ── TC-003: Wrong Password ───────────────────────
            try:
                page = browser.new_page()
                page.goto(base_url, timeout=15000)
                page.fill("#email", valid_email)
                page.fill("#password", "wrongpass123")
                page.click(f"xpath={login_btn}" if not login_btn.startswith("xpath=") else login_btn)
                page.wait_for_load_state("networkidle", timeout=10000)
                result_url = page.url
                passed = result_url == base_url or "login" in result_url.lower()
                results.append({
                    "id": "TC-LOGIN-003",
                    "name": "Wrong Password Test",
                    "email": f"{valid_email} [CORRECT]",
                    "password": "wrongpass123 [WRONG]",
                    "expected": "Stay on login page",
                    "result": f"Stayed on {result_url}" if passed else f"Unexpected redirect to {result_url}",
                    "status": "PASS" if passed else "FAIL"
                })
                page.close()
            except Exception as e:
                results.append({
                    "id": "TC-LOGIN-003",
                    "name": "Wrong Password Test",
                    "email": f"{valid_email} [CORRECT]",
                    "password": "wrongpass123 [WRONG]",
                    "expected": "Stay on login page",
                    "result": f"Error: {str(e)}",
                    "status": "ERROR"
                })

            # ── TC-004: Both Wrong ───────────────────────────
            try:
                page = browser.new_page()
                page.goto(base_url, timeout=15000)
                page.fill("#email", "fake@gmail.com")
                page.fill("#password", "fakepass999")
                page.click(f"xpath={login_btn}" if not login_btn.startswith("xpath=") else login_btn)
                page.wait_for_load_state("networkidle", timeout=10000)
                result_url = page.url
                passed = result_url == base_url or "login" in result_url.lower()
                results.append({
                    "id": "TC-LOGIN-004",
                    "name": "Both Wrong Credentials",
                    "email": "fake@gmail.com [WRONG]",
                    "password": "fakepass999 [WRONG]",
                    "expected": "Stay on login page",
                    "result": f"Stayed on {result_url}" if passed else f"Unexpected redirect to {result_url}",
                    "status": "PASS" if passed else "FAIL"
                })
                page.close()
            except Exception as e:
                results.append({
                    "id": "TC-LOGIN-004",
                    "name": "Both Wrong Credentials",
                    "email": "fake@gmail.com [WRONG]",
                    "password": "fakepass999 [WRONG]",
                    "expected": "Stay on login page",
                    "result": f"Error: {str(e)}",
                    "status": "ERROR"
                })

            # ── TC-005: Empty Fields ─────────────────────────
            try:
                page = browser.new_page()
                page.goto(base_url, timeout=15000)
                page.click(f"xpath={login_btn}" if not login_btn.startswith("xpath=") else login_btn)
                page.wait_for_load_state("networkidle", timeout=10000)
                result_url = page.url
                passed = result_url == base_url or "login" in result_url.lower()
                results.append({
                    "id": "TC-LOGIN-005",
                    "name": "Empty Fields Test",
                    "email": "(empty) [BLANK]",
                    "password": "(empty) [BLANK]",
                    "expected": "Stay on login page",
                    "result": f"Stayed on {result_url}" if passed else f"Unexpected redirect to {result_url}",
                    "status": "PASS" if passed else "FAIL"
                })
                page.close()
            except Exception as e:
                results.append({
                    "id": "TC-LOGIN-005",
                    "name": "Empty Fields Test",
                    "email": "(empty) [BLANK]",
                    "password": "(empty) [BLANK]",
                    "expected": "Stay on login page",
                    "result": f"Error: {str(e)}",
                    "status": "ERROR"
                })

            browser.close()

    except Exception as e:
        return jsonify({"error": str(e), "trace": traceback.format_exc()}), 500

    passed_count = sum(1 for r in results if r["status"] == "PASS")
    return jsonify({
        "results": results,
        "summary": {
            "total": len(results),
            "passed": passed_count,
            "failed": len(results) - passed_count
        }
    })

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
