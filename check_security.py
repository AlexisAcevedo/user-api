#!/usr/bin/env python3
"""
Security Verification Script for GitHub Upload

Verifica que no haya información sensible antes de subir a GitHub.
"""

import os
import re
import sys
from pathlib import Path

# Colores para terminal
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
CYAN = '\033[96m'
RESET = '\033[0m'

def print_header(text):
    print(f"\n{CYAN}{'='*60}{RESET}")
    print(f"{CYAN}{text:^60}{RESET}")
    print(f"{CYAN}{'='*60}{RESET}\n")

def print_success(text):
    print(f"{GREEN}✓ {text}{RESET}")

def print_error(text):
    print(f"{RED}✗ {text}{RESET}")

def print_warning(text):
    print(f"{YELLOW}⚠ {text}{RESET}")

def check_env_file_exists():
    """Verifica si .env existe"""
    print_header("1. Checking .env File")
    
    env_path = Path(".env")
    if env_path.exists():
        print_success(".env file exists (local)")
        return True
    else:
        print_warning(".env file not found (will be created on first run)")
        print("  → Create with: copy .env.example .env")
        return False

def check_gitignore():
    """Verifica si .gitignore contiene .env"""
    print_header("2. Checking .gitignore Configuration")
    
    if not Path(".gitignore").exists():
        print_error(".gitignore file not found!")
        return False
    
    with open(".gitignore", "r") as f:
        content = f.read()
    
    required_patterns = [
        r"^\.env$",
        r"\.env\.local",
        r"__pycache__",
        r"\.log",
    ]
    
    all_good = True
    for pattern in required_patterns:
        if re.search(pattern, content, re.MULTILINE):
            print_success(f"Pattern found: {pattern}")
        else:
            print_error(f"Pattern missing: {pattern}")
            all_good = False
    
    return all_good

def check_hardcoded_secrets():
    """Verifica código por secretos hardcodeados"""
    print_header("3. Checking for Hardcoded Secrets in Python Files")
    
    dangerous_patterns = [
        (r'password\s*=\s*["\'](?!CHANGE|YOUR|password)[^"\']+["\']', "Hardcoded password"),
        (r'api_key\s*=\s*["\'][^"\']+["\']', "Hardcoded API key"),
        (r'secret\s*=\s*["\'](?!dev-key)[^"\']+["\']', "Hardcoded secret"),
        (r'token\s*=\s*["\'][^"\']+["\']', "Hardcoded token"),
    ]
    
    all_good = True
    
    for py_file in Path(".").glob("**/*.py"):
        if any(skip in str(py_file) for skip in ["venv", "env", "__pycache__", ".git"]):
            continue
        
        try:
            with open(py_file, "r", encoding="utf-8") as f:
                lines = f.readlines()
            
            for line_num, line in enumerate(lines, 1):
                for pattern, description in dangerous_patterns:
                    if re.search(pattern, line, re.IGNORECASE):
                        # Ignore comments and .env.example
                        if not line.strip().startswith("#") and ".env.example" not in str(py_file):
                            print_error(f"{py_file}:{line_num} - {description}")
                            print(f"  {line.strip()[:80]}")
                            all_good = False
        
        except (UnicodeDecodeError, IsADirectoryError):
            pass
    
    if all_good:
        print_success("No hardcoded secrets found in Python files")
    
    return all_good

def check_env_example():
    """Verifica que .env.example tiene valores placeholder"""
    print_header("4. Checking .env.example Template")
    
    if not Path(".env.example").exists():
        print_warning(".env.example not found")
        return False
    
    with open(".env.example", "r") as f:
        content = f.read()
    
    # Debe contener placeholders, no valores reales
    required_placeholders = [
        "CHANGE",
        "YOUR_",
        "change",
        "example",
    ]
    
    has_placeholder = any(placeholder in content for placeholder in required_placeholders)
    
    if has_placeholder:
        print_success(".env.example contains placeholder values")
        return True
    else:
        print_warning(".env.example might contain real values")
        return False

def check_sensitive_files():
    """Verifica por archivos sensibles que no deben ser cometidos"""
    print_header("5. Checking for Sensitive Files")
    
    sensitive_patterns = [
        "*.pem",
        "*.key",
        "*.crt",
        "*.cert",
        "*.p12",
        "*.pfx",
        "*credentials*",
        "*secret*",
        ".env.*",
    ]
    
    found_sensitive = []
    
    for pattern in sensitive_patterns:
        for file in Path(".").glob(f"**/{pattern}"):
            if any(skip in str(file) for skip in ["venv", "env", "__pycache__", ".git", "node_modules"]):
                continue
            found_sensitive.append(file)
    
    if found_sensitive:
        print_warning("Sensitive files found (verify they are in .gitignore):")
        for file in found_sensitive:
            print(f"  - {file}")
        return False
    else:
        print_success("No unencrypted sensitive files found")
        return True

def check_git_status():
    """Verifica git status"""
    print_header("6. Checking Git Status")
    
    try:
        import subprocess
        
        # Verificar si .env está tracked
        result = subprocess.run(
            ["git", "ls-files"],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if ".env" in result.stdout:
            print_error(".env file is tracked in git (SECURITY RISK!)")
            print("  → Run: git rm --cached .env")
            print("  → Then commit the change")
            return False
        else:
            print_success(".env is not tracked in git")
            return True
    
    except (FileNotFoundError, subprocess.TimeoutExpired):
        print_warning("Git not available or not initialized")
        return True

def check_logs_directory():
    """Verifica si logs/ está en .gitignore"""
    print_header("7. Checking Logs Directory")
    
    if not Path("logs").exists():
        print_success("logs/ directory not found (will be created at runtime)")
        return True
    
    with open(".gitignore", "r") as f:
        content = f.read()
    
    if "logs/" in content:
        print_success("logs/ is in .gitignore")
        return True
    else:
        print_error("logs/ is NOT in .gitignore")
        return False

def check_docker_secrets():
    """Verifica que docker-compose no tiene secretos"""
    print_header("8. Checking Docker Configuration")
    
    docker_files = ["docker-compose.yml", "Dockerfile", "nginx.conf"]
    all_good = True
    
    for docker_file in docker_files:
        if not Path(docker_file).exists():
            continue
        
        with open(docker_file, "r") as f:
            content = f.read()
        
        # Debe usar variables, no valores reales
        if "${" in content or "$(" in content:
            print_success(f"{docker_file} uses variable substitution")
        elif any(word in content for word in ["DATABASE_URL", "SECRET_KEY"]):
            print_success(f"{docker_file} references environment variables")
        else:
            print_warning(f"{docker_file} might have hardcoded values")
            all_good = False
    
    return all_good

def main():
    print(f"\n{CYAN}🔐 GitHub Upload Security Verification{RESET}\n")
    
    results = {
        ".env file": check_env_file_exists(),
        ".gitignore": check_gitignore(),
        "Hardcoded secrets": check_hardcoded_secrets(),
        ".env.example": check_env_example(),
        "Sensitive files": check_sensitive_files(),
        "Git status": check_git_status(),
        "Logs directory": check_logs_directory(),
        "Docker config": check_docker_secrets(),
    }
    
    print_header("SUMMARY")
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for check, result in results.items():
        status = f"{GREEN}PASS{RESET}" if result else f"{RED}FAIL{RESET}"
        print(f"  {check:<30} [{status}]")
    
    print(f"\n{CYAN}{'='*60}{RESET}")
    print(f"Score: {passed}/{total}")
    
    if passed == total:
        print(f"{GREEN}✓ SAFE TO UPLOAD TO GITHUB!{RESET}\n")
        return 0
    elif passed >= total - 1:
        print(f"{YELLOW}⚠ MOSTLY SAFE - Review warnings above{RESET}\n")
        return 0
    else:
        print(f"{RED}✗ NOT SAFE TO UPLOAD - Fix errors above{RESET}\n")
        return 1

if __name__ == "__main__":
    sys.exit(main())
