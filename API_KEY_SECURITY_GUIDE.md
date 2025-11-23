# Google API Key Security Guide

## Immediate Actions Required

1. **Generate a New API Key**: 
   - Go to the [Google Cloud Console](https://console.cloud.google.com/)
   - Select your project
   - Navigate to "APIs & Services" > "Credentials"
   - Click "Create Credentials" > "API Key"
   - Copy the newly generated key

2. **Replace the Placeholder in .env File**:
   - Open the `.env` file in your project
   - Replace `YOUR_NEW_API_KEY_HERE` with your actual new API key
   - Save the file

3. **Restrict Your API Key** (Important):
   - In the Google Cloud Console, click on your API key
   - Under "Application restrictions", select appropriate restrictions:
     - For web applications: Add your domain(s)
     - For server applications: Restrict by IP address if possible
   - Under "API restrictions", select only the APIs you need (e.g., Generative Language API)
   - Click "Save"

## Best Practices for API Key Security

### 1. Environment Variables
Always store API keys in environment variables, never in your source code:
```python
import os
api_key = os.getenv('GOOGLE_GEMINI_API_KEY')
```

### 2. .gitignore Configuration
Ensure your `.gitignore` file includes:
```
.env
.env.local
.env.*.local
```

### 3. Regular Rotation
- Rotate your API keys regularly (every 90 days)
- Monitor API usage in the Google Cloud Console
- Set up alerts for unusual activity

### 4. Access Control
- Limit who has access to your API keys
- Use different keys for different environments (development, staging, production)
- Apply the principle of least privilege

## What to Do If Your Key Is Compromised Again

1. Immediately regenerate the API key in Google Cloud Console
2. Update your `.env` file with the new key
3. Revoke the compromised key
4. Check your application logs for unauthorized usage
5. Consider enabling billing alerts to monitor unexpected charges

## Additional Security Measures

1. **Use Google Cloud Service Accounts** for server-to-server authentication when possible
2. **Enable VPC Service Controls** for additional security boundaries
3. **Audit logs regularly** in Google Cloud Console
4. **Set up budget alerts** to monitor for unexpected API usage costs

Remember: Never commit API keys to version control systems like Git. Always use environment variables and proper secret management practices.