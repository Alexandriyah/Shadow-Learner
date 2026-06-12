import React from 'react';

interface FlowchartProps {
  mermaidCode: string;
}

const Flowchart: React.FC<FlowchartProps> = ({ mermaidCode }) => {
  // Parse simple flowchart nodes
  // Expected structure example:
  // graph TD
  //   Sunlight --> Leaf
  //   Water --> Leaf
  // Or simple lists
  const parseMermaid = (code: string): string[] => {
    if (!code) return ['Start', 'Learn', 'Practice', 'Master'];
    
    const steps: string[] = [];
    const lines = code.split('\n');
    
    // Look for arrows or definitions
    lines.forEach(line => {
      const match = line.match(/(?:[\w]+)\[([^\]]+)\]|([\w]+)\s*-->\s*([\w]+)/);
      if (match) {
        if (match[1]) {
          // Found A[Text label]
          steps.push(match[1]);
        } else if (match[2] && match[3]) {
          // Found A --> B
          const from = match[2].trim();
          const to = match[3].trim();
          if (!steps.includes(from) && from !== 'Start' && from !== 'graph') steps.push(from);
          if (!steps.includes(to)) steps.push(to);
        }
      } else {
        // Fallback: parse plain words
        const clean = line.replace(/graph TD|-->|\[|\]/g, '').trim();
        if (clean && clean.length > 2) {
          steps.push(clean);
        }
      }
    });
    
    // Deduplicate and filter out formatting noise
    return Array.from(new Set(steps)).filter(s => s && s.toLowerCase() !== 'graph td');
  };

  const steps = parseMermaid(mermaidCode);

  return (
    <div className="bg-white p-8 rounded-kids border-2 border-indigo-100 shadow-md">
      <h3 className="brand-title text-xl text-brand-600 mb-6 flex items-center gap-2">
        🗺️ Learning Pathway Map
      </h3>
      
      <div className="flex flex-col md:flex-row items-center justify-center gap-4 flex-wrap">
        {steps.map((step, index) => {
          // Clean name
          const label = step.split('[')[0].replace(/["']/g, '').trim();
          
          return (
            <React.Fragment key={`step-${index}`}>
              {/* Step Card */}
              <div 
                className="sparkle-hover flex flex-col items-center justify-center p-5 min-w-[150px] bg-gradient-to-br from-white to-slate-50 border-2 border-slate-200 rounded-2xl shadow-sm text-center transition duration-200 cursor-default"
                style={{
                  borderLeftColor: index % 3 === 0 ? '#8b5cf6' : index % 3 === 1 ? '#06b6d4' : '#f59e0b',
                  borderLeftWidth: '6px'
                }}
              >
                <div className="w-8 h-8 rounded-full bg-slate-100 flex items-center justify-center text-xs font-bold text-slate-500 mb-2">
                  {index + 1}
                </div>
                <div className="font-bold text-slate-700 text-sm">
                  {label}
                </div>
              </div>
              
              {/* Connector Arrow */}
              {index < steps.length - 1 && (
                <div className="flex items-center justify-center text-brand-300 font-bold text-2xl py-2 md:py-0">
                  {/* Desktop arrow / mobile arrow */}
                  <span className="hidden md:inline">➡️</span>
                  <span className="inline md:hidden">⬇️</span>
                </div>
              )}
            </React.Fragment>
          );
        })}
      </div>
    </div>
  );
};

export default Flowchart;
