import React from 'react'
import { createRoot } from 'react-dom/client'

const root = document.getElementById("root");
if (root) {
  const reactRoot = createRoot(root);
  reactRoot.render(
    React.createElement('div', null, 
      React.createElement('h1', null, 'React is working!'),
      React.createElement('p', null, 'If you see this, React is rendering correctly.')
    )
  );
} else {
  console.error("Root element not found");
} 