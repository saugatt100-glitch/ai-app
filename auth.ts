// lib/auth.ts - Authentication utilities and JWT handling

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
}