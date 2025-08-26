# AI SaaS Platform - Full-Stack Application

A complete, production-ready AI SaaS platform similar to Sintra.ai, built with Next.js, TypeScript, TailwindCSS, and multiple AI integrations.

## 🚀 Features

### Frontend
- **Landing Page**: Hero section, features, pricing, testimonials
- **Authentication**: JWT-based login/register with role-based access
- **User Dashboard**: AI tools, usage statistics, responsive design
- **Admin Panel**: User management, analytics, AI feature controls
- **AI Tools**: Text generation, image creation, code generation, content summarization
- **Dark/Light Mode**: Full theme switching capability
- **Responsive Design**: Mobile-first approach with Framer Motion animations

### Backend
- **API Routes**: RESTful endpoints for auth, AI tools, admin functions
- **JWT Authentication**: Secure token-based authentication with refresh tokens
- **Role-Based Access Control**: User and admin permissions
- **AI Integration**: Multiple AI services with usage tracking
- **Database Integration**: Support for Supabase, Firebase, or SQLite

## 📁 Project Structure

```
ai-saas-platform/
├── components/           # Reusable React components
├── pages/               # Next.js pages and API routes
│   ├── api/            # Backend API endpoints
│   │   ├── auth/       # Authentication routes
│   │   ├── ai/         # AI tool endpoints
│   │   └── admin/      # Admin panel APIs
│   ├── auth/           # Auth pages (login, register)
│   ├── dashboard/      # User dashboard pages
│   └── admin/          # Admin panel pages
├── lib/                # Utility functions and configurations
├── types/              # TypeScript type definitions
├── styles/             # CSS and styling files
├── public/             # Static assets
├── database/           # Database schema and migrations
└── docs/               # Documentation
```

## 🛠 Installation & Setup

### Prerequisites
- Node.js 18+ and npm/yarn
- Git for version control
- Database (Supabase account recommended)

### Local Development

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/ai-saas-platform.git
cd ai-saas-platform
```

2. **Install dependencies**
```bash
npm install
# or
yarn install
```

3. **Environment setup**
```bash
cp .env.example .env.local
```

Edit `.env.local` with your configuration:
```env
# Authentication
JWT_SECRET=your-super-secret-jwt-key-here
JWT_REFRESH_SECRET=your-refresh-token-secret

# Database - Supabase (Recommended)
SUPABASE_URL=your-supabase-project-url
SUPABASE_ANON_KEY=your-supabase-anon-key
SUPABASE_SERVICE_KEY=your-supabase-service-key

# AI API Keys (Optional - mock responses used if not provided)
OPENAI_API_KEY=sk-your-openai-api-key
STABILITY_API_KEY=sk-your-stability-api-key
HUGGINGFACE_API_KEY=hf_your-huggingface-token

# Admin Settings
ADMIN_EMAIL=admin@yourdomain.com
ADMIN_PASSWORD=secure-admin-password
```

4. **Run the development server**
```bash
npm run dev
# or
yarn dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

## 🗄️ Database Setup

### Option 1: Supabase (Recommended)

1. Create a new project at [supabase.com](https://supabase.com)
2. Run the SQL schema in your Supabase SQL editor (found in `database/schema.sql`)
3. Update your environment variables with Supabase URL and keys

### Option 2: SQLite (Local Development)

For local development, the app can use SQLite with the same schema. The database file will be created automatically at `./dev.db`.

## 🚀 Deployment

### Vercel Deployment (Recommended)

1. **Connect to Vercel**
```bash
npm i -g vercel
vercel login
vercel
```

2. **Set environment variables in Vercel dashboard**
- Go to your project settings
- Add all environment variables from `.env.local`

3. **Deploy**
```bash
vercel --prod
```

### Alternative Deployment Options

- **Netlify**: Use the build command `npm run build && npm run export`
- **Railway**: Direct deployment from GitHub
- **DigitalOcean App Platform**: Container deployment
- **AWS Amplify**: Full-stack deployment

## 🔧 Configuration

### AI Services Setup

#### OpenAI Integration
1. Get API key from [platform.openai.com](https://platform.openai.com)
2. Add to environment: `OPENAI_API_KEY=sk-your-key`

#### Stability AI (Image Generation)
1. Get API key from [platform.stability.ai](https://platform.stability.ai)
2. Add to environment: `STABILITY_API_KEY=sk-your-key`

#### Hugging Face (Alternative AI Models)
1. Get token from [huggingface.co](https://huggingface.co)
2. Add to environment: `HUGGINGFACE_API_KEY=hf_your-token`

## 📊 Usage Analytics

The platform tracks:
- **User Registration/Login**: Authentication events
- **AI Tool Usage**: Per-tool usage statistics  
- **API Calls**: Rate limiting and quota management
- **Admin Analytics**: User growth, revenue metrics

## 🧪 Testing

```bash
# Type checking
npm run type-check

# Linting
npm run lint

# Build test
npm run build
```

## 📚 API Documentation

### Authentication Endpoints

- `POST /api/auth/login` - User login
- `POST /api/auth/register` - User registration  

### AI Tool Endpoints

- `POST /api/ai/text-generate` - Text generation
- `POST /api/ai/image-generate` - Image creation

### Admin Endpoints

- `GET /api/admin/users` - List all users
- `GET /api/admin/analytics` - Platform analytics

## 🔑 Default Login Credentials

**Admin Account:**
- Email: `admin@aiplatform.com`
- Password: `admin123`

**User Account:**
- Email: `user@example.com`
- Password: `user123`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Built with ❤️ using Next.js, TypeScript, and TailwindCSS**"# ai-app" 
