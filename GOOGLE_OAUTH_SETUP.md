# Google OAuth 2.0 Setup Guide

This guide will help you set up Google OAuth 2.0 authentication for the login page.

## Step 1: Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click on the project dropdown and select "New Project"
3. Enter a project name (e.g., "Login App")
4. Click "Create"

## Step 2: Enable Google+ API

1. In the Google Cloud Console, navigate to **APIs & Services** > **Library**
2. Search for "Google+ API" or "Google Identity Services"
3. Click on it and click **Enable**

## Step 3: Create OAuth 2.0 Credentials

1. Navigate to **APIs & Services** > **Credentials**
2. Click **Create Credentials** > **OAuth client ID**
3. If prompted, configure the OAuth consent screen:
   - Choose **External** (unless you have a Google Workspace)
   - Fill in the required fields:
     - App name: Your app name
     - User support email: Your email
     - Developer contact information: Your email
   - Click **Save and Continue**
   - Add scopes: `openid`, `email`, `profile`
   - Click **Save and Continue**
   - Add test users (if needed)
   - Click **Save and Continue**
   - Review and click **Back to Dashboard**

4. Create OAuth Client ID:
   - Application type: **Web application**
   - Name: "Login App Web Client"
   - Authorized JavaScript origins:
     - Add: `http://localhost` (for local testing)
     - Add: `http://localhost:8000` (if using a local server)
     - Add your production domain when ready
   - Authorized redirect URIs:
     - Add: `http://localhost/login.html` (or your actual page path)
     - Add: `http://localhost:8000/login.html` (if using a local server)
     - Add your production URL when ready
   - Click **Create**

5. Copy the **Client ID** (it looks like: `123456789-abcdefghijklmnop.apps.googleusercontent.com`)

## Step 4: Configure the Login Page

1. Open `login.html` in a text editor
2. Find this line in the JavaScript section:
   ```javascript
   const GOOGLE_CLIENT_ID = 'YOUR_GOOGLE_CLIENT_ID.apps.googleusercontent.com';
   ```
3. Replace `YOUR_GOOGLE_CLIENT_ID.apps.googleusercontent.com` with your actual Client ID
4. Save the file

## Step 5: Test the Integration

1. Open `login.html` in a web browser
2. Click the "Sign in with Google" button
3. You'll be redirected to Google's consent screen
4. After authorizing, you'll be redirected back with an authorization code
5. The authorization code will be displayed on the page

## How It Works

The implementation uses **OAuth 2.0 Authorization Code Flow**:

1. User clicks "Sign in with Google"
2. User is redirected to Google's authorization server
3. User grants permission
4. Google redirects back with an **authorization code**
5. The authorization code is displayed on the page
6. You can copy this code and exchange it for tokens on your backend server

## Backend Token Exchange

To exchange the authorization code for access/refresh tokens, make a POST request to Google's token endpoint:

```javascript
// Example using fetch (should be done on your backend server)
const response = await fetch('https://oauth2.googleapis.com/token', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/x-www-form-urlencoded',
  },
  body: new URLSearchParams({
    code: authorizationCode,
    client_id: YOUR_CLIENT_ID,
    client_secret: YOUR_CLIENT_SECRET, // Keep this secret on backend!
    redirect_uri: YOUR_REDIRECT_URI,
    grant_type: 'authorization_code'
  })
});

const tokens = await response.json();
// tokens.access_token - use this to access Google APIs
// tokens.refresh_token - use this to get new access tokens
```

## Security Notes

- **Never expose your Client Secret** in client-side code
- Always verify the `state` parameter to prevent CSRF attacks (already implemented)
- Use HTTPS in production
- Keep your Client Secret secure on your backend server
- The authorization code expires quickly (usually within 10 minutes)

## Troubleshooting

### "Invalid client" error
- Check that your Client ID is correct
- Verify the redirect URI matches exactly what you configured

### "Redirect URI mismatch" error
- Ensure the redirect URI in your code matches exactly what's configured in Google Cloud Console
- Check for trailing slashes, http vs https, port numbers

### Code not appearing
- Check browser console for errors
- Verify the redirect URI is correct
- Make sure you're testing on the same origin as configured

## Additional Resources

- [Google OAuth 2.0 Documentation](https://developers.google.com/identity/protocols/oauth2)
- [Google Identity Services](https://developers.google.com/identity/gsi/web)
- [OAuth 2.0 Playground](https://developers.google.com/oauthplayground/)

