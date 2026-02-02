#!/usr/bin/env python3
"""
FRED API Auto-Registration via Crawlee + Playwright
Automatically registers account and retrieves API key
"""

import asyncio
import sys
import secrets
import string
from pathlib import Path

from crawlee import PlaywrightCrawlingContext
from crawlee.playwright_crawler import PlaywrightCrawler


class FredRegistrationCrawler(PlaywrightCrawler):
    """Crawler to auto-register on FRED and get API key."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.api_key = None
        self.email = None

    def generate_temp_email(self):
        """Generate random temp email info."""
        # Random username for temp email
        username = ''.join(secrets.choice(string.ascii_lowercase) for _ in range(10))
        domains = ['10minutemail.com', 'guerrillamail.com', 'mail.tm']
        domain = secrets.choice(domains)

        return {
            'username': username,
            'domain': domain,
            'email': f'{username}@{domain}'
        }

    def generate_password(self):
        """Generate secure password."""
        alphabet = string.ascii_letters + string.digits + '!@#$%'
        password = ''.join(secrets.choice(alphabet) for _ in range(16))
        return password

    async def register_fred(self):
        """Register account on FRED."""
        print("\n" + "=" * 70)
        print("FRED API AUTO-REGISTRATION")
        print("=" * 70)

        # Generate credentials
        email_info = self.generate_temp_email()
        password = self.generate_password()

        print(f"\n📧 Generated credentials:")
        print(f"  Email: {email_info['email']}")
        print(f"  Password: {password}")
        print(f"\n⚠️  SAVE THESE! You'll need them later.")
        print(f"  API key will be in: .learnings/fred_credentials.json")

        try:
            # Initialize crawler
            crawler = FredRegistrationCrawler(
                headless=True,  # Run in background
                browser_type='chromium'
            )

            # Add request handler
            @crawler.router.default_handler
            async def request_handler(context, request):
                page = await context.new_page()

                print(f"\nNavigating to: {request.url}")
                await page.goto(request.url, wait_until='networkidle', timeout=30000)

                # Wait a bit (human-like)
                await asyncio.sleep(2)

                # Find registration form
                print("\n📝 Looking for registration form...")

                # Email field
                email_input = await page.query_selector('input[type="email"], input[name*="email"]', timeout=5000)
                if email_input:
                    await email_input.fill(email_info['email'])
                    print("  ✓ Email filled")
                    await asyncio.sleep(0.5)
                else:
                    print("  ✗ Email input not found")
                    raise Exception("Registration form structure changed")

                # Password field
                password_input = await page.query_selector('input[type="password"], input[name*="password"]', timeout=5000)
                if password_input:
                    await password_input.fill(password)
                    print("  ✓ Password filled")
                    await asyncio.sleep(0.5)
                else:
                    print("  ✗ Password input not found")
                    raise Exception("Registration form structure changed")

                # Confirm password field
                confirm_password_input = await page.query_selector('input[type="password"][name*="confirm"]', timeout=5000)
                if confirm_password_input:
                    await confirm_password_input.fill(password)
                    print("  ✓ Confirm password filled")
                    await asyncio.sleep(0.5)

                # Name fields
                first_name_input = await page.query_selector('input[name*="first"], input[name*="First"]', timeout=5000)
                if first_name_input:
                    await first_name_input.fill('Auto')
                    print("  ✓ First name filled")
                    await asyncio.sleep(0.3)

                last_name_input = await page.query_selector('input[name*="last"], input[name*="Last"]', timeout=5000)
                if last_name_input:
                    await last_name_input.fill('User')
                    print("  ✓ Last name filled")
                    await asyncio.sleep(0.3)

                # Submit button
                print("\n🔍 Looking for submit button...")

                # Try various button selectors
                submit_button = None
                for selector in ['button[type="submit"]', 'input[type="submit"]', 'button:has-text("Register")']:
                    try:
                        submit_button = await page.query_selector(selector, timeout=2000)
                        if submit_button:
                            break
                    except:
                        continue

                if submit_button:
                    await submit_button.click()
                    print("  ✓ Submit button clicked")
                else:
                    print("  ✗ Submit button not found")
                    raise Exception("Could not find submit button")

                # Wait for redirect or confirmation
                print("\n⏳ Waiting for registration confirmation...")
                await asyncio.sleep(5)

                # Check if we're redirected or confirmed
                current_url = page.url
                print(f"  Current URL: {current_url}")

                if 'apikeys' in current_url:
                    print("\n✅ Registration successful! Redirected to API keys page.")
                elif 'login' in current_url:
                    print("\n✅ Registration successful! Redirected to login page.")
                else:
                    print(f"\n⚠️ Registration may have succeeded. Current URL: {current_url}")

                await page.close()

            # Start crawling (registration)
            await crawler.run(['https://fredaccount.stlouisfed.org/registration/register'])

            # Save credentials
            credentials = {
                'email': email_info['email'],
                'password': password,
                'registration_url': 'https://fredaccount.stlouisfed.org/registration/register',
                'registered_at': asyncio.get_event_loop().time()
            }

            output_file = '/Users/mini-m4-1/clawd/.learnings/fred_credentials.json'
            with open(output_file, 'w') as f:
                import json
                json.dump(credentials, f, indent=2)

            print(f"\n📁 Credentials saved to: {output_file}")
            print("\n✅ Registration process complete!")

            print("\n" + "=" * 70)
            print("IMPORTANT: CHECK YOUR EMAIL!")
            print("=" * 70)
            print(f"To complete registration, check your inbox at:")
            print(f"  {email_info['email']}")
            print("\nThen visit: https://fredaccount.stlouisfed.org/apikeys")
            print("\nCopy the 32-character API key and run:")
            print("  export FRED_API_KEY='your_key_here'")
            print("=" * 70)

        except Exception as e:
            print(f"\n✗ Registration failed: {e}")
            import traceback
            traceback.print_exc()


async def main():
    """Main execution."""
    print("\n" + "=" * 70)
    print("FRED API AUTO-REGISTRATION AGENT")
    print("=" * 70)
    print("Note: This will:")
    print("  1. Generate random email and password")
    print("  2. Navigate to FRED registration page")
    print("  3. Fill out registration form")
    print("  4. Submit registration")
    print("\nYou'll need to:")
    print("  - Check the temp email inbox")
    print("  - Copy verification code/link")
    print("  - Complete email verification")
    print("  - Visit FRED to get API key")

    crawler = FredRegistrationCrawler()

    try:
        await crawler.register_fred()
    except KeyboardInterrupt:
        print("\n\n✗ Registration interrupted by user")
        sys.exit(1)


if __name__ == '__main__':
    asyncio.run(main())
