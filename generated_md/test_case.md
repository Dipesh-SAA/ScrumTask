{
  "tickets": [
    {
      "ticket_id": "US-001",
      "title": "As a user, I want to login securely",
      "test_cases": [
        {
          "test_case_id": "TC-001",
          "title": "Login with valid credentials",
          "category": "Positive",
          "priority": "High",
          "preconditions": "User has a registered account with valid credentials",
          "expected_result": "User is successfully logged in and granted access"
        },
        {
          "test_case_id": "TC-002",
          "title": "Login with invalid password",
          "category": "Negative",
          "priority": "High",
          "preconditions": "User has a registered account",
          "expected_result": "User is not logged in and receives an error message"
        },
        {
          "test_case_id": "TC-003",
          "title": "Login with invalid username",
          "category": "Negative",
          "priority": "High",
          "preconditions": "User does not have an account with the entered username",
          "expected_result": "User is not logged in and receives an error message"
        },
        {
          "test_case_id": "TC-004",
          "title": "Login with empty username",
          "category": "Negative",
          "priority": "Medium",
          "preconditions": "Login form is displayed",
          "expected_result": "User is not logged in and receives an error message"
        },
        {
          "test_case_id": "TC-005",
          "title": "Login with empty password",
          "category": "Negative",
          "priority": "Medium",
          "preconditions": "Login form is displayed",
          "expected_result": "User is not logged in and receives an error message"
        },
        {
          "test_case_id": "TC-006",
          "title": "Verify secure transmission of credentials during login",
          "category": "Positive",
          "priority": "High",
          "preconditions": "User submits login form",
          "expected_result": "Credentials are transmitted securely"
        },
        {
          "test_case_id": "TC-007",
          "title": "Verify password is not visible during entry",
          "category": "Positive",
          "priority": "Medium",
          "preconditions": "User is entering password on login form",
          "expected_result": "Password characters are masked"
        },
        {
          "test_case_id": "TC-008",
          "title": "Verify error message does not reveal sensitive information",
          "category": "Negative",
          "priority": "High",
          "preconditions": "User attempts to login with invalid credentials",
          "expected_result": "Error message does not disclose whether username or password is incorrect"
        },
        {
          "test_case_id": "TC-009",
          "title": "Verify login with case-sensitive credentials",
          "category": "Positive",
          "priority": "Medium",
          "preconditions": "User has a registered account with case-sensitive credentials",
          "expected_result": "User is only logged in if the correct case is used"
        },
        {
          "test_case_id": "TC-010",
          "title": "Verify login fails with both fields empty",
          "category": "Negative",
          "priority": "Medium",
          "preconditions": "Login form is displayed",
          "expected_result": "User is not logged in and receives an error message"
        }
      ]
    }
  ]
}