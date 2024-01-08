# Nginx Reverse Proxy README

This Nginx Reverse Proxy configuration is tailored for local development with a FastAPI server. It efficiently directs incoming requests to the FastAPI application running on `localhost:8000`.

---

## Setup:

- **Configure Nginx:**
   - Ensure Nginx is installed.
   - Update `/reverse-proxy/*.conf` to include additional configurations:
     ```nginx
     include /reverse-proxy/*.conf;
     ```
   - Restart Nginx:
     ```bash
     sudo service nginx restart
     ```

- **Run FastAPI Server:**
   - Ensure FastAPI is running on `localhost:8000`.

- **Access Application:**
   - Open your browser and visit [http://localhost](http://localhost).


---
---

<p align="center">The End, Thank You!</p>

---