import re

with open('index.html', 'r') as f:
    content = f.read()

# Fix the checkLogin function logic
# It should look something like this:
# if (email.includes('security')) {
#     window.userRole = 'security';
#     ...
# } else {
#     ...
# }

pattern = r"(if\(email\.includes\('boss'\)\) window\.userRole = 'boss'; // Override for legacy boss)(\s+)(document\.getElementById\('login-screen'\)\.classList\.add\('hidden'\);)"
replacement = r"\1\2\2if (email.includes('security')) {\2    window.userRole = 'security';\2    \3"

content = re.sub(pattern, replacement, content, flags=re.DOTALL)

with open('index.html', 'w') as f:
    f.write(content)
