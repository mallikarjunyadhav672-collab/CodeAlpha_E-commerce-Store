# LUXE Store — Django demo

This is a minimal Django scaffold to serve the provided `index (1).html` design as a template.

Quick start (Windows):

1. Create a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\activate
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Run the development server:

```powershell
python manage.py runserver
```

Open http://127.0.0.1:8000/ to view the site. The design and inline CSS/JS are preserved exactly from your provided `index (1).html`.

Next steps (optional):
- Hook up the front-end cart/wishlist to the `api/cart/` and `api/wishlist/` endpoints (currently demo endpoints exist in `shop.views`).
- Add static assets or break CSS/JS into separate static files.
- Replace `SECRET_KEY` in `luxe_store/settings.py` for production and set `DEBUG=False`.
