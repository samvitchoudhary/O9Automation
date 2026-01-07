import React, { useState, useEffect, useRef } from 'react';
import { testStepsAPI } from '../services/api';

// Get API base URL from environment or use default
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const TestStepExecutor = ({ step, onStatusUpdate, onRefresh, testCaseId }) => {
  const [isRunning, setIsRunning] = useState(false);
  const [screenshot, setScreenshot] = useState(null);
  const [progress, setProgress] = useState('');
  const [showScript, setShowScript] = useState(false);
  const [isGenerating, setIsGenerating] = useState(false);
  const [editedScript, setEditedScript] = useState(step.selenium_script || '');
  const [editedScriptJson, setEditedScriptJson] = useState(step.selenium_script_json || '');
  const [ws, setWs] = useState(null);
  const wsRef = useRef(null);
  
  // Edit mode state
  const [isEditing, setIsEditing] = useState(false);
  const [editedDescription, setEditedDescription] = useState(step.description || '');
  const [editedExpectedResult, setEditedExpectedResult] = useState(step.expected_result || '');
  const [isSaving, setIsSaving] = useState(false);

  useEffect(() => {
    // Update edited script when step changes
    console.log('Step prop changed, updating script state');
    console.log('Step has selenium_script:', !!step.selenium_script);
    console.log('Script length:', step.selenium_script?.length || 0);
    if (step.selenium_script) {
      setEditedScript(step.selenium_script);
      setEditedScriptJson(step.selenium_script_json || '');
      console.log('✓ State updated from step prop');
    }
  }, [step.selenium_script, step.selenium_script_json, step.id]);

  // Update local state when step prop changes (for editing)
  useEffect(() => {
    setEditedDescription(step.description || '');
    setEditedExpectedResult(step.expected_result || '');
  }, [step.description, step.expected_result]);

  const handleRunStep = () => {
    setIsRunning(true);
    setScreenshot(null);
    setProgress('');

    // Create WebSocket connection
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const wsUrl = `${protocol}//${window.location.host.replace(':5173', ':8000')}/ws/execute-step/${step.id}`;
    const websocket = new WebSocket(wsUrl);
    wsRef.current = websocket;

    websocket.onopen = () => {
      console.log('WebSocket connected');
    };

    websocket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      
      if (data.type === 'status_update') {
        onStatusUpdate(data.status);
      } else if (data.type === 'progress') {
        setProgress(data.message || data.action || '');
      } else if (data.type === 'screenshot') {
        setScreenshot(`data:image/png;base64,${data.image}`);
      } else if (data.type === 'execution_complete') {
        setIsRunning(false);
        setProgress('');
        onStatusUpdate(data.status);
        websocket.close();
      } else if (data.type === 'execution_error') {
        setIsRunning(false);
        setProgress('');
        alert(`Execution error: ${data.error}`);
        websocket.close();
      }
    };

    websocket.onerror = (error) => {
      console.error('WebSocket error:', error);
      setIsRunning(false);
      setProgress('');
    };

    websocket.onclose = () => {
      console.log('WebSocket closed');
      setIsRunning(false);
    };
  };

  const handleGenerateScript = async (e) => {
    // Prevent any default behavior (form submission, page refresh, etc.)
    if (e) {
      e.preventDefault();
      e.stopPropagation();
    }
    
    // Prevent multiple clicks
    if (isGenerating) {
      console.log('Already generating, ignoring click');
      return;
    }
    
    setIsGenerating(true);
    
    console.log('=== GENERATE SCRIPT START ===');
    console.log('Step ID:', step.id);
    console.log('Step description:', step.description?.substring(0, 50));
    
    try {
      setProgress('Generating Selenium script...');
      
      console.log('Making fetch request...');
      console.log('API URL:', `${API_BASE_URL}/api/test-steps/${step.id}/generate-selenium`);
      const startTime = Date.now();
      
      const response = await fetch(`${API_BASE_URL}/api/test-steps/${step.id}/generate-selenium`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        }
      });
      
      const endTime = Date.now();
      console.log(`Request completed in ${endTime - startTime}ms`);
      console.log('Response status:', response.status);
      console.log('Response OK:', response.ok);
      
      // Get response as text first to see what we got
      const textResponse = await response.text();
      console.log('Response text (first 500 chars):', textResponse.substring(0, 500));
      
      // Try to parse as JSON
      let data;
      try {
        data = JSON.parse(textResponse);
      } catch (e) {
        console.error('Failed to parse response as JSON:', e);
        console.error('Full response:', textResponse);
        throw new Error(`Server returned invalid response: ${textResponse.substring(0, 200)}`);
      }
      
      console.log('Response data keys:', Object.keys(data));
      console.log('Has selenium_script:', !!data.selenium_script);
      console.log('Script length:', data.selenium_script?.length || 0);
      
      if (!response.ok) {
        console.error('Response not OK:', data);
        const errorMsg = data.detail || data.error || data.message || 'Failed to generate script';
        throw new Error(errorMsg);
      }
      
      // Check if we got the scripts
      if (!data.selenium_script) {
        console.error('No selenium_script in response:', data);
        throw new Error('Response missing selenium_script field');
      }
      
      // CRITICAL: Update the local state with the actual script
      console.log('Updating local state with script...');
      console.log('Script from response:', data.selenium_script?.substring(0, 100));
      
      if (data.selenium_script) {
        setEditedScript(data.selenium_script);
        setEditedScriptJson(data.selenium_script_json || '');
        console.log('✓ State updated with new script, length:', data.selenium_script.length);
      } else {
        console.error('✗ No selenium_script in response!');
        console.error('Response data:', data);
        throw new Error('Server did not return a script');
      }
      
      // Show success message
      setProgress('✓ Script generated successfully!');
      
      // Auto-show the script section immediately
      setShowScript(true);
      console.log('✓ Script editor opened');
      
      // Refresh parent to update the step prop with fresh data from DB
      console.log('Calling onRefresh if exists...');
      if (typeof onRefresh === 'function') {
        console.log('onRefresh is a function, calling it...');
        await onRefresh();
        console.log('✓ Refresh complete');
      } else {
        console.log('No onRefresh function provided');
      }
      
      // Also call onStatusUpdate if provided
      if (onStatusUpdate) {
        onStatusUpdate('script_generated');
      }
      
      setTimeout(() => setProgress(''), 3000);
      console.log('=== GENERATE SCRIPT SUCCESS ===');
      
    } catch (error) {
      console.error('=== GENERATE SCRIPT ERROR ===');
      console.error('Error:', error);
      console.error('Error name:', error.name);
      console.error('Error message:', error.message);
      console.error('Error stack:', error.stack);
      
      let errorMessage = error.message || 'Failed to generate script. Please try again.';
      
      // Provide more helpful error messages
      if (error.message === 'Failed to fetch' || error.name === 'TypeError') {
        errorMessage = `Cannot connect to backend server. Make sure the backend is running on ${API_BASE_URL}`;
      } else if (error.message.includes('NetworkError') || error.message.includes('network')) {
        errorMessage = 'Network error. Check that backend is running and CORS is configured.';
      }
      
      setProgress(`Error: ${errorMessage}`);
      
      // Show error for longer (10 seconds)
      setTimeout(() => setProgress(''), 10000);
    } finally {
      setIsGenerating(false);
    }
  };

  const handleSaveScript = async () => {
    try {
      console.log('Saving script to:', `${API_BASE_URL}/api/test-steps/${step.id}/update-selenium`);
      const response = await fetch(`${API_BASE_URL}/api/test-steps/${step.id}/update-selenium`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          selenium_script: editedScript,
          selenium_script_json: editedScriptJson
        })
      });
      
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || errorData.error || `Server error: ${response.status}`);
      }
      
      setShowScript(false);
      setProgress('✓ Script saved successfully!');
      setTimeout(() => setProgress(''), 3000);
      
      if (onStatusUpdate) {
        onStatusUpdate('script_saved');
      }
    } catch (error) {
      console.error('Error saving script:', error);
      let errorMessage = error.message || 'Failed to save script. Please try again.';
      
      if (error.message === 'Failed to fetch' || error.name === 'TypeError') {
        errorMessage = `Cannot connect to backend server. Make sure the backend is running on ${API_BASE_URL}`;
      }
      
      setProgress(`Error: ${errorMessage}`);
      setTimeout(() => setProgress(''), 10000);
    }
  };

  const handleSaveEdit = async (e) => {
    if (e) {
      e.preventDefault();
      e.stopPropagation();
    }

    setIsSaving(true);

    try {
      if (!testCaseId) {
        throw new Error('Test case ID is required');
      }

      console.log('Saving step edit...');
      console.log('Test Case ID:', testCaseId);
      console.log('Step ID:', step.id);
      console.log('Data:', { description: editedDescription, expected_result: editedExpectedResult });

      // Use the API service for consistency
      const updatedStep = await testStepsAPI.update(testCaseId, step.id, {
        description: editedDescription,
        expected_result: editedExpectedResult
      });

      console.log('Step updated successfully:', updatedStep);

      setIsEditing(false);
      setProgress('✓ Changes saved! Click "Regenerate Script" to update the script.');

      if (typeof onRefresh === 'function') {
        await onRefresh();
      }

      setTimeout(() => setProgress(''), 5000);

    } catch (error) {
      console.error('Save error:', error);
      console.error('Error name:', error.name);
      console.error('Error message:', error.message);
      
      let errorMessage = error.message || 'Failed to save changes';
      
      // Provide more helpful error messages
      if (error.message === 'Failed to fetch' || error.name === 'TypeError' || error.message.includes('NetworkError')) {
        errorMessage = `Cannot connect to backend server. Make sure the backend is running on ${API_BASE_URL}`;
      } else if (error.response) {
        // Axios error response
        errorMessage = error.response.data?.detail || error.response.data?.error || `Server error: ${error.response.status}`;
      }
      
      setProgress(`Error: ${errorMessage}`);
      setTimeout(() => setProgress(''), 10000);
    } finally {
      setIsSaving(false);
    }
  };

  const handleCancelEdit = () => {
    setEditedDescription(step.description || '');
    setEditedExpectedResult(step.expected_result || '');
    setIsEditing(false);
  };

  const getStatusColor = () => {
    const status = step.execution_status || 'not_run';
    const colors = {
      passed: 'bg-green-100 text-green-800',
      failed: 'bg-red-100 text-red-800',
      error: 'bg-yellow-100 text-yellow-800',
      running: 'bg-blue-100 text-blue-800',
      not_run: 'bg-gray-100 text-gray-800',
    };
    return colors[status] || 'bg-gray-100 text-gray-800';
  };

  const formatStatus = (status) => {
    if (!status) return 'Not Run';
    return status.split('_').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ');
  };

  return (
    <div className="border rounded-lg p-4 mb-4 bg-white">
      {/* Step Header */}
      <div className="flex items-center justify-between mb-3">
        <div className="flex items-center space-x-3">
          <span className="font-semibold text-gray-900">Step {step.step_number}</span>
          <span className={`px-2 py-1 rounded text-xs font-medium ${getStatusColor()}`}>
            {formatStatus(step.execution_status)}
          </span>
          {step.execution_time_ms && (
            <span className="text-xs text-gray-500">
              {step.execution_time_ms}ms
            </span>
          )}
        </div>
        <div className="flex space-x-2">
          {/* Edit Mode Buttons */}
          {isEditing ? (
            <>
              <button
                type="button"
                onClick={handleSaveEdit}
                disabled={isSaving}
                className={`px-3 py-1 rounded text-sm text-white font-medium ${
                  isSaving ? 'bg-gray-400 cursor-not-allowed' : 'bg-green-600 hover:bg-green-700'
                }`}
              >
                {isSaving ? 'Saving...' : 'Save Changes'}
              </button>
              <button
                type="button"
                onClick={handleCancelEdit}
                disabled={isSaving}
                className="px-3 py-1 bg-gray-500 text-white rounded text-sm hover:bg-gray-600 font-medium"
              >
                Cancel
              </button>
            </>
          ) : (
            <>
              {/* Edit Button */}
              <button
                type="button"
                onClick={() => setIsEditing(true)}
                className="px-3 py-1 bg-gray-600 text-white rounded text-sm hover:bg-gray-700 font-medium"
              >
                Edit Step
              </button>
              
              {/* Run Step Button - Only show if script exists */}
              {step.selenium_script_json && (
                <button
                  type="button"
                  onClick={handleRunStep}
                  disabled={isRunning}
                  className="px-3 py-1 bg-blue-600 text-white rounded text-sm hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed font-medium"
                >
                  {isRunning ? 'Running...' : 'Run Step'}
                </button>
              )}
              
              {/* View Script Button - Only show if script exists */}
              {step.selenium_script_json && (
                <button
                  type="button"
                  onClick={() => setShowScript(!showScript)}
                  className="px-3 py-1 bg-gray-600 text-white rounded text-sm hover:bg-gray-700 font-medium"
                >
                  {showScript ? 'Hide Script' : 'View Script'}
                </button>
              )}
              
              {/* Generate/Regenerate Script Button */}
              <button
                type="button"
                onClick={handleGenerateScript}
                disabled={isGenerating}
                className={`px-3 py-1 rounded text-sm font-medium ${
                  isGenerating 
                    ? 'bg-gray-400 cursor-not-allowed' 
                    : 'bg-purple-600 hover:bg-purple-700'
                } text-white`}
              >
                {isGenerating ? 'Generating...' : (step.selenium_script_json ? 'Regenerate Script' : 'Generate Script')}
              </button>
            </>
          )}
        </div>
      </div>

      {/* Progress/Error Display */}
      {progress && (
        <div className={`mb-3 p-2 rounded text-sm ${
          progress.includes('Error') 
            ? 'bg-red-50 text-red-700 border border-red-200' 
            : progress.includes('successfully')
            ? 'bg-green-50 text-green-700 border border-green-200'
            : 'bg-blue-50 text-blue-700 border border-blue-200'
        }`}>
          {progress}
        </div>
      )}

      {/* Step Description - Editable or Display */}
      <div className="mb-3">
        <label className="text-xs font-semibold text-gray-600 block mb-1">
          Description:
        </label>
        {isEditing ? (
          <textarea
            value={editedDescription}
            onChange={(e) => setEditedDescription(e.target.value)}
            className="w-full p-2 border rounded text-sm resize-none focus:outline-none focus:ring-2 focus:ring-blue-500"
            rows={3}
            placeholder="Enter step description..."
          />
        ) : (
          <p className="text-sm text-gray-700 whitespace-pre-wrap bg-gray-50 p-2 rounded">
            {step.description || 'No description'}
          </p>
        )}
      </div>

      {/* Expected Result - Editable or Display */}
      <div className="mb-3">
        <label className="text-xs font-semibold text-gray-600 block mb-1">
          Expected Result:
        </label>
        {isEditing ? (
          <textarea
            value={editedExpectedResult}
            onChange={(e) => setEditedExpectedResult(e.target.value)}
            className="w-full p-2 border rounded text-sm resize-none focus:outline-none focus:ring-2 focus:ring-blue-500"
            rows={2}
            placeholder="Enter expected result..."
          />
        ) : (
          <p className="text-sm text-gray-600 bg-gray-50 p-2 rounded">
            {step.expected_result || 'No expected result'}
          </p>
        )}
      </div>

      {/* Error Message */}
      {step.error_message && (
        <div className="mt-2 p-2 bg-red-50 border border-red-200 rounded">
          <p className="text-sm text-red-700">Error: {step.error_message}</p>
        </div>
      )}

      {/* Real-time Progress */}
      {isRunning && progress && (
        <div className="mt-2 p-2 bg-blue-50 border border-blue-200 rounded">
          <p className="text-xs text-blue-700">{progress}</p>
        </div>
      )}

      {/* Live Browser View */}
      {screenshot && (
        <div className="mt-3">
          <p className="text-xs font-semibold text-gray-600 mb-1">Live View:</p>
          <img
            src={screenshot}
            alt="Browser view"
            className="w-full border rounded max-h-64 object-contain bg-gray-100"
          />
        </div>
      )}

      {/* Script Editor - Read-only display (only show when not editing) */}
      {showScript && step.selenium_script && !isEditing && (
        <div className="mt-3 border-t pt-3">
          <div className="bg-blue-50 border border-blue-200 rounded p-3 mb-3">
            <p className="text-xs text-blue-800">
              <strong>Note:</strong> The Python script below is for <strong>reference only</strong>. 
              The system executes <strong>JSON commands</strong> (not shown here) which are generated 
              automatically and optimized for the automation framework. The JSON commands are what actually 
              control the browser - this Python code is just for human readability.
            </p>
          </div>
          <div className="flex justify-between items-center mb-2">
            <p className="text-sm font-semibold">Selenium Script (Reference Only)</p>
          </div>
          <textarea
            value={editedScript || 'No script generated yet'}
            readOnly
            className="w-full h-64 p-2 border rounded font-mono text-xs bg-gray-50"
            placeholder="Script will appear here..."
          />
        </div>
      )}
    </div>
  );
};

export default TestStepExecutor;

