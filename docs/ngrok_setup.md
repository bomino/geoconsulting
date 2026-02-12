# Sharing the Dev App via ngrok

## One-time setup

1. Sign up at https://ngrok.com (free account)
2. Copy your authtoken from the ngrok dashboard
3. Run: `ngrok config add-authtoken <your-token>`

## Every time you want to share

Terminal 1 — start Django:

```bash
cd geoconsulting
python manage.py runserver
```

Terminal 2 — start ngrok:

```bash
ngrok http 8000
```

ngrok will display a URL like `https://abc123.ngrok-free.app`. Share that with colleagues.

## Notes

- The URL changes every time you restart ngrok (free tier)
- Colleagues will see an ngrok interstitial page on first visit — click "Visit Site" to proceed
- The link only works while both terminals are running
- Admin panel: append `/admin/` to the ngrok URL
- `CSRF_TRUSTED_ORIGINS` is already configured in `config/settings/development.py`
