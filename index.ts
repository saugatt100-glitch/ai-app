// types/index.ts - Type definitions for the AI SaaS platform

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
}