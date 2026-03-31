import re

with open('index.html', 'r') as f:
    content = f.read()

# 1. Clean up duplicate eliminaSerata and renderSerateBoss
# First, remove everything from 'async function eliminaSerata' up to 'async function fetchSerate()'
# Then re-inject clean versions.

pattern = r'async function eliminaSerata\(id\) \{.*?async function fetchSerate\(\)'
clean_js = """
        async function eliminaSerata(id) {
            if(!confirm("Sei sicuro di voler eliminare questa serata?")) return;
            const { error } = await client.from('serate').delete().eq('id', id);
            if (error) {
                showToast("Errore eliminazione", "⛔");
                console.error(error);
            } else {
                showToast("Serata eliminata!", "🗑️");
                fetchSerate();
            }
        }

        function renderSerateBoss(data) {
            const container = document.getElementById('boss-lista-serate');
            if(!container) return;
            container.innerHTML = "";
            data.forEach(s => {
                container.innerHTML += `
                    <div class="flex justify-between items-center p-4 bg-slate-900 rounded-2xl border border-slate-800">
                        <div>
                            <p class="text-white text-xs font-black uppercase">\${s.nome}</p>
                            <p class="text-[9px] text-slate-500 font-bold">\${s.data}</p>
                        </div>
                        <button onclick="eliminaSerata(\${s.id})" class="bg-red-600 text-white px-3 py-2 rounded-xl text-[9px] font-black uppercase shadow-lg active:scale-95 transition-transform">🗑️ Elimina</button>
                    </div>
                `;
            });
        }

        async function fetchSerate()"""

content = re.sub(pattern, clean_js, content, flags=re.DOTALL)

with open('index.html', 'w') as f:
    f.write(content)
