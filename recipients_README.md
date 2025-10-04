# Email Recipients Configuration

This document explains how to configure email recipients for the Veille Qualiopi program.

## Recipients JSON File

The `recipients.json` file contains the email addresses that will receive the veille juridique reports. The file is structured with two main groups:

### Structure

```json
{
    "to": [
        "recipient1@example.com",
        "recipient2@example.com",
        "recipient3@example.com"
    ],
    "cc": [
        "cc1@example.com",
        "cc2@example.com"
    ]
}
```

### Fields

- **`to`**: Array of email addresses that will be visible as primary recipients
- **`cc`**: Array of email addresses that will receive carbon copies (visible to all recipients)

### Usage

1. **Edit the recipients**: Replace the example email addresses with actual recipient addresses
2. **Add recipients**: Add more email addresses to either the `to` or `cc` arrays
3. **Remove recipients**: Remove email addresses from the arrays as needed
4. **Empty arrays**: You can have empty arrays if you don't want recipients in that category

### Examples

**Only TO recipients:**
```json
{
    "to": [
        "manager@company.com",
        "legal@company.com"
    ],
    "cc": []
}
```

**Only CC recipients:**
```json
{
    "to": [],
    "cc": [
        "archive@company.com",
        "backup@company.com"
    ]
}
```

**Mixed recipients:**
```json
{
    "to": [
        "primary@company.com"
    ],
    "cc": [
        "manager@company.com",
        "legal@company.com",
        "archive@company.com"
    ]
}
```

### Important Notes

- The program will automatically load this file when sending emails
- If both `to` and `cc` arrays are empty, the email will not be sent
- Email addresses should be valid and properly formatted
- The file must be valid JSON format
- The file should be named `recipients.json` and placed in the project root directory
- CC recipients are visible to all other recipients (unlike BCC which are hidden)
