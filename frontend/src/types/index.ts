export interface User {
  id: number;
  username: string;
  email: string;
  role: string;
  is_active: boolean;
  created_at: string;
}

export interface Service {
  id: number;
  name: string;
  description?: string;
  repository_url?: string;
  language?: string;
  owner?: string;
  created_at: string;
}

export interface Environment {
  id: number;
  name: string;
  description?: string;
  created_at: string;
}

export interface Pipeline {
  id: number;
  name: string;
  service_id: number;
  trigger: string;
  status: string;
  created_at: string;
}

export interface Build {
  id: number;
  pipeline_id: number;
  commit_sha?: string;
  branch?: string;
  status: string;
  started_at?: string;
  finished_at?: string;
  logs?: string;
}

export interface Deployment {
  id: number;
  build_id: number;
  service_id: number;
  environment_id: number;
  status: string;
  deployed_by?: string;
  deployed_at: string;
  version?: string;
}

export interface DashboardStats {
  total_pipelines: number;
  total_builds: number;
  successful_deployments: number;
  failed_builds: number;
  recent_builds: Build[];
  recent_deployments: Deployment[];
}
