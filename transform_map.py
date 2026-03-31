import re

with open('index.html', 'r') as f:
    content = f.read()

# 1. Update Modal Mappa to be dynamic
modal_mappa_pattern = r'<div id="modal-mappa".*?>.*?<img src=".*?"></div></div>'
updated_modal_mappa = '<div id="modal-mappa" class="hidden fixed inset-0 bg-black z-[4000] flex flex-col"><div class="p-5 flex justify-between bg-slate-950 items-center"><span class="text-yellow-500 font-black text-[10px] uppercase italic">Piantina Malua 54</span><button onclick="toggleMappa(false)" class="bg-white text-black px-4 py-2 rounded-xl text-xs font-black uppercase italic">Esci</button></div><div class="flex-1 img-viewer overflow-auto flex items-center justify-center p-4"><img id="mappa-img-viewer" src="https://i.postimg.cc/8zqmMw4B/Image-6.jpg" class="max-w-full max-h-full object-contain"></div></div>'
content = re.sub(modal_mappa_pattern, updated_modal_mappa, content, flags=re.DOTALL)

# 2. Update entraNelLocale to load the map
entra_nel_locale_pattern = r'async function entraNelLocale\(n, id\) {.*?window\.currentSerataId = id;.*?(?:const s = serate\.find.*?document\.getElementById\(\'mappa-img-viewer\'\)\.src = .*?;)?'
updated_entra_nel_locale = 'async function entraNelLocale(n, id) { window.currentSerataId = id; const s = serate.find(x => x.id === id); if(s && s.mappa_url) document.getElementById("mappa-img-viewer").src = s.mappa_url; else document.getElementById("mappa-img-viewer").src = "https://i.postimg.cc/8zqmMw4B/Image-6.jpg";'
content = re.sub(r'async function entraNelLocale\(n, id\) {.*?window\.currentSerataId = id;', updated_entra_nel_locale, content, flags=re.DOTALL)

with open('index.html', 'w') as f:
    f.write(content)
