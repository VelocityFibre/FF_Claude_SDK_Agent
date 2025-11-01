/**
 * Database AI Agent API Route
 *
 * Path: app/api/agent/chat/route.ts
 *
 * Handles communication between Next.js frontend and Python backend
 */

import { NextRequest, NextResponse } from 'next/server';

// Backend URL - set in environment variables
const AGENT_BACKEND_URL = process.env.AGENT_BACKEND_URL || 'http://localhost:8000';

// Optional: API key for backend authentication
const AGENT_API_KEY = process.env.AGENT_API_KEY;

interface ChatRequest {
  message: string;
  context?: Record<string, any>;
}

interface ChatResponse {
  response: string;
  success: boolean;
  error?: string;
}

export async function POST(req: NextRequest) {
  try {
    // Parse request body
    const body: ChatRequest = await req.json();
    const { message, context = {} } = body;

    // Validate input
    if (!message || typeof message !== 'string') {
      return NextResponse.json(
        { error: 'Message is required', success: false },
        { status: 400 }
      );
    }

    if (message.length > 5000) {
      return NextResponse.json(
        { error: 'Message too long (max 5000 characters)', success: false },
        { status: 400 }
      );
    }

    // Get user info from session/auth (if you have auth)
    // const session = await getServerSession(authOptions);
    // const userId = session?.user?.id;

    // Prepare headers for backend request
    const headers: HeadersInit = {
      'Content-Type': 'application/json',
    };

    // Add API key if configured
    if (AGENT_API_KEY) {
      headers['Authorization'] = `Bearer ${AGENT_API_KEY}`;
    }

    // Add user context
    const enrichedContext = {
      ...context,
      // userId, // If you have auth
      timestamp: new Date().toISOString(),
      userAgent: req.headers.get('user-agent') || 'unknown',
    };

    // Call Python backend
    const backendResponse = await fetch(`${AGENT_BACKEND_URL}/agent/chat`, {
      method: 'POST',
      headers,
      body: JSON.stringify({
        message,
        context: enrichedContext,
      }),
      // Set timeout to 30 seconds
      signal: AbortSignal.timeout(30000),
    });

    if (!backendResponse.ok) {
      const errorText = await backendResponse.text();
      console.error('Backend error:', errorText);

      return NextResponse.json(
        {
          error: `Backend error: ${backendResponse.status}`,
          success: false,
        },
        { status: backendResponse.status }
      );
    }

    // Parse backend response
    const data: ChatResponse = await backendResponse.json();

    // Log query for analytics (optional)
    console.log('[Agent Query]', {
      message: message.substring(0, 100),
      context: context.page || 'general',
      responseLength: data.response?.length || 0,
      timestamp: new Date().toISOString(),
    });

    // Return response
    return NextResponse.json({
      response: data.response,
      success: true,
    });

  } catch (error) {
    console.error('API route error:', error);

    // Handle timeout
    if (error instanceof Error && error.name === 'AbortError') {
      return NextResponse.json(
        {
          error: 'Request timed out. Please try a simpler query.',
          success: false,
        },
        { status: 504 }
      );
    }

    // Handle other errors
    return NextResponse.json(
      {
        error: error instanceof Error ? error.message : 'Internal server error',
        success: false,
      },
      { status: 500 }
    );
  }
}

// Optional: Health check endpoint
export async function GET() {
  try {
    // Check if backend is reachable
    const response = await fetch(`${AGENT_BACKEND_URL}/health`, {
      signal: AbortSignal.timeout(5000),
    });

    if (response.ok) {
      return NextResponse.json({
        status: 'healthy',
        backend: 'connected',
        timestamp: new Date().toISOString(),
      });
    } else {
      return NextResponse.json(
        {
          status: 'degraded',
          backend: 'unreachable',
          timestamp: new Date().toISOString(),
        },
        { status: 503 }
      );
    }
  } catch (error) {
    return NextResponse.json(
      {
        status: 'unhealthy',
        backend: 'error',
        error: error instanceof Error ? error.message : 'Unknown error',
        timestamp: new Date().toISOString(),
      },
      { status: 503 }
    );
  }
}
