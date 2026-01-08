"""Tests for access request and authentication flow."""

import pytest
import sqlite3
from pathlib import Path
import sys
import os

# Add src to path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from ui.access_request import (
    validate_email,
    validate_username,
    username_exists,
    email_has_pending_request,
    submit_access_request
)

# Test database path
TEST_DB = Path(__file__).parent.parent / "jdr_test.db"


@pytest.fixture(scope="function")
def test_db():
    """Create a test database for each test."""
    # Remove if exists
    if TEST_DB.exists():
        TEST_DB.unlink()
    
    # Create test database with schema
    conn = sqlite3.connect(TEST_DB)
    c = conn.cursor()
    
    c.execute('''
        CREATE TABLE users (
            username TEXT PRIMARY KEY,
            name TEXT,
            email TEXT,
            password_hash TEXT,
            role TEXT DEFAULT 'joueur',
            must_change_password BOOLEAN DEFAULT 0
        )
    ''')
    
    c.execute('''
        CREATE TABLE requests (
            username TEXT PRIMARY KEY,
            email TEXT,
            status TEXT DEFAULT 'PENDING',
            request_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()
    
    # Temporarily replace DB_PATH in access_request module
    import ui.access_request as ar
    original_db = ar.DB_PATH
    ar.DB_PATH = TEST_DB
    
    yield TEST_DB
    
    # Restore original DB_PATH
    ar.DB_PATH = original_db
    
    # Clean up
    if TEST_DB.exists():
        TEST_DB.unlink()


class TestEmailValidation:
    """Test email validation."""
    
    def test_valid_emails(self):
        """Test valid email formats."""
        valid_emails = [
            "user@example.com",
            "user.name@example.com",
            "user+tag@example.co.uk",
            "user_name@example.org"
        ]
        for email in valid_emails:
            assert validate_email(email) is True, f"Email '{email}' should be valid"
    
    def test_invalid_emails(self):
        """Test invalid email formats."""
        invalid_emails = [
            "invalid",
            "user@",
            "@example.com",
            "user@example",
            "user space@example.com"
        ]
        for email in invalid_emails:
            assert validate_email(email) is False, f"Email '{email}' should be invalid"


class TestUsernameValidation:
    """Test username validation."""
    
    def test_valid_usernames(self):
        """Test valid username formats."""
        valid_usernames = [
            "user123",
            "user_name",
            "a_b_c",
            "User123",
            "player_1"
        ]
        for username in valid_usernames:
            assert validate_username(username) is True, f"Username '{username}' should be valid"
    
    def test_invalid_usernames(self):
        """Test invalid username formats."""
        invalid_usernames = [
            "ab",  # Too short
            "user-name",  # Contains dash
            "user name",  # Contains space
            "user@name",  # Contains special char
            "a" * 21  # Too long (>20 chars)
        ]
        for username in invalid_usernames:
            assert validate_username(username) is False, f"Username '{username}' should be invalid"


class TestAccessRequest:
    """Test access request functionality."""
    
    def test_submit_valid_request(self, test_db):
        """Test submitting a valid access request."""
        success, message = submit_access_request("newuser", "user@example.com")
        assert success is True
        assert "✅" in message
        
        # Verify it's in the database
        conn = sqlite3.connect(TEST_DB)
        c = conn.cursor()
        result = c.execute(
            "SELECT status FROM requests WHERE username = ?",
            ("newuser",)
        ).fetchone()
        conn.close()
        
        assert result is not None
        assert result[0] == "PENDING"
    
    def test_duplicate_username(self, test_db):
        """Test that duplicate usernames are rejected."""
        # Insert a user first
        conn = sqlite3.connect(TEST_DB)
        c = conn.cursor()
        c.execute(
            "INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
            ("existing", "existing@example.com", "hash")
        )
        conn.commit()
        conn.close()
        
        # Try to create request with same username
        success, message = submit_access_request("existing", "other@example.com")
        assert success is False
        assert "❌" in message
    
    def test_invalid_email(self, test_db):
        """Test that invalid emails are rejected."""
        success, message = submit_access_request("newuser", "invalid-email")
        assert success is False
        assert "email" in message.lower()
    
    def test_invalid_username(self, test_db):
        """Test that invalid usernames are rejected."""
        success, message = submit_access_request("ab", "user@example.com")
        assert success is False
        assert "identifiant" in message.lower()
    
    def test_duplicate_pending_request(self, test_db):
        """Test that duplicate pending requests are rejected."""
        # First request
        success1, _ = submit_access_request("user1", "same@example.com")
        assert success1 is True
        
        # Second request with same email
        success2, message = submit_access_request("user2", "same@example.com")
        assert success2 is False
        assert "en cours" in message.lower()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
