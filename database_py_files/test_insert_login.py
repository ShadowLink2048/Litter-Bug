from db_utils_login import insert_user

# Test data
test_users = [
    ("player1", "test_passkey_1"),
    ("player2", "test_passkey_2"),
    ("player3", "test_passkey_3"),
    ("player1", "should_fail_duplicate")  # This should trigger the duplicate check
]

for user_id, passkey in test_users:
    insert_user(user_id, passkey)
