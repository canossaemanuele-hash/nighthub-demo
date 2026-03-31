import re

with open('index.html', 'r') as f:
    content = f.read()

# 1. Declare let serate = [];
content = content.replace('let prenotazioni = [];', 'let serate = [];\n        let prenotazioni = [];')

# 2. Update fetchSerate() to store data
fetch_serate_old = """        async function fetchSerate() {
            const { data, error } = await client.from('serate').select('*').eq('attiva', true).order('data', { ascending: true });
            if (!error) {
                renderSerate(data);
            }
        }"""

fetch_serate_new = """        async function fetchSerate() {
            const { data, error } = await client.from('serate').select('*').eq('attiva', true).order('data', { ascending: true });
            if (!error) {
                serate = data || [];
                renderSerate(serate);
            }
        }"""

content = content.replace(fetch_serate_old, fetch_serate_new)

with open('index.html', 'w') as f:
    f.write(content)
