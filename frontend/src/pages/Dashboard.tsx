import { useEffect, useState } from 'react';
import Layout from '../components/Layout';
import StatCard from '../components/StatCard';
import { getDashboardStats } from '../api/services';
import type { DashboardStats } from '../types';

function statusBadge(status: string) {
  const colors: Record<string, string> = {
    success: 'bg-green-100 text-green-700',
    failed: 'bg-red-100 text-red-700',
    running: 'bg-blue-100 text-blue-700',
    pending: 'bg-yellow-100 text-yellow-700',
    rolled_back: 'bg-gray-100 text-gray-700',
  };
  return (
    <span className={`px-2 py-0.5 rounded-full text-xs font-medium ${colors[status] || 'bg-gray-100 text-gray-600'}`}>
      {status}
    </span>
  );
}

export default function Dashboard() {
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getDashboardStats()
      .then(setStats)
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <Layout title="Dashboard"><div className="text-gray-400">Loading...</div></Layout>;
  if (!stats) return <Layout title="Dashboard"><div className="text-red-500">Failed to load stats</div></Layout>;

  return (
    <Layout title="Dashboard">
      <div className="space-y-6">
        {/* Stat cards */}
        <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-4">
          <StatCard title="Total Pipelines" value={stats.total_pipelines} icon="⚡" color="bg-blue-50" subtitle="Active CI/CD pipelines" />
          <StatCard title="Total Builds" value={stats.total_builds} icon="🔨" color="bg-purple-50" subtitle="All time builds" />
          <StatCard title="Successful Deployments" value={stats.successful_deployments} icon="✅" color="bg-green-50" subtitle="Completed successfully" />
          <StatCard title="Failed Builds" value={stats.failed_builds} icon="❌" color="bg-red-50" subtitle="Require attention" />
        </div>

        <div className="grid grid-cols-1 xl:grid-cols-2 gap-6">
          {/* Recent Builds */}
          <div className="bg-white rounded-xl border border-gray-200 shadow-sm">
            <div className="px-6 py-4 border-b border-gray-100">
              <h3 className="font-semibold text-gray-800">Recent Builds</h3>
            </div>
            <div className="divide-y divide-gray-50">
              {stats.recent_builds.map((build) => (
                <div key={build.id} className="px-6 py-3 flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium text-gray-800">Build #{build.id}</p>
                    <p className="text-xs text-gray-400">{build.branch} · {build.commit_sha?.slice(0, 7)}</p>
                  </div>
                  {statusBadge(build.status)}
                </div>
              ))}
            </div>
          </div>

          {/* Recent Deployments */}
          <div className="bg-white rounded-xl border border-gray-200 shadow-sm">
            <div className="px-6 py-4 border-b border-gray-100">
              <h3 className="font-semibold text-gray-800">Recent Deployments</h3>
            </div>
            <div className="divide-y divide-gray-50">
              {stats.recent_deployments.map((dep) => (
                <div key={dep.id} className="px-6 py-3 flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium text-gray-800">Deployment #{dep.id}</p>
                    <p className="text-xs text-gray-400">{dep.version} · by {dep.deployed_by}</p>
                  </div>
                  {statusBadge(dep.status)}
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </Layout>
  );
}
