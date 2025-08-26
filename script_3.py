# Add all API routes

# Login API
login_api = """// pages/api/auth/login.ts - Login API endpoint

import type { NextApiRequest, NextApiResponse } from 'next';
import { AuthUtils, MockDB } from '@/lib/auth';
import { LoginCredentials, AuthTokens } from '@/types';

type LoginResponse = {
  success: boolean;
  data?: {
    user: any;
    tokens: AuthTokens;
  };
  error?: string;
};

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse<LoginResponse>
) {
  if (req.method !== 'POST') {
    return res.status(405).json({
      success: false,
      error: 'Method not allowed'
    });
  }

  try {
    const { email, password }: LoginCredentials = req.body;

    if (!email || !password) {
      return res.status(400).json({
        success: false,
        error: 'Email and password are required'
      });
    }

    // Find user by email
    const user = await MockDB.findUserByEmail(email);
    if (!user) {
      return res.status(401).json({
        success: false,
        error: 'Invalid credentials'
      });
    }

    // Verify password
    const passwordHash = await MockDB.getPasswordHash(email);
    if (!passwordHash || !(await AuthUtils.verifyPassword(password, passwordHash))) {
      return res.status(401).json({
        success: false,
        error: 'Invalid credentials'
      });
    }

    // Generate tokens
    const tokens = AuthUtils.generateTokens(user);

    // Remove sensitive information from user object
    const { totalUsage, createdAt, ...safeUser } = user;

    res.status(200).json({
      success: true,
      data: {
        user: safeUser,
        tokens
      }
    });

  } catch (error) {
    console.error('Login error:', error);
    res.status(500).json({
      success: false,
      error: 'Internal server error'
    });
  }
}"""

# Register API
register_api = """// pages/api/auth/register.ts - Registration API endpoint

import type { NextApiRequest, NextApiResponse } from 'next';
import { AuthUtils, MockDB } from '@/lib/auth';
import { RegisterData, AuthTokens } from '@/types';

type RegisterResponse = {
  success: boolean;
  data?: {
    user: any;
    tokens: AuthTokens;
  };
  error?: string;
};

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse<RegisterResponse>
) {
  if (req.method !== 'POST') {
    return res.status(405).json({
      success: false,
      error: 'Method not allowed'
    });
  }

  try {
    const { name, email, password, confirmPassword }: RegisterData = req.body;

    // Validation
    if (!name || !email || !password || !confirmPassword) {
      return res.status(400).json({
        success: false,
        error: 'All fields are required'
      });
    }

    if (password !== confirmPassword) {
      return res.status(400).json({
        success: false,
        error: 'Passwords do not match'
      });
    }

    if (password.length < 6) {
      return res.status(400).json({
        success: false,
        error: 'Password must be at least 6 characters long'
      });
    }

    // Check if user already exists
    const existingUser = await MockDB.findUserByEmail(email);
    if (existingUser) {
      return res.status(400).json({
        success: false,
        error: 'User already exists with this email'
      });
    }

    // Hash password
    const hashedPassword = await AuthUtils.hashPassword(password);

    // Create user
    const newUser = await MockDB.createUser({
      name,
      email,
      role: 'user',
      subscription: 'Starter',
      password: hashedPassword
    });

    // Generate tokens
    const tokens = AuthUtils.generateTokens(newUser);

    // Remove sensitive information
    const { totalUsage, createdAt, ...safeUser } = newUser;

    res.status(201).json({
      success: true,
      data: {
        user: safeUser,
        tokens
      }
    });

  } catch (error) {
    console.error('Registration error:', error);
    res.status(500).json({
      success: false,
      error: 'Internal server error'
    });
  }
}"""

# Text Generation API
text_generate_api = """// pages/api/ai/text-generate.ts - Text generation API endpoint

import type { NextApiRequest, NextApiResponse } from 'next';
import { AuthUtils } from '@/lib/auth';
import { AIResponse } from '@/types';

// Mock AI responses for demonstration
const mockTextResponses = [
  "Here's a well-crafted response based on your prompt. This AI-generated content demonstrates the capabilities of our text generation tool. The system can produce various types of content including articles, emails, marketing copy, and creative writing pieces.",
  "Our advanced AI text generator creates human-like content tailored to your specific needs. Whether you're writing blog posts, product descriptions, or social media content, this tool helps streamline your content creation process.",
  "This is an example of AI-generated text that showcases natural language processing capabilities. The content is coherent, contextually relevant, and maintains a professional tone throughout the response."
];

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse<AIResponse>
) {
  if (req.method !== 'POST') {
    return res.status(405).json({
      success: false,
      error: 'Method not allowed'
    });
  }

  try {
    // Verify authentication
    const token = AuthUtils.extractTokenFromHeader(req.headers.authorization);
    if (!token) {
      return res.status(401).json({
        success: false,
        error: 'Authentication required'
      });
    }

    const decoded = AuthUtils.verifyAccessToken(token);
    const { prompt, maxLength = 150 } = req.body;

    if (!prompt) {
      return res.status(400).json({
        success: false,
        error: 'Prompt is required'
      });
    }

    // Simulate processing delay
    await new Promise(resolve => setTimeout(resolve, 2000));

    // Select a random mock response
    const randomResponse = mockTextResponses[Math.floor(Math.random() * mockTextResponses.length)];
    
    // Truncate response based on maxLength
    const truncatedResponse = randomResponse.length > maxLength 
      ? randomResponse.substring(0, maxLength) + '...'
      : randomResponse;

    // Simulate usage tracking
    const tokensUsed = Math.floor(truncatedResponse.length / 4);
    const remainingCredits = decoded.subscription === 'Enterprise' ? -1 : Math.max(0, 1000 - tokensUsed);

    res.status(200).json({
      success: true,
      data: {
        text: truncatedResponse,
        prompt: prompt
      },
      usage: {
        tokensUsed,
        remainingCredits
      }
    });

  } catch (error) {
    console.error('Text generation error:', error);
    res.status(500).json({
      success: false,
      error: 'Internal server error'
    });
  }
}"""

# Image Generation API
image_generate_api = """// pages/api/ai/image-generate.ts - Image generation API endpoint

import type { NextApiRequest, NextApiResponse } from 'next';
import { AuthUtils } from '@/lib/auth';
import { AIResponse } from '@/types';

// Mock image URLs for demonstration
const mockImageUrls = [
  'https://images.unsplash.com/photo-1547036967-23d11aacaee0?w=512&h=512&fit=crop',
  'https://images.unsplash.com/photo-1518837695005-2083093ee35b?w=512&h=512&fit=crop',
  'https://images.unsplash.com/photo-1501594907352-04cda38ebc29?w=512&h=512&fit=crop',
  'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=512&h=512&fit=crop',
  'https://images.unsplash.com/photo-1519904981063-b0cf448d479e?w=512&h=512&fit=crop'
];

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse<AIResponse>
) {
  if (req.method !== 'POST') {
    return res.status(405).json({
      success: false,
      error: 'Method not allowed'
    });
  }

  try {
    // Verify authentication
    const token = AuthUtils.extractTokenFromHeader(req.headers.authorization);
    if (!token) {
      return res.status(401).json({
        success: false,
        error: 'Authentication required'
      });
    }

    const decoded = AuthUtils.verifyAccessToken(token);
    const { prompt, style = 'realistic', size = '512x512' } = req.body;

    if (!prompt) {
      return res.status(400).json({
        success: false,
        error: 'Prompt is required'
      });
    }

    // Simulate processing delay (image generation typically takes longer)
    await new Promise(resolve => setTimeout(resolve, 4000));

    // Select random mock images
    const numberOfImages = Math.min(4, Math.floor(Math.random() * 3) + 1);
    const selectedImages = mockImageUrls
      .sort(() => 0.5 - Math.random())
      .slice(0, numberOfImages)
      .map((url, index) => ({
        id: `img_${Date.now()}_${index}`,
        url,
        prompt: prompt,
        style: style,
        size: size
      }));

    // Simulate usage tracking
    const tokensUsed = numberOfImages * 100; // 100 tokens per image
    const remainingCredits = decoded.subscription === 'Enterprise' ? -1 : Math.max(0, 1000 - tokensUsed);

    res.status(200).json({
      success: true,
      data: {
        images: selectedImages,
        prompt: prompt,
        style: style,
        size: size
      },
      usage: {
        tokensUsed,
        remainingCredits
      }
    });

  } catch (error) {
    console.error('Image generation error:', error);
    res.status(500).json({
      success: false,
      error: 'Internal server error'
    });
  }
}"""

# Admin users API
admin_users_api = """// pages/api/admin/users.ts - Admin user management API

import type { NextApiRequest, NextApiResponse } from 'next';
import { AuthUtils, MockDB } from '@/lib/auth';
import { User } from '@/types';

type UsersResponse = {
  success: boolean;
  data?: {
    users: User[];
    pagination: {
      total: number;
      page: number;
      limit: number;
      totalPages: number;
    };
  };
  error?: string;
};

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse<UsersResponse>
) {
  try {
    // Verify admin authentication
    const token = AuthUtils.extractTokenFromHeader(req.headers.authorization);
    if (!token) {
      return res.status(401).json({
        success: false,
        error: 'Authentication required'
      });
    }

    const decoded = AuthUtils.verifyAccessToken(token);
    if (decoded.role !== 'admin') {
      return res.status(403).json({
        success: false,
        error: 'Admin access required'
      });
    }

    if (req.method === 'GET') {
      // Get all users with pagination
      const page = parseInt(req.query.page as string) || 1;
      const limit = parseInt(req.query.limit as string) || 10;
      const search = req.query.search as string || '';

      const allUsers = await MockDB.getAllUsers();
      
      // Filter users based on search
      const filteredUsers = search 
        ? allUsers.filter(user => 
            user.name.toLowerCase().includes(search.toLowerCase()) ||
            user.email.toLowerCase().includes(search.toLowerCase())
          )
        : allUsers;

      // Paginate results
      const startIndex = (page - 1) * limit;
      const endIndex = startIndex + limit;
      const paginatedUsers = filteredUsers.slice(startIndex, endIndex);

      return res.status(200).json({
        success: true,
        data: {
          users: paginatedUsers,
          pagination: {
            total: filteredUsers.length,
            page,
            limit,
            totalPages: Math.ceil(filteredUsers.length / limit)
          }
        }
      });

    } else {
      return res.status(405).json({
        success: false,
        error: 'Method not allowed'
      });
    }

  } catch (error) {
    console.error('Admin users API error:', error);
    res.status(500).json({
      success: false,
      error: 'Internal server error'
    });
  }
}"""

# Admin analytics API
admin_analytics_api = """// pages/api/admin/analytics.ts - Admin analytics API

import type { NextApiRequest, NextApiResponse } from 'next';
import { AuthUtils } from '@/lib/auth';
import { AdminStats } from '@/types';

type AnalyticsResponse = {
  success: boolean;
  data?: AdminStats;
  error?: string;
};

// Mock analytics data
const mockAnalytics: AdminStats = {
  totalUsers: 1247,
  activeUsers: 892,
  totalAPIUsage: 45678,
  revenueThisMonth: 12450,
  userGrowth: 23.5,
  usageByTool: {
    'text-generation': 18500,
    'image-generation': 12300,
    'code-generation': 8900,
    'summarization': 5978
  }
};

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse<AnalyticsResponse>
) {
  if (req.method !== 'GET') {
    return res.status(405).json({
      success: false,
      error: 'Method not allowed'
    });
  }

  try {
    // Verify admin authentication
    const token = AuthUtils.extractTokenFromHeader(req.headers.authorization);
    if (!token) {
      return res.status(401).json({
        success: false,
        error: 'Authentication required'
      });
    }

    const decoded = AuthUtils.verifyAccessToken(token);
    if (decoded.role !== 'admin') {
      return res.status(403).json({
        success: false,
        error: 'Admin access required'
      });
    }

    res.status(200).json({
      success: true,
      data: mockAnalytics
    });

  } catch (error) {
    console.error('Analytics API error:', error);
    res.status(500).json({
      success: false,
      error: 'Internal server error'
    });
  }
}"""

# Write all API files
api_files = {
    'pages/api/auth/login.ts': login_api,
    'pages/api/auth/register.ts': register_api,
    'pages/api/ai/text-generate.ts': text_generate_api,
    'pages/api/ai/image-generate.ts': image_generate_api,
    'pages/api/admin/users.ts': admin_users_api,
    'pages/api/admin/analytics.ts': admin_analytics_api
}

for filepath, content in api_files.items():
    full_path = os.path.join(project_name, filepath)
    with open(full_path, 'w') as f:
        f.write(content)

print("✅ Added API routes:")
for filepath in api_files.keys():
    print(f"   ├── {filepath}")