import React from 'react';

const SettingsPanel = ({ settings, setSettings, showSettings }) => {
  if (!showSettings) return null;

  return (
    <div className="mt-4 p-4 bg-gray-50 rounded-xl space-y-3">
      <div>
        <label className="text-sm font-medium text-gray-700">
          Temperature: {settings.temperature}
        </label>
        <input
          type="range"
          min="0"
          max="1"
          step="0.1"
          value={settings.temperature}
          onChange={(e) => setSettings({...settings, temperature: parseFloat(e.target.value)})}
          className="w-full"
        />
      </div>
      <div>
        <label className="text-sm font-medium text-gray-700">
          Max Tokens: {settings.maxTokens}
        </label>
        <input
          type="range"
          min="100"
          max="4096"
          step="100"
          value={settings.maxTokens}
          onChange={(e) => setSettings({...settings, maxTokens: parseInt(e.target.value)})}
          className="w-full"
        />
      </div>
      <div>
        <label className="text-sm font-medium text-gray-700">
          Search K: {settings.searchK}
        </label>
        <input
          type="range"
          min="1"
          max="10"
          step="1"
          value={settings.searchK}
          onChange={(e) => setSettings({...settings, searchK: parseInt(e.target.value)})}
          className="w-full"
        />
      </div>
    </div>
  );
};

export default SettingsPanel;
