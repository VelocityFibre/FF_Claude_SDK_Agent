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

    // Parse query parameters
    const searchParams = request.nextUrl.searchParams;
    const feedbackSent = searchParams.get('feedback_sent');
    const status = searchParams.get('status'); // PASS, PARTIAL, FAIL
    const limit = parseInt(searchParams.get('limit') || '100');
    const offset = parseInt(searchParams.get('offset') || '0');

    // Build WHERE clause
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

    // Query evaluations
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

    // Get total count
    const countQuery = `
      SELECT COUNT(*) as total
      FROM foto_evaluations
      ${whereClause}
    `;

    const countResult = await sql(
      countQuery,
      params.slice(0, params.length - 2) // Remove limit and offset
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

/**
 * GET /api/foto/evaluations/pending
 * Convenience endpoint for pending feedback
 */
export async function getPendingEvaluations() {
  try {
    const query = `
      SELECT
        dr_number,
        overall_status,
        average_score,
        total_steps,
        passed_steps,
        feedback_sent,
        evaluation_date
      FROM foto_evaluations
      WHERE feedback_sent = false
      ORDER BY evaluation_date DESC
    `;

    const result = await sql(query);

    return NextResponse.json({
      success: true,
      data: result.rows,
      count: result.rows.length
    });

  } catch (error: any) {
    log.error('FotoEvaluations', 'Failed to fetch pending evaluations', {
      error: error.message
    });

    return NextResponse.json({
      success: false,
      error: 'Failed to fetch pending evaluations',
      message: error.message
    }, { status: 500 });
  }
}
