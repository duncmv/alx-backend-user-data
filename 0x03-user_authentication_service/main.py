#!/usr/bin/env python3
"""
Main file
"""
import requests


def register_user(email: str, password: str) -> None:
    """Register a user"""
    url = "http://localhost:5000/users"
    data = {"email": email, "password": password}
    resp = requests.post(url, data=data)
    assert resp.status_code == 200
    assert resp.json() == {"email": email, "message": "user created"}


def log_in(email: str, password: str) -> str:
    """Login a user"""
    url = "http://localhost:5000/sessions"
    data = {"email": email, "password": password}
    resp = requests.post(url, data=data)
    assert resp.status_code == 200
    assert resp.json() == {"email": email, "message": "logged in"}
    return resp.cookies.get('session_id')


def log_in_wrong_password(email: str, password: str) -> None:
    """Login a user with wrong password"""
    url = "http://localhost:5000/sessions"
    data = {"email": email, "password": password}
    resp = requests.post(url, data=data)
    assert resp.status_code == 401


def profile_unlogged() -> None:
    """Profile unlogged"""
    url = "http://localhost:5000/profile"
    resp = requests.get(url)
    assert resp.status_code == 403


def profile_logged(session_id: str) -> None:
    """Profile logged"""
    url = "http://localhost:5000/profile"
    resp = requests.get(url, cookies={'session_id': session_id})
    assert resp.status_code == 200
    assert resp.json() == {"email": "guillaume@holberton.io"}


def log_out(session_id: str) -> None:
    """Log out"""
    url = "http://localhost:5000/sessions"
    resp = requests.delete(url, cookies={'session_id': session_id})
    assert resp.status_code == 200


def reset_password_token(email: str) -> str:
    """Reset password"""
    url = "http://localhost:5000/reset_password"
    data = {"email": email}
    resp = requests.post(url, data=data)
    assert resp.status_code == 200
    return resp.json().get('reset_token')


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """Update password"""
    url = "http://localhost:5000/reset_password"
    data = {"email": email, "reset_token": reset_token,
            "new_password": new_password}
    resp = requests.put(url, data=data)
    assert resp.status_code == 200


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
