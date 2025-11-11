import './App.css';

function App() {
  return (
    <div className="app-container">
      <div className="toolbar">
        <h1>Strategy Builder</h1>
        <div>
          <button>Save</button>
          <button>Load</button>
        </div>
      </div>
      <div className="main-content">
        <div className="palette">
          <h2>Palette</h2>
          {/* Components will go here */}
        </div>
        <div className="canvas">
          <h2>Canvas</h2>
          {/* Drag-and-drop area will go here */}
        </div>
        <div className="settings">
          <h2>Settings & Preview</h2>
          {/* Settings and preview will go here */}
        </div>
      </div>
    </div>
  );
}

export default App;
