import re

with open('index.html', 'r') as f:
    content = f.read()

# Fix the checkLogin structure to be syntactically correct and clean
fixed_check_login = """
        async function checkLogin() {
            const email = document.getElementById('user-input').value;
            const password = document.getElementById('pass-input').value;

            const btn = document.querySelector('button[onclick="checkLogin()"]');
            const originalText = btn.innerText;
            btn.innerText = "ACCESSO IN CORSO...";

            const { data, error } = await client.auth.signInWithPassword({
                email: email,
                password: password,
            });

            btn.innerText = originalText;

            if (error) {
                showToast("Credenziali errate", "⛔");
                return;
            }

            const user = data.user;
            window.currentUser = user.email;
            window.userRole = user.user_metadata.role || 'cliente';
            if(email.includes('boss')) window.userRole = 'boss';

            if (email.includes('security')) {
                window.userRole = 'security';
                document.getElementById('login-screen').classList.add('hidden');
                document.getElementById('app-content').classList.remove('hidden');
                document.getElementById('nav-generale').classList.add('hidden');
                document.getElementById('nav-security').classList.remove('hidden');
                switchView('security');
            } else {
                if (email === 'boss@malua54.com') window.userRole = 'boss';
                else if (email === 'pr@malua54.com') window.userRole = 'pr';

                document.getElementById('login-screen').classList.add('hidden');
                document.getElementById('landing-page').classList.remove('hidden');
                document.getElementById('btn-pr').classList.toggle('hidden', window.userRole !== 'pr');
                document.getElementById('btn-capo').classList.toggle('hidden', window.userRole !== 'boss');

                await loadConfig();
                fetchSerate();
                showToast("Login effettuato!", "🔓");
            }
        }
"""

pattern = r'async function checkLogin\(\) \{.*?\}\n\n        async function loadConfig\(\)'
content = re.sub(pattern, fixed_check_login + '\n\n        async function loadConfig()', content, flags=re.DOTALL)

with open('index.html', 'w') as f:
    f.write(content)
