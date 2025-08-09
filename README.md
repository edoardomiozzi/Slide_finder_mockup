# Slide Finder – Mock Demo (Business Case)

Demo pronta per mostrare la ricerca di slide simili in Teams **senza** dati SharePoint reali.

## Contenuto
- `main.py` – API FastAPI con endpoint mock `/search`, `/index`, `/health`
- `mock_data.json` – 15 risultati fittizi con `title`, `thumb_url`, `open_url`
- `adaptive_card.json` – Card pronta da incollare in Power Automate
- `requirements.txt`

## Avvio locale
```bash
python -m venv .venv && . .venv/bin/activate  # (Windows: .venv\Scripts\activate)
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```
Test rapido: apri http://localhost:8000/health e poi invia POST a `http://localhost:8000/search` con body:
```json
{ "query": "ebitda bridge", "top_k": 5 }
```

## Power Automate – Flow demo (senza Teams, super semplice)
1. Crea **Instant cloud flow** → trigger **Manually trigger a flow**.
2. Aggiungi **Initialize variable** `BASE_URL` (String) = `http://localhost:8000` *(oppure la tua URL su Render se pubblichi)*.
3. Aggiungi **Initialize variable** `query_text` (String) = `EBITDA bridge` (o usa un **Manual trigger input** di tipo testo).
4. **HTTP** (connettore HTTP):  
   - Method: `POST`  
   - URI: `@{format('{0}/search', variables('BASE_URL'))}`  
   - Headers: `Content-Type: application/json`  
   - Body:
   ```json
   {
     "query": "@{variables('query_text')}",
     "top_k": 5
   }
   ```
5. **Parse JSON** → Content: `@{body('HTTP')}` → **Generate from sample** incolla:
   ```json
   [
     {
       "title": "Quarterly Sales Overview",
       "deck_id": "deck-sales-q1",
       "slide_id": 1,
       "score": 0.92,
       "thumb_url": "https://placehold.co/200x120/png?text=Sales+Q1+S1",
       "open_url": "https://contoso.sharepoint.com/presentation1"
     }
   ]
   ```
6. **Post adaptive card in chat or channel** (se vuoi usare Teams) oppure **Compose** per vedere il JSON.  
   - Se usi Teams: copia il contenuto di `adaptive_card.json` nel campo Card Payload.  
   - Recipient: tu stesso. Post as: Flow bot.

**Suggerimento demo:** registra uno screen (2 minuti) che mostra: avvio flow → card con risultati.

## Pubblicazione rapida su Render (facoltativa)
- Crea un nuovo Web Service puntando a questa cartella (o carica il repo).  
- Command: `uvicorn main:app --host 0.0.0.0 --port 10000`  
- Port: `10000`

## Nota
Questo è un mock al 100%: niente SharePoint, niente Graph. In produzione sostituisci la sorgente dati del `/search` con il tuo indice vero.