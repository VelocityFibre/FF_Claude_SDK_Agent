#!/bin/bash
# WA Monitor Deployment Script
# Deploys API endpoint and React components to FibreFlow

set -e  # Exit on error

echo "================================================"
echo "WA Monitor Deployment Script"
echo "================================================"
echo ""

# Configuration
SERVER_USER="louis"
SERVER_HOST="100.96.203.105"
SERVER_PASSWORD="VeloAdmin2025!"
APP_PATH="/home/louis/apps/fibreflow"

echo "Deploying to: $SERVER_USER@$SERVER_HOST:$APP_PATH"
echo ""

# Step 1: Deploy API Endpoint
echo "Step 1: Deploying /api/foto/evaluations endpoint..."
sshpass -p "$SERVER_PASSWORD" ssh -o StrictHostKeyChecking=no $SERVER_USER@$SERVER_HOST << 'ENDSSH'
cd /home/louis/apps/fibreflow

# Create evaluations API directory
mkdir -p app/api/foto/evaluations

# Create route.ts
cat > app/api/foto/evaluations/route.ts << 'ENDFILE'
/**
 * GET /api/foto/evaluations
 * Returns all foto evaluations with optional filtering
 */

import { NextRequest, NextResponse } from 'next/server';
import { sql } from '@/lib/neon';
import { log } from '@/lib/logger';

export const runtime = 'nodejs';
export const dynamic = 'force-dynamic';

export async function GET(request: NextRequest) {
  const startTime = Date.now();

  try {
    log.info('FotoEvaluations', 'Fetching all evaluations');

    const searchParams = request.nextUrl.searchParams;
    const feedbackSent = searchParams.get('feedback_sent');
    const status = searchParams.get('status');
    const limit = parseInt(searchParams.get('limit') || '100');
    const offset = parseInt(searchParams.get('offset') || '0');

    const conditions: string[] = [];
    const params: any[] = [];
    let paramIndex = 1;

    if (feedbackSent !== null) {
      conditions.push(`feedback_sent = $${paramIndex++}`);
      params.push(feedbackSent === 'true');
    }

    if (status) {
      conditions.push(`overall_status = $${paramIndex++}`);
      params.push(status);
    }

    const whereClause = conditions.length > 0
      ? `WHERE ${conditions.join(' AND ')}`
      : '';

    const query = `
      SELECT
        dr_number,
        overall_status,
        average_score,
        total_steps,
        passed_steps,
        step_results,
        markdown_report,
        feedback_sent,
        evaluation_date,
        created_at,
        updated_at
      FROM foto_evaluations
      ${whereClause}
      ORDER BY evaluation_date DESC
      LIMIT $${paramIndex++}
      OFFSET $${paramIndex}
    `;

    params.push(limit, offset);

    const result = await sql(query, params);
    const evaluations = result.rows;

    const countQuery = `
      SELECT COUNT(*) as total
      FROM foto_evaluations
      ${whereClause}
    `;

    const countResult = await sql(
      countQuery,
      params.slice(0, params.length - 2)
    );
    const total = parseInt(countResult.rows[0].total);

    const duration = Date.now() - startTime;

    log.info('FotoEvaluations', `Retrieved ${evaluations.length} evaluations in ${duration}ms`);

    return NextResponse.json({
      success: true,
      data: evaluations,
      meta: {
        total,
        limit,
        offset,
        returned: evaluations.length
      },
      duration_ms: duration
    });

  } catch (error: any) {
    const duration = Date.now() - startTime;

    log.error('FotoEvaluations', 'Failed to fetch evaluations', {
      error: error.message,
      stack: error.stack,
      duration_ms: duration
    });

    return NextResponse.json({
      success: false,
      error: 'Failed to fetch evaluations',
      message: error.message,
      duration_ms: duration
    }, { status: 500 });
  }
}
ENDFILE

echo "✅ API endpoint created"
ENDSSH

echo ""
echo "Step 2: Rebuilding Next.js application..."
sshpass -p "$SERVER_PASSWORD" ssh -o StrictHostKeyChecking=no $SERVER_USER@$SERVER_HOST << 'ENDSSH'
cd /home/louis/apps/fibreflow

# Build the application
echo "Building Next.js app (this may take a few minutes)..."
npm run build

echo "✅ Build complete"
ENDSSH

echo ""
echo "Step 3: Restarting Next.js server..."
sshpass -p "$SERVER_PASSWORD" ssh -o StrictHostKeyChecking=no $SERVER_USER@$SERVER_HOST << 'ENDSSH'
# Kill existing Next.js process
pkill -f "next-server" || true
sleep 3

# Start Next.js
cd /home/louis/apps/fibreflow
NODE_ENV=production nohup npm run start > /tmp/nextjs_restart.log 2>&1 &

sleep 5

# Check if started
if ps aux | grep -q "[n]ext-server"; then
    echo "✅ Next.js server restarted"
else
    echo "⚠️  Next.js may not have started. Check /tmp/nextjs_restart.log"
fi
ENDSSH

echo ""
echo "Step 4: Testing API endpoint..."
sleep 3
response=$(curl -s "http://$SERVER_HOST:3005/api/foto/evaluations?limit=1")
if echo "$response" | grep -q '"success":true'; then
    echo "✅ API endpoint is working!"
    echo "$response" | jq '.meta // {}'
else
    echo "⚠️  API endpoint may not be working correctly"
    echo "$response" | head -100
fi

echo ""
echo "Step 5: Checking WhatsApp Sender service..."
wa_health=$(curl -s "http://$SERVER_HOST:8081/health")
echo "$wa_health" | jq '.'

if echo "$wa_health" | grep -q '"connected":false'; then
    echo ""
    echo "⚠️  WARNING: WhatsApp phone is NOT paired!"
    echo "   Phone +27 71 155 8396 must be paired for feedback to work."
    echo ""
    echo "   To pair:"
    echo "   1. SSH to server: ssh $SERVER_USER@$SERVER_HOST"
    echo "   2. Get QR code: curl http://localhost:8081/qr"
    echo "   3. Scan with WhatsApp on phone +27 71 155 8396"
    echo ""
fi

echo ""
echo "================================================"
echo "Deployment Complete!"
echo "================================================"
echo ""
echo "✅ API Endpoint: http://$SERVER_HOST:3005/api/foto/evaluations"
echo "✅ Web Interface: https://app.fibreflow.app/foto-reviews"
echo "✅ WA Monitor: https://app.fibreflow.app/wa-monitor"
echo ""
echo "Next Steps:"
echo "1. Open https://app.fibreflow.app/foto-reviews to see evaluations"
echo "2. Pair WhatsApp phone if not already done (see warning above)"
echo "3. Test feedback sending on a pending evaluation"
echo ""
echo "For complete documentation, see DEPLOYMENT_GUIDE.md"
echo "================================================"
