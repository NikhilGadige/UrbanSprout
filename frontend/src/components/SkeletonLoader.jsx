import React from 'react';

export function PriceStatsSkeleton() {
  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-6 animate-pulse w-full">
      {[1, 2, 3].map((i) => (
        <div key={i} className="glass-panel p-6 rounded-xl border border-forest-700">
          <div className="h-4 w-1/3 bg-forest-700 rounded mb-4"></div>
          <div className="h-8 w-2/3 bg-forest-600 rounded mb-2"></div>
          <div className="h-3 w-1/2 bg-forest-700 rounded"></div>
        </div>
      ))}
    </div>
  );
}

export function PriceChartSkeleton() {
  return (
    <div className="glass-panel p-6 rounded-xl border border-forest-700 w-full animate-pulse">
      <div className="flex justify-between items-center mb-6">
        <div className="h-6 w-1/4 bg-forest-700 rounded"></div>
        <div className="h-4 w-1/6 bg-forest-700 rounded"></div>
      </div>
      <div className="h-64 w-full bg-forest-800 rounded-lg flex items-end p-4 gap-4">
        {[20, 45, 30, 80, 50, 65, 40, 90, 55, 70].map((h, i) => (
          <div 
            key={i} 
            className="flex-1 bg-forest-700 rounded-t"
            style={{ height: `${h}%` }}
          ></div>
        ))}
      </div>
    </div>
  );
}

export function PriceTableSkeleton() {
  return (
    <div className="glass-panel rounded-xl border border-forest-700 w-full overflow-hidden animate-pulse">
      <div className="bg-forest-900 px-6 py-4 border-b border-forest-700 flex gap-4">
        {[1, 2, 3, 4, 5].map((i) => (
          <div key={i} className="h-4 flex-1 bg-forest-800 rounded"></div>
        ))}
      </div>
      <div className="divide-y divide-forest-700 p-6 space-y-4">
        {[1, 2, 3, 4, 5].map((i) => (
          <div key={i} className="flex gap-4">
            {[1, 2, 3, 4, 5].map((j) => (
              <div key={j} className="h-4 flex-1 bg-forest-800 rounded"></div>
            ))}
          </div>
        ))}
      </div>
    </div>
  );
}

export function DiseaseResultSkeleton() {
  return (
    <div className="glass-panel p-6 rounded-xl border border-forest-700 w-full space-y-6 animate-pulse">
      <div className="flex flex-col md:flex-row gap-6">
        <div className="w-full md:w-1/3 aspect-square bg-forest-800 rounded-xl"></div>
        <div className="flex-1 space-y-4 py-2">
          <div className="h-4 w-1/4 bg-forest-700 rounded"></div>
          <div className="h-8 w-3/4 bg-forest-600 rounded"></div>
          <div className="h-6 w-1/3 bg-forest-700 rounded"></div>
        </div>
      </div>
      <div className="space-y-4 border-t border-forest-700 pt-6">
        <div className="h-6 w-1/3 bg-forest-700 rounded"></div>
        <div className="space-y-2">
          <div className="h-4 w-full bg-forest-800 rounded"></div>
          <div className="h-4 w-5/6 bg-forest-800 rounded"></div>
          <div className="h-4 w-4/5 bg-forest-800 rounded"></div>
        </div>
      </div>
    </div>
  );
}
