/**
 * Foto Reviews Dashboard Component
 * Review AI-generated feedback before sending to WhatsApp
 */

'use client';

import { useState, useEffect } from 'react';
import {
  Card,
  CardContent,
  Typography,
  Button,
  TextField,
  Box,
  Chip,
  Grid,
  Alert,
  CircularProgress,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextareaAutosize,
  Divider
} from '@mui/material';
import {
  Refresh as RefreshIcon,
  Check as CheckIcon,
  Close as CloseIcon,
  Edit as EditIcon,
  Send as SendIcon
} from '@mui/icons-material';

interface Evaluation {
  dr_number: string;
  overall_status: 'PASS' | 'PARTIAL' | 'FAIL';
  average_score: number;
  total_steps: number;
  passed_steps: number;
  step_results: Array<{
    score: number;
    passed: boolean;
    comment: string;
    step_name: string;
    step_label: string;
    step_number: number;
  }>;
  feedback_sent: boolean;
  evaluation_date: string;
}

export function FotoReviewsDashboard() {
  const [evaluations, setEvaluations] = useState<Evaluation[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedEval, setSelectedEval] = useState<Evaluation | null>(null);
  const [feedbackMessage, setFeedbackMessage] = useState('');
  const [isEditing, setIsEditing] = useState(false);
  const [sending, setSending] = useState(false);

  // Stats
  const stats = {
    pending: evaluations.filter(e => !e.feedback_sent).length,
    approved: 0, // Not tracking approval status yet
    rejected: 0, // Not tracking rejection status yet
    sent: evaluations.filter(e => e.feedback_sent).length
  };

  // Fetch evaluations
  const fetchEvaluations = async () => {
    setLoading(true);
    setError(null);

    try {
      const response = await fetch('/api/foto/evaluations?feedback_sent=false&limit=50');
      const data = await response.json();

      if (data.success) {
        setEvaluations(data.data);
      } else {
        setError(data.message || 'Failed to fetch evaluations');
      }
    } catch (err: any) {
      setError(err.message || 'Failed to fetch evaluations');
    } finally {
      setLoading(false);
    }
  };

  // Generate WhatsApp feedback message
  const generateFeedback = (eval: Evaluation): string => {
    const { overall_status, dr_number, average_score, passed_steps, total_steps, step_results } = eval;

    let emoji = '❌';
    let header = 'QA FAILED';
    if (overall_status === 'PASS') {
      emoji = '✅';
      header = 'QA PASSED';
    } else if (overall_status === 'PARTIAL') {
      emoji = '⚠️';
      header = 'QA PARTIAL PASS';
    }

    let message = `${emoji} *${header}*\nDR: ${dr_number}\n\n`;
    message += `📊 Overall Score: ${average_score}/10\n`;
    message += `✔️ Steps Passed: ${passed_steps}/${total_steps}\n\n`;

    // Add step details
    if (step_results && step_results.length > 0) {
      message += '*Detailed Results:*\n';
      step_results.slice(0, 5).forEach(step => {
        const stepEmoji = step.passed ? '✓' : '✗';
        message += `${stepEmoji} ${step.step_label}: ${step.score}/10\n`;
        if (step.comment && !step.passed) {
          // Truncate long comments
          const comment = step.comment.length > 100
            ? step.comment.substring(0, 97) + '...'
            : step.comment;
          message += `  ↳ ${comment}\n`;
        }
      });

      if (step_results.length > 5) {
        message += `\n_...and ${step_results.length - 5} more steps_\n`;
      }
    }

    // Add recommendations
    message += '\n*Recommendations:*\n';
    if (overall_status === 'PASS') {
      message += '✅ Good work! All quality standards met.\n';
    } else if (overall_status === 'PARTIAL') {
      message += '⚠️ Please review and address the noted issues.\n';
    } else {
      message += '❌ Significant issues found. Please rework and resubmit.\n';
    }

    return message;
  };

  // Handle review click
  const handleReview = (eval: Evaluation) => {
    setSelectedEval(eval);
    setFeedbackMessage(generateFeedback(eval));
    setIsEditing(false);
  };

  // Handle send feedback
  const handleSendFeedback = async () => {
    if (!selectedEval) return;

    setSending(true);

    try {
      const response = await fetch('/api/foto/feedback', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          dr_number: selectedEval.dr_number,
          message: feedbackMessage
        })
      });

      const data = await response.json();

      if (data.success) {
        // Update local state
        setEvaluations(prev =>
          prev.map(e =>
            e.dr_number === selectedEval.dr_number
              ? { ...e, feedback_sent: true }
              : e
          )
        );
        setSelectedEval(null);
        setFeedbackMessage('');
      } else {
        setError(data.message || 'Failed to send feedback');
      }
    } catch (err: any) {
      setError(err.message || 'Failed to send feedback');
    } finally {
      setSending(false);
    }
  };

  // Handle reject
  const handleReject = () => {
    setSelectedEval(null);
    setFeedbackMessage('');
  };

  // Initial load
  useEffect(() => {
    fetchEvaluations();
  }, []);

  // Filter evaluations
  const filteredEvaluations = evaluations.filter(e =>
    e.dr_number.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" sx={{ mb: 3 }}>
        Foto Reviews
      </Typography>

      {/* Stats */}
      <Grid container spacing={3} sx={{ mb: 3 }}>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Pending
              </Typography>
              <Typography variant="h4">{stats.pending}</Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Approved
              </Typography>
              <Typography variant="h4">{stats.approved}</Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Rejected
              </Typography>
              <Typography variant="h4">{stats.rejected}</Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Sent
              </Typography>
              <Typography variant="h4">{stats.sent}</Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Search and Actions */}
      <Box sx={{ mb: 3, display: 'flex', gap: 2 }}>
        <TextField
          fullWidth
          label="Search DR Number"
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          size="small"
        />
        <Button
          variant="outlined"
          startIcon={<RefreshIcon />}
          onClick={fetchEvaluations}
          disabled={loading}
        >
          Refresh
        </Button>
      </Box>

      {/* Error */}
      {error && (
        <Alert severity="error" sx={{ mb: 2 }} onClose={() => setError(null)}>
          {error}
        </Alert>
      )}

      {/* Loading */}
      {loading && (
        <Box sx={{ display: 'flex', justifyContent: 'center', py: 5 }}>
          <CircularProgress />
        </Box>
      )}

      {/* Evaluations List */}
      {!loading && filteredEvaluations.length === 0 && (
        <Card>
          <CardContent>
            <Typography color="textSecondary" align="center">
              No pending evaluations found
            </Typography>
          </CardContent>
        </Card>
      )}

      {!loading && filteredEvaluations.map((eval) => (
        <Card key={eval.dr_number} sx={{ mb: 2 }}>
          <CardContent>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
              <Typography variant="h6">{eval.dr_number}</Typography>
              <Chip
                label={eval.overall_status}
                color={
                  eval.overall_status === 'PASS' ? 'success' :
                  eval.overall_status === 'PARTIAL' ? 'warning' : 'error'
                }
                size="small"
              />
            </Box>

            <Grid container spacing={2} sx={{ mb: 2 }}>
              <Grid item xs={4}>
                <Typography variant="body2" color="textSecondary">Score</Typography>
                <Typography variant="h6">{eval.average_score}/10</Typography>
              </Grid>
              <Grid item xs={4}>
                <Typography variant="body2" color="textSecondary">Steps Passed</Typography>
                <Typography variant="h6">{eval.passed_steps}/{eval.total_steps}</Typography>
              </Grid>
              <Grid item xs={4}>
                <Typography variant="body2" color="textSecondary">Date</Typography>
                <Typography variant="body2">
                  {new Date(eval.evaluation_date).toLocaleDateString()}
                </Typography>
              </Grid>
            </Grid>

            <Button
              variant="contained"
              size="small"
              onClick={() => handleReview(eval)}
            >
              Review Feedback
            </Button>
          </CardContent>
        </Card>
      ))}

      {/* Review Dialog */}
      <Dialog
        open={selectedEval !== null}
        onClose={() => setSelectedEval(null)}
        maxWidth="md"
        fullWidth
      >
        <DialogTitle>
          Review Feedback - {selectedEval?.dr_number}
        </DialogTitle>
        <DialogContent>
          <Box sx={{ mb: 2 }}>
            <Chip
              label={selectedEval?.overall_status}
              color={
                selectedEval?.overall_status === 'PASS' ? 'success' :
                selectedEval?.overall_status === 'PARTIAL' ? 'warning' : 'error'
              }
              sx={{ mr: 1 }}
            />
            <Typography variant="body2" component="span" color="textSecondary">
              Score: {selectedEval?.average_score}/10 •
              Steps: {selectedEval?.passed_steps}/{selectedEval?.total_steps}
            </Typography>
          </Box>

          <Divider sx={{ my: 2 }} />

          <Typography variant="subtitle2" gutterBottom>
            WhatsApp Message:
          </Typography>

          {isEditing ? (
            <TextField
              fullWidth
              multiline
              rows={12}
              value={feedbackMessage}
              onChange={(e) => setFeedbackMessage(e.target.value)}
              variant="outlined"
              sx={{ fontFamily: 'monospace', mb: 2 }}
            />
          ) : (
            <Box
              sx={{
                bgcolor: 'grey.100',
                p: 2,
                borderRadius: 1,
                fontFamily: 'monospace',
                whiteSpace: 'pre-wrap',
                fontSize: '0.875rem',
                mb: 2
              }}
            >
              {feedbackMessage}
            </Box>
          )}

          {!isEditing && (
            <Button
              startIcon={<EditIcon />}
              onClick={() => setIsEditing(true)}
              size="small"
            >
              Edit Message
            </Button>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={handleReject} color="error">
            Reject
          </Button>
          <Button
            onClick={handleSendFeedback}
            variant="contained"
            startIcon={sending ? <CircularProgress size={20} /> : <SendIcon />}
            disabled={sending}
          >
            {sending ? 'Sending...' : 'Send to WhatsApp'}
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
}
