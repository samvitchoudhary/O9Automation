import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { testCasesAPI } from '../services/api';

const CreateTestCase = () => {
  const [prompt, setPrompt] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const examplePrompts = [
    "Create a test case for validating BOM consumption in the manufacturing network. Include steps for filtering items, viewing consumed materials, and exporting the data.",
    "Generate a test for the AI/ML forecast analysis workflow. The test should cover login, navigating to the forecast page, analyzing driver-based forecasts, and reviewing gap percentages.",
    "Test the demand planning forecast generation process including system forecast review and last cycle comparison.",
  ];

  const handleGenerate = async (e) => {
    e.preventDefault();
    
    if (!prompt.trim()) {
      setError('Please enter a test case description');
      return;
    }

    setLoading(true);
    setError('');

    try {
      const testCase = await testCasesAPI.generate(prompt);
      navigate(`/test-case/${testCase.id}`);
    } catch (err) {
      console.error('Error generating test case:', err);
      setError(err.response?.data?.detail || 'Failed to generate test case. Please try again.');
    } finally {
      setLoading(false);
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
            <p className="text-sm text-red-800">{error}</p>
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

