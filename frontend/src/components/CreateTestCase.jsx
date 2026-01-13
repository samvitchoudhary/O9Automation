import React, { useState, useRef, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { testCasesAPI } from '../services/api';

const CreateTestCase = () => {
  const [prompt, setPrompt] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [progress, setProgress] = useState(0);
  const [progressMessage, setProgressMessage] = useState('');
  const [currentStep, setCurrentStep] = useState(0);
  const [totalSteps, setTotalSteps] = useState(0);
  const [useWebSocket, setUseWebSocket] = useState(true); // Prefer WebSocket
  const navigate = useNavigate();
  const wsRef = useRef(null);

  const examplePrompts = [
    "Create a test case for validating BOM consumption in the manufacturing network. Include steps for filtering items, viewing consumed materials, and exporting the data.",
    "Generate a test for the AI/ML forecast analysis workflow. The test should cover login, navigating to the forecast page, analyzing driver-based forecasts, and reviewing gap percentages.",
    "Test the demand planning forecast generation process including system forecast review and last cycle comparison.",
  ];

  // Cleanup WebSocket on unmount
  useEffect(() => {
    return () => {
      if (wsRef.current) {
        wsRef.current.close();
      }
    };
  }, []);

  const handleGenerateWebSocket = (e) => {
    e.preventDefault();
    
    if (!prompt.trim()) {
      setError('Please enter a test case description');
      return;
    }

    setLoading(true);
    setError('');
    setProgress(0);
    setProgressMessage('Connecting...');
    setCurrentStep(0);
    setTotalSteps(0);

    // Create WebSocket connection
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const wsUrl = `${protocol}//${window.location.host.replace(':5173', ':8000')}/ws/generate-test-case`;
    const websocket = new WebSocket(wsUrl);
    wsRef.current = websocket;

    websocket.onopen = () => {
      console.log('WebSocket connected for test case generation');
      setProgressMessage('Connected. Starting generation...');
      
      // Send generation request
      websocket.send(JSON.stringify({ description: prompt.trim() }));
    };

    websocket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      console.log('WebSocket message:', data);
      
      if (data.type === 'generation_progress') {
        setProgress(data.progress || 0);
        setProgressMessage(data.message || 'Processing...');
        setCurrentStep(data.step || 0);
        setTotalSteps(data.total || 0);
      } else if (data.type === 'generation_complete') {
        if (data.success && data.test_case_id) {
          console.log(`✓ Test case ${data.test_case_id} generated successfully`);
          setProgress(100);
          setProgressMessage('✓ Complete! Redirecting...');
          
          // Redirect after brief delay
          setTimeout(() => {
            navigate(data.redirect_url || `/test-case/${data.test_case_id}`);
          }, 1000);
        } else {
          setError('Generation completed but no test case ID received');
          setLoading(false);
        }
        websocket.close();
      } else if (data.type === 'generation_error') {
        console.error('Generation error:', data);
        setError(data.error || 'Failed to generate test case. Please try again.');
        setLoading(false);
        websocket.close();
      }
    };

    websocket.onerror = (error) => {
      console.error('WebSocket error:', error);
      setError('WebSocket connection error. Falling back to REST API...');
      setLoading(false);
      websocket.close();
      
      // Fallback to REST API
      setTimeout(() => {
        handleGenerateREST(e);
      }, 500);
    };

    websocket.onclose = () => {
      console.log('WebSocket closed');
      if (loading && progress < 100) {
        // Connection closed unexpectedly
        setError('Connection closed unexpectedly. Please try again.');
        setLoading(false);
      }
    };
  };

  const handleGenerateREST = async (e) => {
    e.preventDefault();
    
    if (!prompt.trim()) {
      setError('Please enter a test case description');
      return;
    }

    setLoading(true);
    setError('');
    setProgress(0);
    setProgressMessage('Generating test case... (this may take 30-60 seconds)');

    try {
      console.log('Generating test case with REST API:', prompt.substring(0, 100) + '...');
      
      const response = await testCasesAPI.generate(prompt);
      
      console.log('Response received:', response);
      
      // Check for success response (new format)
      if (response.success && response.test_case_id) {
        console.log(`✓ Test case ${response.test_case_id} generated successfully`);
        console.log(`  Name: ${response.test_case_name}`);
        console.log(`  Steps: ${response.steps_count}`);
        console.log(`  Redirecting to: ${response.redirect_url}`);
        
        setProgress(100);
        setProgressMessage('✓ Complete! Redirecting...');
        
        // Redirect to the new test case page
        setTimeout(() => {
          navigate(response.redirect_url || `/test-case/${response.test_case_id}`);
        }, 500);
      } 
      // Fallback: Check for test_case object (old format)
      else if (response.id || response.test_case?.id) {
        const testCaseId = response.id || response.test_case?.id;
        console.log(`✓ Test case ${testCaseId} generated (legacy format)`);
        setProgress(100);
        setTimeout(() => {
          navigate(`/test-case/${testCaseId}`);
        }, 500);
      }
      // No success flag and no ID - this shouldn't happen
      else {
        console.error('Unexpected response format:', response);
        setError('Test case generated but response format is unexpected. Please check the test cases list.');
        setLoading(false);
      }
      
    } catch (err) {
      console.error('Error generating test case:', err);
      
      // Extract error message
      let errorMessage = 'Failed to generate test case. Please try again.';
      
      if (err.code === 'ECONNABORTED' || err.message?.includes('timeout')) {
        errorMessage = 'Generation is taking longer than expected. The test case may still be created - please check the test cases list.';
      } else if (err.response?.data?.detail) {
        errorMessage = err.response.data.detail;
      } else if (err.response?.data?.error) {
        errorMessage = err.response.data.error;
      } else if (err.message) {
        errorMessage = err.message;
      }
      
      setError(errorMessage);
      setLoading(false);
    }
  };

  const handleGenerate = (e) => {
    // Try WebSocket first, fallback to REST if needed
    if (useWebSocket) {
      handleGenerateWebSocket(e);
    } else {
      handleGenerateREST(e);
    }
  };

  const useExamplePrompt = (examplePrompt) => {
    setPrompt(examplePrompt);
  };

  return (
    <div className="max-w-4xl mx-auto">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Create New Test Case</h1>
        <p className="text-gray-600">
          Describe your test case in natural language, and our AI will generate detailed test steps for you.
        </p>
      </div>

      <form onSubmit={handleGenerate} className="bg-white rounded-lg shadow p-6">
        <div className="mb-6">
          <label htmlFor="prompt" className="block text-sm font-medium text-gray-700 mb-2">
            Test Case Description
          </label>
          <textarea
            id="prompt"
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            rows={8}
            className="w-full px-4 py-3 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
            placeholder="Describe what you want to test in O9. For example: 'Create a test for validating BOM consumption in the manufacturing network...'"
            disabled={loading}
          />
          <p className="mt-2 text-sm text-gray-500">
            Be as specific as possible about the workflow, modules, and validations you want to test.
          </p>
        </div>

        {error && (
          <div className="mb-4 p-4 bg-red-50 border border-red-200 rounded-md">
            <p className="text-sm text-red-800">
              <strong>Error:</strong> {error}
            </p>
          </div>
        )}

        {loading && (
          <div className="mb-4 p-4 bg-blue-50 border border-blue-200 rounded-md">
            {/* Progress Bar */}
            {progress > 0 && (
              <div className="mb-3">
                <div className="w-full bg-blue-200 rounded-full h-2.5 mb-2">
                  <div 
                    className="bg-blue-600 h-2.5 rounded-full transition-all duration-500 ease-out"
                    style={{ width: `${progress}%` }}
                  ></div>
                </div>
                <div className="flex justify-between items-center text-sm">
                  <span className="text-blue-800 font-semibold">{progress}%</span>
                  {totalSteps > 0 && (
                    <span className="text-blue-600">Step {currentStep} of {totalSteps}</span>
                  )}
                </div>
              </div>
            )}
            
            <div className="flex items-center">
              <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-blue-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              <div className="flex-1">
                <p className="text-sm text-blue-800 font-semibold">
                  {progressMessage || 'Generating test case...'}
                </p>
                <p className="text-xs text-blue-600 mt-1">
                  ⏱️ AI generation typically takes 30-60 seconds. Please wait...
                </p>
              </div>
            </div>
          </div>
        )}

        <div className="flex justify-end">
          <button
            type="submit"
            disabled={loading || !prompt.trim()}
            className="bg-blue-600 text-white px-6 py-3 rounded-md font-medium hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed flex items-center"
          >
            {loading ? (
              <>
                <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Generating Test Case...
              </>
            ) : (
              'Generate Test Case'
            )}
          </button>
        </div>
      </form>

      {/* Example Prompts */}
      <div className="mt-8 bg-blue-50 rounded-lg p-6">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">Example Prompts</h2>
        <p className="text-sm text-gray-600 mb-4">
          Click on any example below to use it as a starting point:
        </p>
        <div className="space-y-3">
          {examplePrompts.map((example, index) => (
            <button
              key={index}
              onClick={() => useExamplePrompt(example)}
              className="w-full text-left p-4 bg-white rounded-md border border-blue-200 hover:border-blue-400 hover:shadow-md transition-all"
              disabled={loading}
            >
              <p className="text-sm text-gray-700">{example}</p>
            </button>
          ))}
        </div>
      </div>
    </div>
  );
};

export default CreateTestCase;

