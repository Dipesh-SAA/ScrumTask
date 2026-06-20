{
  "tickets": [
    {
      "ticket_id": "US-FP-001",
      "title": "Forget Password Page",
      "test_cases": [
        {
          "test_case_id": "TC-FP-001",
          "title": "Verify presence of email input field",
          "category": "UI",
          "priority": "High",
          "preconditions": "User navigates to the forget password page",
          "expected_result": "Email input field is displayed on the forget password page"
        },
        {
          "test_case_id": "TC-FP-002",
          "title": "Verify presence of submit button",
          "category": "UI",
          "priority": "High",
          "preconditions": "User navigates to the forget password page",
          "expected_result": "Submit button is displayed on the forget password page"
        },
        {
          "test_case_id": "TC-FP-003",
          "title": "Verify email field accepts valid email format",
          "category": "Functional",
          "priority": "High",
          "preconditions": "User is on the forget password page",
          "expected_result": "Email field accepts input in valid email format"
        },
        {
          "test_case_id": "TC-FP-004",
          "title": "Verify error message for invalid email format",
          "category": "Validation",
          "priority": "High",
          "preconditions": "User is on the forget password page",
          "expected_result": "Appropriate error message is displayed when an invalid email format is entered"
        },
        {
          "test_case_id": "TC-FP-005",
          "title": "Verify error message for empty email field",
          "category": "Validation",
          "priority": "High",
          "preconditions": "User is on the forget password page",
          "expected_result": "Appropriate error message is displayed when the email field is left empty and submit is clicked"
        },
        {
          "test_case_id": "TC-FP-006",
          "title": "Verify successful submission with registered email",
          "category": "Functional",
          "priority": "High",
          "preconditions": "User is on the forget password page and enters a registered email",
          "expected_result": "User receives confirmation that password reset instructions have been sent"
        },
        {
          "test_case_id": "TC-FP-007",
          "title": "Verify error message for unregistered email",
          "category": "Validation",
          "priority": "Medium",
          "preconditions": "User is on the forget password page and enters an unregistered email",
          "expected_result": "Appropriate error message is displayed for unregistered email"
        },
        {
          "test_case_id": "TC-FP-008",
          "title": "Verify navigation back to login page",
          "category": "Navigation",
          "priority": "Medium",
          "preconditions": "User is on the forget password page",
          "expected_result": "User can navigate back to the login page from the forget password page"
        },
        {
          "test_case_id": "TC-FP-009",
          "title": "Verify accessibility of forget password page",
          "category": "Accessibility",
          "priority": "Medium",
          "preconditions": "User attempts to access the forget password page",
          "expected_result": "Forget password page is accessible"
        },
        {
          "test_case_id": "TC-FP-010",
          "title": "Verify confirmation message after successful request",
          "category": "UI",
          "priority": "Medium",
          "preconditions": "User submits a valid email on the forget password page",
          "expected_result": "Confirmation message is displayed indicating that password reset instructions have been sent"
        }
      ]
    }
  ]
}