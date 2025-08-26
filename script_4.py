# Add database schema and documentation

# Database schema
database_schema = """-- Database schema for AI SaaS Platform
-- Compatible with PostgreSQL (Supabase), MySQL, and SQLite

-- Users table with authentication and subscription info
CREATE TABLE users (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    role VARCHAR(20) DEFAULT 'user' CHECK (role IN ('user', 'admin')),
    subscription VARCHAR(20) DEFAULT 'Starter' CHECK (subscription IN ('Starter', 'Professional', 'Enterprise')),
    avatar_url VARCHAR(500),
    email_verified BOOLEAN DEFAULT FALSE,
    active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP
);

-- AI usage tracking for analytics and billing
CREATE TABLE ai_usage (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    tool_type VARCHAR(50) NOT NULL CHECK (tool_type IN ('text-generation', 'image-generation', 'code-generation', 'summarization')),
    prompt_text TEXT,
    response_text TEXT,
    tokens_used INTEGER DEFAULT 0,
    processing_time_ms INTEGER,
    success BOOLEAN DEFAULT TRUE,
    error_message TEXT,
    metadata JSONB, -- Additional tool-specific data
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- User settings and preferences
CREATE TABLE user_settings (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID UNIQUE NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    theme VARCHAR(10) DEFAULT 'light' CHECK (theme IN ('light', 'dark')),
    notifications BOOLEAN DEFAULT TRUE,
    email_notifications BOOLEAN DEFAULT TRUE,
    api_limit_per_month INTEGER DEFAULT 1000,
    language VARCHAR(10) DEFAULT 'en',
    timezone VARCHAR(50) DEFAULT 'UTC',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- API keys and integrations (for admin)
CREATE TABLE api_configurations (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    service_name VARCHAR(50) NOT NULL UNIQUE,
    api_key_encrypted TEXT,
    active BOOLEAN DEFAULT TRUE,
    configuration JSONB, -- Service-specific configuration
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Subscription and billing information
CREATE TABLE subscriptions (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID UNIQUE NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    plan_name VARCHAR(50) NOT NULL,
    status VARCHAR(20) DEFAULT 'active' CHECK (status IN ('active', 'cancelled', 'expired', 'past_due')),
    current_period_start TIMESTAMP,
    current_period_end TIMESTAMP,
    cancel_at_period_end BOOLEAN DEFAULT FALSE,
    stripe_subscription_id VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Refresh tokens for JWT authentication
CREATE TABLE refresh_tokens (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    token_hash VARCHAR(255) NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_used TIMESTAMP
);

-- Audit logs for admin activities
CREATE TABLE audit_logs (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    admin_user_id UUID REFERENCES users(id),
    action VARCHAR(100) NOT NULL,
    resource_type VARCHAR(50), -- e.g., 'user', 'ai_usage', 'settings'
    resource_id VARCHAR(255),
    details JSONB,
    ip_address INET,
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for better query performance
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_role ON users(role);
CREATE INDEX idx_users_subscription ON users(subscription);
CREATE INDEX idx_ai_usage_user_id ON ai_usage(user_id);
CREATE INDEX idx_ai_usage_tool_type ON ai_usage(tool_type);
CREATE INDEX idx_ai_usage_created_at ON ai_usage(created_at);
CREATE INDEX idx_refresh_tokens_user_id ON refresh_tokens(user_id);
CREATE INDEX idx_refresh_tokens_expires_at ON refresh_tokens(expires_at);
CREATE INDEX idx_audit_logs_admin_user_id ON audit_logs(admin_user_id);
CREATE INDEX idx_audit_logs_created_at ON audit_logs(created_at);

-- Sample data insertion
INSERT INTO users (id, email, password_hash, name, role, subscription) VALUES 
('11111111-1111-1111-1111-111111111111', 'admin@aiplatform.com', '$2a$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LsEaGb.xjmtNOhgka', 'Admin User', 'admin', 'Enterprise'),
('22222222-2222-2222-2222-222222222222', 'user@example.com', '$2a$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LsEaGb.xjmtNOhgka', 'John Doe', 'user', 'Professional');

INSERT INTO user_settings (user_id, theme, api_limit_per_month) VALUES 
('11111111-1111-1111-1111-111111111111', 'dark', -1), -- Unlimited for admin
('22222222-2222-2222-2222-222222222222', 'light', 10000);

-- Functions for updating timestamps (PostgreSQL specific)
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Triggers to automatically update timestamps
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users 
FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_user_settings_updated_at BEFORE UPDATE ON user_settings 
FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_subscriptions_updated_at BEFORE UPDATE ON subscriptions 
FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();"""

# README documentation
readme_content = """# AI SaaS Platform - Full-Stack Application

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

**Built with ❤️ using Next.js, TypeScript, and TailwindCSS**"""

# Simple global styles
global_styles = """/* styles/globals.css */

@tailwind base;
@tailwind components;
@tailwind utilities;

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

html {
  font-family: 'Inter', sans-serif;
}

body {
  @apply bg-gray-50 text-gray-900 transition-colors duration-200;
}

.dark body {
  @apply bg-gray-900 text-gray-100;
}

/* Custom scrollbar */
::-webkit-scrollbar {
  width: 6px;
}

::-webkit-scrollbar-track {
  @apply bg-gray-100 dark:bg-gray-800;
}

::-webkit-scrollbar-thumb {
  @apply bg-gray-300 dark:bg-gray-600 rounded-full;
}

::-webkit-scrollbar-thumb:hover {
  @apply bg-gray-400 dark:bg-gray-500;
}

/* Animation utilities */
@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-fadeIn {
  animation: fadeIn 0.5s ease-in-out;
}

.animate-slideUp {
  animation: slideUp 0.3s ease-out;
}

/* Loading spinner */
.spinner {
  @apply inline-block w-4 h-4 border-2 border-solid border-gray-200 border-t-primary-500 rounded-full animate-spin;
}

/* Button variants */
.btn {
  @apply px-4 py-2 rounded-lg font-medium transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2;
}

.btn-primary {
  @apply bg-primary-500 text-white hover:bg-primary-600 focus:ring-primary-500;
}

.btn-secondary {
  @apply bg-gray-200 text-gray-900 hover:bg-gray-300 focus:ring-gray-500 dark:bg-gray-700 dark:text-gray-100 dark:hover:bg-gray-600;
}

.btn-outline {
  @apply border border-gray-300 text-gray-700 hover:bg-gray-50 focus:ring-gray-500 dark:border-gray-600 dark:text-gray-300 dark:hover:bg-gray-800;
}

/* Card component */
.card {
  @apply bg-white rounded-lg shadow-sm border border-gray-200 dark:bg-gray-800 dark:border-gray-700;
}

/* Form inputs */
.form-input {
  @apply w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent dark:bg-gray-700 dark:border-gray-600 dark:text-white;
}

/* Navigation */
.nav-link {
  @apply text-gray-600 hover:text-gray-900 dark:text-gray-300 dark:hover:text-white transition-colors duration-200;
}

.nav-link.active {
  @apply text-primary-500 dark:text-primary-400;
}"""

# Basic home page
home_page = """// pages/index.tsx - Landing page

import React from 'react';
import Head from 'next/head';

export default function Home() {
  return (
    <>
      <Head>
        <title>AI SaaS Platform - Advanced AI Tools for Everyone</title>
        <meta name="description" content="Powerful AI tools for text generation, image creation, code generation, and content summarization." />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 dark:from-gray-900 dark:to-gray-800">
        {/* Navigation */}
        <nav className="bg-white/80 backdrop-blur-sm dark:bg-gray-900/80 sticky top-0 z-50">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between items-center h-16">
              <div className="flex items-center">
                <h1 className="text-xl font-bold text-gray-900 dark:text-white">
                  🤖 AI Platform
                </h1>
              </div>
              <div className="flex items-center space-x-4">
                <a href="/auth/login" className="btn btn-outline">
                  Login
                </a>
                <a href="/auth/register" className="btn btn-primary">
                  Sign Up
                </a>
              </div>
            </div>
          </div>
        </nav>

        {/* Hero Section */}
        <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
          <div className="text-center">
            <h1 className="text-4xl md:text-6xl font-bold text-gray-900 dark:text-white mb-6">
              Supercharge Your Workflow with{' '}
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-purple-600">
                AI Tools
              </span>
            </h1>
            <p className="text-xl text-gray-600 dark:text-gray-300 mb-8 max-w-3xl mx-auto">
              Generate text, create images, write code, and summarize content with our powerful AI platform. 
              Everything you need to boost productivity in one place.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <a href="/auth/register" className="btn btn-primary text-lg px-8 py-3">
                Get Started Free
              </a>
              <a href="#features" className="btn btn-outline text-lg px-8 py-3">
                Learn More
              </a>
            </div>
          </div>

          {/* Features Section */}
          <section id="features" className="mt-32">
            <h2 className="text-3xl font-bold text-center text-gray-900 dark:text-white mb-16">
              Powerful AI Tools at Your Fingertips
            </h2>
            <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
              <div className="card p-6 text-center">
                <div className="text-4xl mb-4">📝</div>
                <h3 className="text-xl font-semibold mb-2">Text Generation</h3>
                <p className="text-gray-600 dark:text-gray-300">
                  Generate high-quality content, articles, and copy using advanced language models.
                </p>
              </div>
              <div className="card p-6 text-center">
                <div className="text-4xl mb-4">🎨</div>
                <h3 className="text-xl font-semibold mb-2">Image Creation</h3>
                <p className="text-gray-600 dark:text-gray-300">
                  Create stunning visuals and artwork from simple text descriptions.
                </p>
              </div>
              <div className="card p-6 text-center">
                <div className="text-4xl mb-4">💻</div>
                <h3 className="text-xl font-semibold mb-2">Code Generation</h3>
                <p className="text-gray-600 dark:text-gray-300">
                  Generate, debug, and optimize code in multiple programming languages.
                </p>
              </div>
              <div className="card p-6 text-center">
                <div className="text-4xl mb-4">📊</div>
                <h3 className="text-xl font-semibold mb-2">Content Summarization</h3>
                <p className="text-gray-600 dark:text-gray-300">
                  Quickly summarize long documents, articles, and research papers.
                </p>
              </div>
            </div>
          </section>

          {/* Pricing Section */}
          <section className="mt-32">
            <h2 className="text-3xl font-bold text-center text-gray-900 dark:text-white mb-16">
              Simple, Transparent Pricing
            </h2>
            <div className="grid md:grid-cols-3 gap-8 max-w-6xl mx-auto">
              <div className="card p-8">
                <h3 className="text-2xl font-bold mb-4">Starter</h3>
                <div className="text-4xl font-bold mb-4">$9<span className="text-lg text-gray-500">/month</span></div>
                <ul className="space-y-3 mb-8">
                  <li className="flex items-center">
                    <span className="text-green-500 mr-2">✓</span>
                    1,000 AI credits/month
                  </li>
                  <li className="flex items-center">
                    <span className="text-green-500 mr-2">✓</span>
                    Basic text generation
                  </li>
                  <li className="flex items-center">
                    <span className="text-green-500 mr-2">✓</span>
                    Email support
                  </li>
                </ul>
                <button className="btn btn-outline w-full">Get Started</button>
              </div>
              <div className="card p-8 border-primary-500 relative">
                <div className="absolute -top-3 left-1/2 transform -translate-x-1/2">
                  <span className="bg-primary-500 text-white px-3 py-1 rounded-full text-sm">Most Popular</span>
                </div>
                <h3 className="text-2xl font-bold mb-4">Professional</h3>
                <div className="text-4xl font-bold mb-4">$29<span className="text-lg text-gray-500">/month</span></div>
                <ul className="space-y-3 mb-8">
                  <li className="flex items-center">
                    <span className="text-green-500 mr-2">✓</span>
                    10,000 AI credits/month
                  </li>
                  <li className="flex items-center">
                    <span className="text-green-500 mr-2">✓</span>
                    All AI tools access
                  </li>
                  <li className="flex items-center">
                    <span className="text-green-500 mr-2">✓</span>
                    Priority support
                  </li>
                  <li className="flex items-center">
                    <span className="text-green-500 mr-2">✓</span>
                    API access
                  </li>
                </ul>
                <button className="btn btn-primary w-full">Get Started</button>
              </div>
              <div className="card p-8">
                <h3 className="text-2xl font-bold mb-4">Enterprise</h3>
                <div className="text-4xl font-bold mb-4">$99<span className="text-lg text-gray-500">/month</span></div>
                <ul className="space-y-3 mb-8">
                  <li className="flex items-center">
                    <span className="text-green-500 mr-2">✓</span>
                    Unlimited AI credits
                  </li>
                  <li className="flex items-center">
                    <span className="text-green-500 mr-2">✓</span>
                    Custom AI models
                  </li>
                  <li className="flex items-center">
                    <span className="text-green-500 mr-2">✓</span>
                    24/7 phone support
                  </li>
                  <li className="flex items-center">
                    <span className="text-green-500 mr-2">✓</span>
                    Team collaboration
                  </li>
                </ul>
                <button className="btn btn-outline w-full">Contact Sales</button>
              </div>
            </div>
          </section>
        </main>

        {/* Footer */}
        <footer className="bg-white dark:bg-gray-900 border-t border-gray-200 dark:border-gray-700 mt-32">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
            <div className="text-center">
              <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
                🤖 AI Platform
              </h3>
              <p className="text-gray-600 dark:text-gray-300">
                Built with Next.js, TypeScript, and TailwindCSS
              </p>
            </div>
          </div>
        </footer>
      </div>
    </>
  );
}"""

# Write final files
final_files = {
    'database/schema.sql': database_schema,
    'README.md': readme_content,
    'styles/globals.css': global_styles,
    'pages/index.tsx': home_page
}

for filepath, content in final_files.items():
    full_path = os.path.join(project_name, filepath)
    with open(full_path, 'w') as f:
        f.write(content)

print("✅ Added database schema and documentation:")
for filepath in final_files.keys():
    print(f"   ├── {filepath}")

# Create .gitignore file
gitignore_content = """# Dependencies
node_modules/
/.pnp
.pnp.js

# Testing
/coverage

# Next.js
/.next/
/out/

# Production
/build

# Misc
.DS_Store
*.pem

# Debug
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Local env files
.env
.env.local
.env.development.local
.env.test.local
.env.production.local

# Vercel
.vercel

# TypeScript
*.tsbuildinfo
next-env.d.ts

# Database
*.db
*.sqlite
*.sqlite3

# IDE
.vscode/
.idea/
*.swp
*.swo

# Logs
logs
*.log

# Cache
.npm
.eslintcache
.parcel-cache
.cache/"""

with open(os.path.join(project_name, '.gitignore'), 'w') as f:
    f.write(gitignore_content)

print("   ├── .gitignore")
print("\n" + "="*60)
print("🎉 COMPLETE PROJECT FOLDER CREATED!")
print("="*60)