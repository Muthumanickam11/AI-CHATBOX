# Deployment Guide - AI-CHATBOX Backend

## 🚀 Deployment Options

### Option 1: Render (Recommended)

1. **Create New Web Service**
   - Connect your GitHub repository
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

2. **Environment Variables**
   ```
   OPENAI_API_KEY=your_key_here
   DATABASE_URL=postgresql://user:pass@host/db
   SECRET_KEY=your_secret_key_here
   ```

3. **Database**
   - Add PostgreSQL database
   - Copy DATABASE_URL to environment variables

### Option 2: Railway

1. **Deploy from GitHub**
   ```bash
   railway login
   railway init
   railway up
   ```

2. **Add PostgreSQL**
   ```bash
   railway add postgresql
   ```

3. **Set Environment Variables**
   - Go to Variables tab
   - Add OPENAI_API_KEY, SECRET_KEY

### Option 3: Heroku

1. **Create App**
   ```bash
   heroku create ai-chatbox-backend
   heroku addons:create heroku-postgresql:hobby-dev
   ```

2. **Set Config**
   ```bash
   heroku config:set OPENAI_API_KEY=your_key
   heroku config:set SECRET_KEY=your_secret
   ```

3. **Deploy**
   ```bash
   git push heroku main
   ```

## 📝 Production Checklist

- [ ] Set strong SECRET_KEY (use: `openssl rand -hex 32`)
- [ ] Configure production DATABASE_URL
- [ ] Add OPENAI_API_KEY
- [ ] Update CORS origins in `app/main.py`
- [ ] Enable HTTPS
- [ ] Set up monitoring/logging
- [ ] Configure rate limiting
- [ ] Set up backup strategy
- [ ] Test all endpoints
- [ ] Document API for frontend team

## 🔒 Security

1. **Never commit `.env` file**
2. **Use environment variables for all secrets**
3. **Enable HTTPS in production**
4. **Implement rate limiting**
5. **Regular security audits**

## 📊 Monitoring

Access `/api/v1/health` for:
- System status
- Uptime metrics
- Request statistics
- Error rates

## 🌐 Frontend Integration

Update CORS origins in `app/main.py`:
```python
origins = [
    "https://your-frontend.vercel.app",
    "http://localhost:3000"  # for development
]
```

## 📞 API Endpoints

Base URL: `https://your-backend-url.com/api/v1`

- `POST /chat` - Main chat endpoint
- `POST /login` - User authentication
- `POST /signup` - User registration
- `POST /history` - Get chat history
- `POST /upload` - Upload documents
- `GET /health` - Health check

## 🐛 Troubleshooting

### Database Connection Issues
- Verify DATABASE_URL format
- Check database is accessible
- Ensure SSL mode is correct

### CORS Errors
- Add frontend URL to origins list
- Verify CORS middleware is configured

### OpenAI API Errors
- Check API key is valid
- Verify account has credits
- Check rate limits

## 📈 Scaling

For high traffic:
1. Use PostgreSQL connection pooling
2. Implement Redis caching
3. Add load balancer
4. Use CDN for static assets
5. Implement request queuing
