#!/usr/bin/env python3
"""
Generate a secure secret key for Flask application
"""
import secrets

if __name__ == "__main__":
    secret_key = secrets.token_hex(32)
    print("\n" + "="*60)
    print("SECURE SECRET KEY GENERATED")
    print("="*60)
    print(f"\n{secret_key}\n")
    print("="*60)
    print("\nCopy this key and add it as an environment variable")
    print("in Render with the name: SECRET_KEY")
    print("="*60 + "\n")
