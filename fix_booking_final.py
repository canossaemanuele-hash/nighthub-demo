import re

with open('index.html', 'r') as f:
    content = f.read()

# Ensure selectedTavolo is logged and checked before insert
pattern = r'try \{.*?if \(checkTable\) \{'
replacement = """
            try {
                console.log("LOG: Avvio prenotazione...", {
                    serata: window.currentSerataId,
                    tavolo: selectedTavolo,
                    cliente: window.currentUser
                });

                if(!selectedTavolo) {
                    showToast("Seleziona prima un tavolo sulla mappa", "⚠️");
                    document.getElementById('modal-pagamento').classList.add('hidden');
                    return;
                }

                const { data: checkTable } = await client.from('prenotazioni').select('id').eq('tavolo_id', selectedTavolo.tavolo_id).eq('serata_id', window.currentSerataId).maybeSingle();

                if (checkTable) {"""

content = re.sub(pattern, replacement, content, flags=re.DOTALL)

# Also ensure customer-name is captured or fallback to currentUser
# The insert already uses: cliente: document.getElementById("customer-name").value || window.currentUser

with open('index.html', 'w') as f:
    f.write(content)
