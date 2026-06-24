import client from './client';
import type { DashboardStats, Service, Environment, Pipeline, Build, Deployment, User } from '../types';

// Auth
export const login = async (username: string, password: string): Promise<string> => {
  const form = new URLSearchParams();
  form.append('username', username);
  form.append('password', password);
  const res = await client.post('/api/auth/login', form, {
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
  });
  return res.data.access_token;
};

// Dashboard
export const getDashboardStats = (): Promise<DashboardStats> =>
  client.get('/api/dashboard/stats').then((r) => r.data);

// Services
export const getServices = (): Promise<Service[]> => client.get('/api/services/').then((r) => r.data);
export const createService = (data: Partial<Service>): Promise<Service> => client.post('/api/services/', data).then((r) => r.data);
export const deleteService = (id: number): Promise<void> => client.delete(`/api/services/${id}`).then((r) => r.data);

// Environments
export const getEnvironments = (): Promise<Environment[]> => client.get('/api/environments/').then((r) => r.data);
export const createEnvironment = (data: Partial<Environment>): Promise<Environment> => client.post('/api/environments/', data).then((r) => r.data);
export const deleteEnvironment = (id: number): Promise<void> => client.delete(`/api/environments/${id}`).then((r) => r.data);

// Pipelines
export const getPipelines = (): Promise<Pipeline[]> => client.get('/api/pipelines/').then((r) => r.data);
export const createPipeline = (data: Partial<Pipeline>): Promise<Pipeline> => client.post('/api/pipelines/', data).then((r) => r.data);
export const deletePipeline = (id: number): Promise<void> => client.delete(`/api/pipelines/${id}`).then((r) => r.data);
export const triggerPipeline = (id: number): Promise<Build> => client.post(`/api/pipelines/${id}/trigger`).then((r) => r.data);

// Builds
export const getBuilds = (): Promise<Build[]> => client.get('/api/builds/').then((r) => r.data);

// Deployments
export const getDeployments = (): Promise<Deployment[]> => client.get('/api/deployments/').then((r) => r.data);
export const rollbackDeployment = (id: number): Promise<Deployment> => client.post(`/api/deployments/${id}/rollback`).then((r) => r.data);

// Users
export const getUsers = (): Promise<User[]> => client.get('/api/users/').then((r) => r.data);
