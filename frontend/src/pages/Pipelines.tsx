import { useEffect, useState } from 'react';
import Layout from '../components/Layout';
import { getPipelines, getServices, triggerPipeline, deletePipeline, createPipeline } from '../api/services';
import type { Pipeline, Service } from '../types';

export default function Pipelines() {
  const [pipelines, setPipelines] = useState<Pipeline[]>([]);
  const [services, setServices] = useState<Service[]>([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [form, setForm] = useState({ name: '', service_id: '', trigger: 'push', status: 'active' });
  const [triggering, setTriggering] = useState<number | null>(null);

  const load = () => {
    Promise.all([getPipelines(), getServices()])
      .then(([p, s]) => { setPipelines(p); setServices(s); })
      .finally(() => setLoading(false));
  };
  useEffect(() => { load(); }, []);

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault();
    await createPipeline({ ...form, service_id: Number(form.service_id) });
    setForm({ name: '', service_id: '', trigger: 'push', status: 'active' });
    setShowForm(false);
    load();
  };

  const handleTrigger = async (id: number) => {
    setTriggering(id);
    try {
      await triggerPipeline(id);
      alert('Pipeline triggered successfully!');
      load();
    } finally {
      setTriggering(null);
    }
  };

  const serviceMap = Object.fromEntries(services.map(s => [s.id, s.name]));

  const triggerColors: Record<string, string> = {
    push: 'bg-blue-50 text-blue-700',
    pr: 'bg-purple-50 text-purple-700',
    manual: 'bg-gray-100 text-gray-700',
    schedule: 'bg-orange-50 text-orange-700',
  };

  return (
    <Layout title="Pipelines">
      <div className="space-y-4">
        <div className="flex justify-between items-center">
          <p className="text-sm text-gray-500">{pipelines.length} pipelines</p>
          <button onClick={() => setShowForm(!showForm)} className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg text-sm font-medium transition-colors">
            + New Pipeline
          </button>
        </div>

        {showForm && (
          <form onSubmit={handleCreate} className="bg-white rounded-xl border border-gray-200 p-6 space-y-4">
            <h3 className="font-semibold text-gray-800">New Pipeline</h3>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Name</label>
                <input className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 outline-none" value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} required />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Service</label>
                <select className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 outline-none" value={form.service_id} onChange={(e) => setForm({ ...form, service_id: e.target.value })} required>
                  <option value="">Select service...</option>
                  {services.map(s => <option key={s.id} value={s.id}>{s.name}</option>)}
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Trigger</label>
                <select className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 outline-none" value={form.trigger} onChange={(e) => setForm({ ...form, trigger: e.target.value })}>
                  {['push', 'pr', 'manual', 'schedule'].map(t => <option key={t} value={t}>{t}</option>)}
                </select>
              </div>
            </div>
            <div className="flex gap-2">
              <button type="submit" className="bg-blue-600 text-white px-4 py-2 rounded-lg text-sm">Create</button>
              <button type="button" onClick={() => setShowForm(false)} className="bg-gray-100 text-gray-700 px-4 py-2 rounded-lg text-sm">Cancel</button>
            </div>
          </form>
        )}

        <div className="bg-white rounded-xl border border-gray-200 shadow-sm overflow-hidden">
          <table className="w-full text-sm">
            <thead className="bg-gray-50 border-b border-gray-200">
              <tr>
                {['Name', 'Service', 'Trigger', 'Status', 'Created', 'Actions'].map(h => (
                  <th key={h} className="px-4 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider">{h}</th>
                ))}
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-50">
              {loading ? (
                <tr><td colSpan={6} className="px-4 py-8 text-center text-gray-400">Loading...</td></tr>
              ) : pipelines.map((p) => (
                <tr key={p.id} className="hover:bg-gray-50">
                  <td className="px-4 py-3 font-medium text-gray-800">{p.name}</td>
                  <td className="px-4 py-3 text-gray-500">{serviceMap[p.service_id] || `#${p.service_id}`}</td>
                  <td className="px-4 py-3">
                    <span className={`px-2 py-0.5 rounded text-xs font-medium ${triggerColors[p.trigger] || 'bg-gray-100 text-gray-600'}`}>{p.trigger}</span>
                  </td>
                  <td className="px-4 py-3">
                    <span className={`px-2 py-0.5 rounded-full text-xs font-medium ${p.status === 'active' ? 'bg-green-100 text-green-700' : 'bg-gray-100 text-gray-600'}`}>{p.status}</span>
                  </td>
                  <td className="px-4 py-3 text-gray-400">{new Date(p.created_at).toLocaleDateString()}</td>
                  <td className="px-4 py-3 flex gap-2">
                    <button
                      onClick={() => handleTrigger(p.id)}
                      disabled={triggering === p.id}
                      className="text-blue-600 hover:text-blue-800 text-xs font-medium disabled:opacity-50"
                    >
                      {triggering === p.id ? 'Running...' : '▶ Run'}
                    </button>
                    <button onClick={() => { if(confirm('Delete?')) deletePipeline(p.id).then(load); }} className="text-red-500 hover:text-red-700 text-xs font-medium">Delete</button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </Layout>
  );
}
