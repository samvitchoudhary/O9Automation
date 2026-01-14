import React from 'react';
import './ViewScriptModal.css';

function ViewScriptModal({ step, onClose }) {
  if (!step) return null;

  // Parse JSON commands
  let jsonCommands = [];
  let jsonError = null;
  
  try {
    if (step.selenium_script_json) {
      jsonCommands = JSON.parse(step.selenium_script_json);
    } else {
      jsonError = 'No JSON commands available';
    }
  } catch (e) {
    jsonError = `Error parsing JSON: ${e.message}`;
  }

  /**
   * Export JSON commands to a file
   */
  const handleExportJson = () => {
    try {
      // Create formatted JSON string
      const jsonString = JSON.stringify(jsonCommands, null, 2);
      
      // Create blob
      const blob = new Blob([jsonString], { type: 'application/json' });
      
      // Create download link
      const url = URL.createObjectURL(blob);
      const link = document.createElement('a');
      
      // Sanitize filename
      const sanitizeFilename = (str) => {
        return str
          .replace(/[^a-z0-9]/gi, '_')
          .replace(/_{2,}/g, '_')
          .toLowerCase();
      };
      
      // Set filename with step info
      const descriptionPart = step.description 
        ? sanitizeFilename(step.description).substring(0, 50)
        : 'step';
      const filename = `step_${step.step_number}_${descriptionPart}.json`;
      
      link.href = url;
      link.download = filename;
      
      // Trigger download
      document.body.appendChild(link);
      link.click();
      
      // Cleanup
      document.body.removeChild(link);
      URL.revokeObjectURL(url);
      
      console.log(`✓ Exported JSON: ${filename}`);
      
    } catch (error) {
      console.error('Error exporting JSON:', error);
      alert('Failed to export JSON file. Please try again.');
    }
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        {/* Header */}
        <div className="modal-header">
          <h2>View Selenium Script - Step {step.step_number}</h2>
          <button className="close-button" onClick={onClose}>×</button>
        </div>

        {/* Body */}
        <div className="modal-body">
          {/* Description Section */}
          <div className="section">
            <h3 className="section-title">DESCRIPTION</h3>
            <p className="section-content">{step.description || 'No description'}</p>
          </div>

          {/* Expected Result Section */}
          {step.expected_result && (
            <div className="section">
              <h3 className="section-title">EXPECTED RESULT</h3>
              <p className="section-content">{step.expected_result}</p>
            </div>
          )}

          {/* JSON Commands Section */}
          <div className="section">
            <div className="commands-header">
              <h3 className="section-title">⚙️ JSON Commands (Executed)</h3>
              <span className="command-count">
                {jsonCommands.length} command{jsonCommands.length !== 1 ? 's' : ''}
              </span>
            </div>

            {jsonError ? (
              <div className="error-box">
                <p>{jsonError}</p>
              </div>
            ) : jsonCommands.length === 0 ? (
              <div className="error-box">
                <p>No commands available. Please generate a script first.</p>
              </div>
            ) : (
              <div className="json-commands">
                {jsonCommands.map((command, index) => (
                  <div key={index} className="command-block">
                    <div className="command-header">
                      <span className="command-number">Command {index + 1}</span>
                      <span className="command-action">{command.action || 'unknown'}</span>
                    </div>
                    
                    <div className="command-details">
                      {Object.entries(command).map(([key, value]) => (
                        <div key={key} className="command-field">
                          <span className="field-key">{key}:</span>
                          <span className="field-value">
                            {typeof value === 'object' && value !== null
                              ? JSON.stringify(value, null, 2)
                              : String(value || '')}
                          </span>
                        </div>
                      ))}
                    </div>
                    
                    {command.description && (
                      <div className="command-description">
                        💬 {command.description}
                      </div>
                    )}
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>

        {/* Footer with Export Button */}
        <div className="modal-footer">
          <button 
            className="btn-export" 
            onClick={handleExportJson}
            disabled={!jsonCommands.length || !!jsonError}
            title={jsonCommands.length ? 'Export JSON commands to file' : 'No commands to export'}
          >
            <span className="export-icon">📥</span>
            Export JSON
          </button>
          <button className="btn-close" onClick={onClose}>
            Close
          </button>
        </div>
      </div>
    </div>
  );
}

export default ViewScriptModal;
