import re

with open('index.html', 'r') as f:
    content = f.read()

# 1. Total Rebranding
content = content.replace('TableKey', 'Malua 54')
content = content.replace('TABLEKEY', 'MALUA54')
content = content.replace('tablekey', 'malua54')
content = content.replace('NightHub', 'Malua 54')
content = content.replace('NIGHTHUB', 'MALUA54')
content = content.replace('nighthub', 'malua54')

# 2. Modify Login Screen for Registration
login_screen_pattern = r'(<div id="login-screen".*?>\s*<div.*?>\s*<h1.*?>.*?</h1>\s*<p.*?>.*?</p>\s*)(<div class="space-y-4">.*?</div>)(\s*</div>\s*</div>)'
signup_html = """
            <div id="login-form" class="space-y-4">
                <input type="text" id="user-input" placeholder="Email" class="w-full bg-slate-950/50 border border-slate-700 p-4 rounded-2xl text-sm focus:border-yellow-500 outline-none text-white italic">
                <input type="password" id="pass-input" placeholder="Password" class="w-full bg-slate-950/50 border border-slate-700 p-4 rounded-2xl text-sm focus:border-yellow-500 outline-none text-white">
                <button onclick="checkLogin()" class="w-full bg-yellow-500 text-black font-black py-4 rounded-2xl uppercase text-xs tracking-widest italic shadow-xl active:scale-95 transition-transform">Entra</button>
                <p class="text-[10px] text-slate-500 font-bold uppercase italic mt-4">Nuovo nel Club? <a href="javascript:void(0)" onclick="toggleAuth('signup')" class="text-yellow-500">Registrati</a></p>
            </div>
            <div id="signup-form" class="hidden space-y-4 text-left">
                <input type="email" id="reg-email" placeholder="Email" class="w-full bg-slate-950/50 border border-slate-700 p-4 rounded-2xl text-sm focus:border-yellow-500 outline-none text-white italic">
                <input type="password" id="reg-pass" placeholder="Password (min 6 car.)" class="w-full bg-slate-950/50 border border-slate-700 p-4 rounded-2xl text-sm focus:border-yellow-500 outline-none text-white">
                <div class="grid grid-cols-2 gap-2">
                    <button onclick="selectRegRole('cliente', this)" class="reg-role-btn py-3 rounded-xl border border-yellow-500 bg-slate-900 text-white text-[10px] font-black uppercase italic">Cliente</button>
                    <button onclick="selectRegRole('pr', this)" class="reg-role-btn py-3 rounded-xl border border-slate-700 text-slate-500 text-[10px] font-black uppercase italic">Promoter PR</button>
                </div>
                <button onclick="handleSignup()" class="w-full bg-white text-black font-black py-4 rounded-2xl uppercase text-xs tracking-widest italic shadow-xl active:scale-95 transition-transform">Crea Account</button>
                <p class="text-[10px] text-slate-500 font-bold uppercase italic mt-4 text-center">Hai già un account? <a href="javascript:void(0)" onclick="toggleAuth('login')" class="text-yellow-500">Accedi</a></p>
            </div>
"""

content = re.sub(login_screen_pattern, r'\1' + signup_html + r'\3', content, flags=re.DOTALL)

# 3. Add JS Functions and Update checkLogin
js_additions = """
        let regRole = 'cliente';
        function toggleAuth(mode) {
            document.getElementById('login-form').classList.toggle('hidden', mode === 'signup');
            document.getElementById('signup-form').classList.toggle('hidden', mode === 'login');
        }
        function selectRegRole(role, btn) {
            regRole = role;
            document.querySelectorAll('.reg-role-btn').forEach(b => {
                b.classList.remove('border-yellow-500', 'bg-slate-900', 'text-white');
                b.classList.add('border-slate-700', 'text-slate-500');
            });
            btn.classList.add('border-yellow-500', 'bg-slate-900', 'text-white');
            btn.classList.remove('border-slate-700', 'text-slate-500');
        }
        async function handleSignup() {
            const email = document.getElementById('reg-email').value;
            const pass = document.getElementById('reg-pass').value;
            if(!email || pass.length < 6) return showToast("Dati non validi", "⚠️");
            const { data, error } = await client.auth.signUp({
                email, password: pass,
                options: { data: { role: regRole } }
            });
            if(error) showToast(error.message, "⛔");
            else { showToast("Account creato! Ora accedi", "🎉"); toggleAuth('login'); }
        }
"""

# Inject JS before checkLogin
content = content.replace('async function checkLogin()', js_additions + '\n        async function checkLogin()')

# Update checkLogin to use metadata
check_login_update = """
            const user = data.user;
            window.currentUser = user.email;
            window.userRole = user.user_metadata.role || 'cliente';
            if(email.includes('boss')) window.userRole = 'boss'; // Override for legacy boss
"""
content = re.sub(r'const user = data\.user;.*?window\.userRole = .*?;', check_login_update, content, flags=re.DOTALL)

# Fix branding in scanner part specifically if needed (it was MALUA54-T... before)
content = content.replace('TABLEKEY-T', 'MALUA54-T')

with open('index.html', 'w') as f:
    f.write(content)
