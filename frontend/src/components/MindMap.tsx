import React, { useState } from 'react';

interface MindMapNode {
  name: string;
  children?: MindMapNode[];
}

interface MindMapProps {
  data: MindMapNode | null;
}

const MindMap: React.FC<MindMapProps> = ({ data }) => {
  const [expandedNodes, setExpandedNodes] = useState<Record<string, boolean>>({
    'Foundations': true,
    'Applications': true,
    'Assessments': true,
  });

  if (!data) {
    return (
      <div className="flex items-center justify-center h-80 bg-white border-2 border-dashed border-slate-200 rounded-kids">
        <span className="text-slate-400 font-bold">✨ No mind map data available</span>
      </div>
    );
  }

  const toggleNode = (name: string) => {
    setExpandedNodes(prev => ({
      ...prev,
      [name]: !prev[name]
    }));
  };

  // SVG coordinates setup (Radial placement for kid simplicity and premium looks)
  const width = 800;
  const height = 500;
  const cx = width / 2;
  const cy = height / 2;

  const branches = data.children || [];
  const radius = 160;

  return (
    <div className="bg-gradient-to-br from-indigo-50 to-purple-50 p-6 rounded-kids border-2 border-brand-200 shadow-inner relative overflow-hidden">
      <div className="absolute top-4 left-4 bg-white/80 px-3 py-1.5 rounded-full border border-indigo-100 text-xs font-bold text-slate-500 shadow-sm">
        💡 Pro Tip: Click branches to toggle sub-details!
      </div>
      <div className="w-full overflow-x-auto">
        <svg viewBox={`0 0 ${width} ${height}`} className="w-full max-w-[800px] h-auto mx-auto block">
          {/* Defs for gradients & shadows */}
          <defs>
            <filter id="shadow" x="-10%" y="-10%" width="120%" height="120%">
              <feDropShadow dx="0" dy="4" stdDeviation="4" floodColor="#8b5cf6" floodOpacity="0.15" />
            </filter>
            <linearGradient id="centerGrad" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stopColor="#8b5cf6" />
              <stop offset="100%" stopColor="#a855f7" />
            </linearGradient>
            <linearGradient id="branchGrad" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stopColor="#06b6d4" />
              <stop offset="100%" stopColor="#3b82f6" />
            </linearGradient>
            <linearGradient id="leafGrad" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stopColor="#f59e0b" />
              <stop offset="100%" stopColor="#f97316" />
            </linearGradient>
          </defs>

          {/* Draw connecting lines first */}
          {branches.map((b, i) => {
            const angle = (i * 2 * Math.PI) / branches.length;
            const bx = cx + radius * Math.cos(angle);
            const by = cy + radius * Math.sin(angle);
            
            return (
              <g key={`lines-${i}`}>
                {/* Center to Branch */}
                <line 
                  x1={cx} y1={cy} x2={bx} y2={by} 
                  stroke="#c084fc" strokeWidth="4" 
                  strokeDasharray="4 4"
                />
                
                {/* Branch to Sub-branches */}
                {expandedNodes[b.name] && b.children?.map((sub, j) => {
                  const subAngle = angle + (j - (b.children!.length - 1) / 2) * 0.35;
                  const sx = cx + (radius + 90) * Math.cos(subAngle);
                  const sy = cy + (radius + 90) * Math.sin(subAngle);
                  
                  return (
                    <line 
                      key={`line-sub-${i}-${j}`}
                      x1={bx} y1={by} x2={sx} y2={sy} 
                      stroke="#22d3ee" strokeWidth="3" 
                    />
                  );
                })}
              </g>
            );
          })}

          {/* Draw Central Node */}
          <g transform={`translate(${cx}, ${cy})`} filter="url(#shadow)" className="cursor-pointer">
            <circle r="60" fill="url(#centerGrad)" />
            <text 
              textAnchor="middle" dy="5" 
              fill="white" className="font-bold text-sm select-none"
              style={{ fontFamily: "'Fredoka One', cursive" }}
            >
              {data.name.length > 15 ? `${data.name.slice(0, 12)}...` : data.name}
            </text>
          </g>

          {/* Draw Branch and Leaf Nodes */}
          {branches.map((b, i) => {
            const angle = (i * 2 * Math.PI) / branches.length;
            const bx = cx + radius * Math.cos(angle);
            const by = cy + radius * Math.sin(angle);
            const isExpanded = expandedNodes[b.name];
            
            return (
              <g key={`nodes-${i}`}>
                {/* Branch Circle */}
                <g 
                  transform={`translate(${bx}, ${by})`} 
                  onClick={() => toggleNode(b.name)}
                  className="cursor-pointer select-none transition transform hover:scale-105 active:scale-95"
                >
                  <circle r="40" fill="url(#branchGrad)" stroke="#ffffff" strokeWidth="2" filter="url(#shadow)" />
                  <text 
                    textAnchor="middle" dy="4" 
                    fill="white" className="font-bold text-xs"
                  >
                    {b.name}
                  </text>
                </g>

                {/* Sub-branch Leaf Circles */}
                {isExpanded && b.children?.map((sub, j) => {
                  const subAngle = angle + (j - (b.children!.length - 1) / 2) * 0.35;
                  const sx = cx + (radius + 90) * Math.cos(subAngle);
                  const sy = cy + (radius + 90) * Math.sin(subAngle);
                  
                  return (
                    <g 
                      key={`leaf-${i}-${j}`}
                      transform={`translate(${sx}, ${sy})`} 
                      className="cursor-default select-none animate-bounce"
                      style={{ animationDuration: `${2 + (j % 3)}s` }}
                    >
                      <circle r="25" fill="url(#leafGrad)" stroke="#ffffff" strokeWidth="1.5" filter="url(#shadow)" />
                      <text 
                        textAnchor="middle" dy="3" 
                        fill="white" className="font-semibold" style={{ fontSize: '9px' }}
                      >
                        {sub.name.length > 10 ? `${sub.name.slice(0, 8)}..` : sub.name}
                      </text>
                    </g>
                  );
                })}
              </g>
            );
          })}
        </svg>
      </div>
    </div>
  );
};

export default MindMap;
