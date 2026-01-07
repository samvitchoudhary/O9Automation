import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { testCasesAPI, testStepsAPI } from '../services/api';
import TestCaseExecutor from './TestCaseExecutor';

const TestCaseDetail = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [testCase, setTestCase] = useState(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  useEffect(() => {
    loadTestCase();
  }, [id]);

  const loadTestCase = async () => {
    try {
      setLoading(true);
      const data = await testCasesAPI.getById(id);
      setTestCase(data);
    } catch (err) {
      console.error('Error loading test case:', err);
      setError('Failed to load test case. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleUpdateTestCase = async (field, value) => {
    try {
      setSaving(true);
      const updated = await testCasesAPI.update(id, { [field]: value });
      setTestCase(updated);
      setSuccess('Test case updated successfully');
      setTimeout(() => setSuccess(''), 3000);
    } catch (err) {
      console.error('Error updating test case:', err);
      setError('Failed to update test case. Please try again.');
    } finally {
      setSaving(false);
    }
  };

  const handleUpdateStep = async (stepId, field, value) => {
    try {
      setSaving(true);
      await testStepsAPI.update(id, stepId, { [field]: value });
      await loadTestCase();
      setSuccess('Step updated successfully');
      setTimeout(() => setSuccess(''), 3000);
    } catch (err) {
      console.error('Error updating step:', err);
      setError('Failed to update step. Please try again.');
    } finally {
      setSaving(false);
    }
  };

  const handleDeleteStep = async (stepId) => {
    if (window.confirm('Are you sure you want to delete this step?')) {
      try {
        await testStepsAPI.delete(id, stepId);
        await loadTestCase();
        setSuccess('Step deleted successfully');
        setTimeout(() => setSuccess(''), 3000);
      } catch (err) {
        console.error('Error deleting step:', err);
        setError('Failed to delete step. Please try again.');
      }
    }
  };

  const handleApprove = async () => {
    try {
      setSaving(true);
      const updated = await testCasesAPI.approve(id);
      setTestCase(updated);
      setSuccess('Test case approved successfully');
      setTimeout(() => setSuccess(''), 3000);
    } catch (err) {
      console.error('Error approving test case:', err);
      setError('Failed to approve test case. Please try again.');
    } finally {
      setSaving(false);
    }
  };

  // Removed: handleExportExcel and handleGenerateSelenium functions

  const getStatusBadgeColor = (status) => {
    const colors = {
      draft: 'bg-gray-100 text-gray-800',
      approved: 'bg-green-100 text-green-800',
      in_progress: 'bg-blue-100 text-blue-800',
      completed: 'bg-purple-100 text-purple-800',
      failed: 'bg-red-100 text-red-800',
    };
    return colors[status] || 'bg-gray-100 text-gray-800';
  };

  const getStepStatusBadgeColor = (status) => {
    const colors = {
      not_started: 'bg-gray-100 text-gray-800',
      passed: 'bg-green-100 text-green-800',
      failed: 'bg-red-100 text-red-800',
      blocked: 'bg-yellow-100 text-yellow-800',
    };
    return colors[status] || 'bg-gray-100 text-gray-800';
  };

  const formatStatus = (status) => {
    return status.split('_').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ');
  };

  if (loading) {
    return (
      <div className="text-center py-12">
        <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
        <p className="mt-2 text-gray-600">Loading test case...</p>
      </div>
    );
  }

  if (!testCase) {
    return (
      <div className="text-center py-12">
        <p className="text-gray-600">Test case not found.</p>
        <button
          onClick={() => navigate('/')}
          className="mt-4 text-blue-600 hover:text-blue-800"
        >
          Back to Dashboard
        </button>
      </div>
    );
  }

  const sortedSteps = [...(testCase.steps || [])].sort((a, b) => a.step_number - b.step_number);

  return (
    <div>
      <div className="mb-6 flex items-center justify-between">
        <div>
          <button
            onClick={() => navigate('/')}
            className="text-blue-600 hover:text-blue-800 mb-2"
          >
            ← Back to Dashboard
          </button>
          <h1 className="text-3xl font-bold text-gray-900">{testCase.name}</h1>
        </div>
        <div className="flex items-center space-x-2">
          <span
            className={`px-3 py-1 inline-flex text-sm leading-5 font-semibold rounded-full ${getStatusBadgeColor(
              testCase.status
            )}`}
          >
            {formatStatus(testCase.status)}
          </span>
        </div>
      </div>

      {error && (
        <div className="mb-4 p-4 bg-red-50 border border-red-200 rounded-md">
          <p className="text-sm text-red-800">{error}</p>
        </div>
      )}

      {success && (
        <div className="mb-4 p-4 bg-green-50 border border-green-200 rounded-md">
          <p className="text-sm text-green-800">{success}</p>
        </div>
      )}

      {/* Test Case Metadata */}
      <div className="bg-white rounded-lg shadow p-6 mb-6">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">Test Case Information</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Name</label>
            <input
              type="text"
              value={testCase.name}
              onChange={(e) => handleUpdateTestCase('name', e.target.value)}
              onBlur={(e) => handleUpdateTestCase('name', e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              disabled={saving}
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Status</label>
            <select
              value={testCase.status}
              onChange={(e) => handleUpdateTestCase('status', e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              disabled={saving}
            >
              <option value="draft">Draft</option>
              <option value="approved">Approved</option>
              <option value="in_progress">In Progress</option>
              <option value="completed">Completed</option>
              <option value="failed">Failed</option>
            </select>
          </div>
          <div className="md:col-span-2">
            <label className="block text-sm font-medium text-gray-700 mb-1">Description</label>
            <textarea
              value={testCase.description || ''}
              onChange={(e) => handleUpdateTestCase('description', e.target.value)}
              onBlur={(e) => handleUpdateTestCase('description', e.target.value)}
              rows={3}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              disabled={saving}
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Requirements</label>
            <input
              type="text"
              value={testCase.requirements || ''}
              onChange={(e) => handleUpdateTestCase('requirements', e.target.value)}
              onBlur={(e) => handleUpdateTestCase('requirements', e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              placeholder="e.g., RQ-123, RQ-456"
              disabled={saving}
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Assigned To</label>
            <input
              type="text"
              value={testCase.assigned_to || ''}
              onChange={(e) => handleUpdateTestCase('assigned_to', e.target.value)}
              onBlur={(e) => handleUpdateTestCase('assigned_to', e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              disabled={saving}
            />
          </div>
        </div>
      </div>

      {/* Action Buttons - Removed: Export to Excel, Generate Selenium Script */}
      {testCase.status !== 'approved' && (
        <div className="bg-white rounded-lg shadow p-6 mb-6">
          <div className="flex flex-wrap gap-3">
            <button
              onClick={handleApprove}
              disabled={saving}
              className="bg-green-600 text-white px-4 py-2 rounded-md font-medium hover:bg-green-700 disabled:bg-gray-400"
            >
              Approve Test Case
            </button>
          </div>
        </div>
      )}

      {/* Test Execution Section - This is the ONLY section showing steps */}
      {sortedSteps.length > 0 ? (
        <TestCaseExecutor
          testCase={testCase}
          steps={sortedSteps}
          onRefresh={loadTestCase}
        />
      ) : (
        <div className="bg-white rounded-lg shadow p-6">
          <p className="text-gray-500 text-center py-8">No test steps yet.</p>
        </div>
      )}
    </div>
  );
};

export default TestCaseDetail;

