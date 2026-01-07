import React from 'react';
import TestStepExecutor from './TestStepExecutor';

const TestCaseExecutor = ({ testCase, steps, onRefresh }) => {

  // Removed: handleRunAllSteps and handleGenerateAllScripts functions

  const handleStatusUpdate = (status) => {
    // Refresh to get updated statuses
    onRefresh();
  };

  return (
    <div className="mt-6">
      {/* Steps - Removed control bar with "Generate All Scripts" and "Run All Steps" */}
      {steps.map(step => (
        <TestStepExecutor
          key={step.id}
          step={step}
          testCaseId={testCase?.id}
          onStatusUpdate={handleStatusUpdate}
          onRefresh={onRefresh}
        />
      ))}
    </div>
  );
};

export default TestCaseExecutor;

