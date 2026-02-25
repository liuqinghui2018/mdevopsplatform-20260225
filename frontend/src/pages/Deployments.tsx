import { useEffect, useState } from 'react';
import Layout from '../components/Layout';
import { getDeployments, getServices, getEnvironments, rollbackDeployment } from '../api/services';
import type { Deployment, Service, Environment } from '../types';

function statusBadge(status: string) {
  const colors: Record<string, string> = {
    success: 'bg-green-100 text-green-700',
    failed: 'bg-red-100 text-red-700',
    running: 'bg-blue-100 text-blue-700',
    pending: 'bg-yellow-100 text-yellow-700',
    rolled_back: 'bg-gray-100 text-gray-600',
  };
  return (
    <span className={`px-2 py-0.5 rounded-full text-xs font-medium ${colors[status] || 'bg-gray-100 text-gray-600'}`}>
      {status}
    </span>
  );
}

export default function Deployments() {
  const [deployments, setDeployments] = useState<Deployment[]>([]);
  const [services, setServices] = useState<Service[]>([]);
  const [environments, setEnvironments] = useState<Environment[]>([]);
  const [loading, setLoading] = useState(true);

  const load = () => {
    Promise.all([getDeployments(), getServices(), getEnvironments()])
      .then(([d, s, e]) => { setDeployments(d); setServices(s); setEnvironments(e); })
      .finally(() => setLoading(false));
  };
  useEffect(() => { load(); }, []);

  const serviceMap = Object.fromEntries(services.map(s => [s.id, s.name]));
  const envMap = Object.fromEntries(environments.map(e => [e.id, e.name]));

  const envColors: Record<string, string> = {
    prod: 'bg-red-100 text-red-700',
    staging: 'bg-yellow-100 text-yellow-700',
    dev: 'bg-green-100 text-green-700',
  };

  const handleRollback = async (id: number) => {
    if (confirm('Rollback this deployment?')) {
      await rollbackDeployment(id);
      load();
    }
  };

  return (
    <Layout title="Deployments">
      <div className="space-y-4">
        <p className="text-sm text-gray-500">{deployments.length} deployments</p>

        <div className="bg-white rounded-xl border border-gray-200 shadow-sm overflow-hidden">
          <table className="w-full text-sm">
            <thead className="bg-gray-50 border-b border-gray-200">
              <tr>
                {['#', 'Service', 'Environment', 'Version', 'Status', 'Deployed By', 'Deployed At', 'Actions'].map(h => (
                  <th key={h} className="px-4 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider">{h}</th>
                ))}
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-50">
              {loading ? (
                <tr><td colSpan={8} className="px-4 py-8 text-center text-gray-400">Loading...</td></tr>
              ) : deployments.map((d) => {
                const envName = envMap[d.environment_id] || `#${d.environment_id}`;
                return (
                  <tr key={d.id} className="hover:bg-gray-50">
                    <td className="px-4 py-3 font-medium text-gray-800">#{d.id}</td>
                    <td className="px-4 py-3 text-gray-600 font-medium">{serviceMap[d.service_id] || `#${d.service_id}`}</td>
                    <td className="px-4 py-3">
                      <span className={`px-2 py-0.5 rounded text-xs font-medium ${envColors[envName] || 'bg-gray-100 text-gray-600'}`}>{envName}</span>
                    </td>
                    <td className="px-4 py-3 text-gray-500 font-mono text-xs">{d.version || '—'}</td>
                    <td className="px-4 py-3">{statusBadge(d.status)}</td>
                    <td className="px-4 py-3 text-gray-500">{d.deployed_by || '—'}</td>
                    <td className="px-4 py-3 text-gray-400">{new Date(d.deployed_at).toLocaleString()}</td>
                    <td className="px-4 py-3">
                      {d.status === 'success' && (
                        <button onClick={() => handleRollback(d.id)} className="text-orange-500 hover:text-orange-700 text-xs font-medium">↩ Rollback</button>
                      )}
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>
    </Layout>
  );
}
