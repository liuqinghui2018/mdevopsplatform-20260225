import { useEffect, useState } from 'react';
import Layout from '../components/Layout';
import { getBuilds } from '../api/services';
import type { Build } from '../types';

function statusBadge(status: string) {
  const colors: Record<string, string> = {
    success: 'bg-green-100 text-green-700',
    failed: 'bg-red-100 text-red-700',
    running: 'bg-blue-100 text-blue-700',
    pending: 'bg-yellow-100 text-yellow-700',
  };
  return (
    <span className={`px-2 py-0.5 rounded-full text-xs font-medium ${colors[status] || 'bg-gray-100 text-gray-600'}`}>
      {status}
    </span>
  );
}

export default function Builds() {
  const [builds, setBuilds] = useState<Build[]>([]);
  const [loading, setLoading] = useState(true);
  const [selected, setSelected] = useState<Build | null>(null);

  useEffect(() => {
    getBuilds().then(setBuilds).finally(() => setLoading(false));
  }, []);

  return (
    <Layout title="Build History">
      <div className="space-y-4">
        <p className="text-sm text-gray-500">{builds.length} builds total</p>

        <div className="grid grid-cols-1 xl:grid-cols-3 gap-6">
          <div className="xl:col-span-2 bg-white rounded-xl border border-gray-200 shadow-sm overflow-hidden">
            <table className="w-full text-sm">
              <thead className="bg-gray-50 border-b border-gray-200">
                <tr>
                  {['#', 'Pipeline', 'Branch', 'Commit', 'Status', 'Duration', 'Started'].map(h => (
                    <th key={h} className="px-4 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider">{h}</th>
                  ))}
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-50">
                {loading ? (
                  <tr><td colSpan={7} className="px-4 py-8 text-center text-gray-400">Loading...</td></tr>
                ) : builds.map((b) => {
                  const duration = b.started_at && b.finished_at
                    ? Math.round((new Date(b.finished_at).getTime() - new Date(b.started_at).getTime()) / 1000) + 's'
                    : b.status === 'running' ? 'Running...' : '—';
                  return (
                    <tr key={b.id} className="hover:bg-gray-50 cursor-pointer" onClick={() => setSelected(b)}>
                      <td className="px-4 py-3 font-medium text-gray-800">#{b.id}</td>
                      <td className="px-4 py-3 text-gray-500">#{b.pipeline_id}</td>
                      <td className="px-4 py-3 text-gray-500">{b.branch || '—'}</td>
                      <td className="px-4 py-3 text-gray-400 font-mono text-xs">{b.commit_sha?.slice(0, 7) || '—'}</td>
                      <td className="px-4 py-3">{statusBadge(b.status)}</td>
                      <td className="px-4 py-3 text-gray-400">{duration}</td>
                      <td className="px-4 py-3 text-gray-400">{b.started_at ? new Date(b.started_at).toLocaleDateString() : '—'}</td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>

          {/* Log viewer */}
          <div className="bg-white rounded-xl border border-gray-200 shadow-sm">
            <div className="px-4 py-3 border-b border-gray-100">
              <h3 className="font-semibold text-gray-800 text-sm">
                {selected ? `Build #${selected.id} Logs` : 'Select a build to view logs'}
              </h3>
            </div>
            <div className="p-4">
              {selected ? (
                <pre className="text-xs text-gray-600 bg-gray-50 rounded-lg p-3 overflow-auto max-h-64 whitespace-pre-wrap">
                  {selected.logs || 'No logs available'}
                </pre>
              ) : (
                <p className="text-sm text-gray-400 text-center py-8">Click a build row to view its logs</p>
              )}
            </div>
          </div>
        </div>
      </div>
    </Layout>
  );
}
