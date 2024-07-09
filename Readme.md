# TalkSync v2
It's the upgradation of TalkSync using FastAPI in the backend instead of a pseudo FastAPI-like library

## Techs
- Backend - `FastAPI` + `SQLalchemy`
- Frontend - `SvelteKit`

## Install and Run

Copy files from github:
```bash
git clone https://github.com/saged-sama/TalkSyncv2.git
```
<b>Backend</b><br>
Go to the backend directory.

Set up python environment and then run:
```bash
pip install --no-cache-dir -r requirements.txt
```

When installation is complete run
```bash
uvicorn app.app:app --reload

#or replace hostname and port in the following
uvicorn app.app:app --host hostname --port port --reload
```

<b>Frontend</b> <br>
In the frontend directory. Create a `.env` file and give the backend address like so

```python
PUBLIC_API_ROOT = "http://localhost:8000/api/v1"
```

Then run
```bash
npm run dev

#or
npm run dev -- --host
```

Or build and run
```bash
npm run build
node build
```
All security is turned off for now
The adapter `@sveltejs/adapter-node` is used

## Testing
- Open two accounts from two different browsers, or incognito
- Send Messages back and forth