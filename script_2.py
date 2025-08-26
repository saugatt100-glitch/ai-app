# Add TypeScript types and utilities

# Types definitions
types_content = """// types/index.ts - Type definitions for the AI SaaS platform

export interface User {
  id: string;
  email: string;
  name: string;
  role: 'user' | 'admin';
  subscription: 'Starter' | 'Professional' | 'Enterprise';
  createdAt: string;
  totalUsage: number;
}

export interface AuthTokens {
  accessToken: string;
  refreshToken: string;
}

export interface LoginCredentials {
  email: string;
  password: string;
  rememberMe?: boolean;
}

export interface RegisterData {
  name: string;
  email: string;
  password: string;
  confirmPassword: string;
}

export interface AITool {
  id: string;
  name: string;
  description: string;
  icon: string;
  category: string;
}

export interface UsageStats {
  textGeneration: number;
  imageGeneration: number;
  codeGeneration: number;
  summarization: number;
}

export interface PricingTier {
  name: string;
  price: string;
  period: string;
  popular?: boolean;
  features: string[];
  limitations: {
    textGeneration: number; // -1 for unlimited
    imageGeneration: number;
    codeGeneration: number;
    summarization: number;
  };
}

export interface AIResponse {
  success: boolean;
  data?: any;
  error?: string;
  usage?: {
    tokensUsed: number;
    remainingCredits: number;
  };
}

export interface AdminStats {
  totalUsers: number;
  activeUsers: number;
  totalAPIUsage: number;
  revenueThisMonth: number;
  userGrowth: number;
  usageByTool: Record<string, number>;
}"""

# Auth utilities
auth_utils = """// lib/auth.ts - Authentication utilities and JWT handling

import jwt from 'jsonwebtoken';
import bcrypt from 'bcryptjs';
import { User, AuthTokens } from '@/types';

const JWT_SECRET = process.env.JWT_SECRET || 'fallback-secret-key';
const JWT_REFRESH_SECRET = process.env.JWT_REFRESH_SECRET || 'fallback-refresh-key';

export class AuthUtils {
  static async hashPassword(password: string): Promise<string> {
    return bcrypt.hash(password, 12);
  }

  static async verifyPassword(password: string, hashedPassword: string): Promise<boolean> {
    return bcrypt.compare(password, hashedPassword);
  }

  static generateTokens(user: Omit<User, 'totalUsage' | 'createdAt'>): AuthTokens {
    const accessToken = jwt.sign(
      { 
        userId: user.id, 
        email: user.email, 
        role: user.role,
        subscription: user.subscription 
      },
      JWT_SECRET,
      { expiresIn: '15m' }
    );

    const refreshToken = jwt.sign(
      { userId: user.id },
      JWT_REFRESH_SECRET,
      { expiresIn: '7d' }
    );

    return { accessToken, refreshToken };
  }

  static verifyAccessToken(token: string): any {
    try {
      return jwt.verify(token, JWT_SECRET);
    } catch (error) {
      throw new Error('Invalid access token');
    }
  }

  static verifyRefreshToken(token: string): any {
    try {
      return jwt.verify(token, JWT_REFRESH_SECRET);
    } catch (error) {
      throw new Error('Invalid refresh token');
    }
  }

  static extractTokenFromHeader(authHeader: string | undefined): string | null {
    if (!authHeader || !authHeader.startsWith('Bearer ')) {
      return null;
    }
    return authHeader.substring(7);
  }
}

// Mock database functions (replace with actual database calls)
export class MockDB {
  private static users: User[] = [
    {
      id: '1',
      email: 'admin@aiplatform.com',
      name: 'Admin User',
      role: 'admin',
      subscription: 'Enterprise',
      createdAt: '2024-01-15T00:00:00Z',
      totalUsage: 15420
    },
    {
      id: '2', 
      email: 'user@example.com',
      name: 'John Doe',
      role: 'user',
      subscription: 'Professional',
      createdAt: '2024-03-20T00:00:00Z',
      totalUsage: 8750
    }
  ];

  private static passwords: Record<string, string> = {
    'admin@aiplatform.com': '$2a$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LsEaGb.xjmtNOhgka', // password: admin123
    'user@example.com': '$2a$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LsEaGb.xjmtNOhgka' // password: user123
  };

  static async findUserByEmail(email: string): Promise<User | null> {
    return this.users.find(user => user.email === email) || null;
  }

  static async findUserById(id: string): Promise<User | null> {
    return this.users.find(user => user.id === id) || null;
  }

  static async getPasswordHash(email: string): Promise<string | null> {
    return this.passwords[email] || null;
  }

  static async createUser(userData: Omit<User, 'id' | 'createdAt' | 'totalUsage'> & { password: string }): Promise<User> {
    const newUser: User = {
      id: (this.users.length + 1).toString(),
      email: userData.email,
      name: userData.name,
      role: userData.role,
      subscription: userData.subscription,
      createdAt: new Date().toISOString(),
      totalUsage: 0
    };
    
    this.users.push(newUser);
    this.passwords[userData.email] = userData.password;
    
    return newUser;
  }

  static async getAllUsers(): Promise<User[]> {
    return this.users;
  }
}"""

# Middleware
middleware_content = """// middleware.ts - Next.js middleware for route protection

import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';
import jwt from 'jsonwebtoken';

const JWT_SECRET = process.env.JWT_SECRET || 'fallback-secret-key';

// Routes that require authentication
const protectedRoutes = ['/dashboard', '/admin', '/profile'];
const adminRoutes = ['/admin'];
const authRoutes = ['/auth/login', '/auth/register'];

export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;
  
  // Check if the route requires authentication
  const isProtectedRoute = protectedRoutes.some(route => pathname.startsWith(route));
  const isAdminRoute = adminRoutes.some(route => pathname.startsWith(route));
  const isAuthRoute = authRoutes.some(route => pathname.startsWith(route));
  
  // Get token from cookies or headers
  const token = request.cookies.get('accessToken')?.value || 
                request.headers.get('authorization')?.replace('Bearer ', '');

  // If accessing protected route without token, redirect to login
  if (isProtectedRoute && !token) {
    const loginUrl = new URL('/auth/login', request.url);
    loginUrl.searchParams.set('redirect', pathname);
    return NextResponse.redirect(loginUrl);
  }

  // If token exists, verify it
  if (token) {
    try {
      const decoded = jwt.verify(token, JWT_SECRET) as any;
      
      // If user is authenticated and trying to access auth routes, redirect to dashboard
      if (isAuthRoute) {
        return NextResponse.redirect(new URL('/dashboard', request.url));
      }
      
      // Check admin access for admin routes
      if (isAdminRoute && decoded.role !== 'admin') {
        return NextResponse.redirect(new URL('/dashboard', request.url));
      }
      
    } catch (error) {
      // Invalid token - redirect to login if accessing protected route
      if (isProtectedRoute) {
        const loginUrl = new URL('/auth/login', request.url);
        loginUrl.searchParams.set('redirect', pathname);
        return NextResponse.redirect(loginUrl);
      }
    }
  }

  return NextResponse.next();
}

export const config = {
  matcher: [
    '/dashboard/:path*',
    '/admin/:path*',
    '/profile/:path*',
    '/auth/:path*'
  ]
};"""

# Write these files
files_to_create = {
    'types/index.ts': types_content,
    'lib/auth.ts': auth_utils,
    'middleware.ts': middleware_content
}

for filepath, content in files_to_create.items():
    full_path = os.path.join(project_name, filepath)
    with open(full_path, 'w') as f:
        f.write(content)

print("✅ Added TypeScript utilities:")
for filepath in files_to_create.keys():
    print(f"   ├── {filepath}")