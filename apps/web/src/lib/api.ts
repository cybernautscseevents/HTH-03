/**
 * ClinScribe AI — API Client
 * Centralized API communication layer for the frontend.
 */

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

class ApiClient {
  private token: string | null = null;

  setToken(token: string) {
    this.token = token;
    if (typeof window !== 'undefined') {
      localStorage.setItem('clinscribe_token', token);
    }
  }

  getToken(): string | null {
    if (this.token) return this.token;
    if (typeof window !== 'undefined') {
      this.token = localStorage.getItem('clinscribe_token');
    }
    return this.token;
  }

  clearToken() {
    this.token = null;
    if (typeof window !== 'undefined') {
      localStorage.removeItem('clinscribe_token');
    }
  }

  private async fetch(path: string, options: RequestInit = {}): Promise<any> {
    const url = `${API_BASE}${path}`;
    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
      ...(options.headers as Record<string, string> || {}),
    };

    const token = this.getToken();
    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }

    const response = await fetch(url, {
      ...options,
      headers,
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'Request failed' }));
      throw new Error(error.detail || `HTTP ${response.status}`);
    }

    return response.json();
  }

  // Auth
  async login(email: string, password: string) {
    const data = await this.fetch('/auth/login', {
      method: 'POST',
      body: JSON.stringify({ email, password }),
    });
    this.setToken(data.access_token);
    return data;
  }

  async getMe() {
    return this.fetch('/auth/me');
  }

  // Patients
  async getPatients(search?: string) {
    const params = search ? `?search=${encodeURIComponent(search)}` : '';
    return this.fetch(`/patients${params}`);
  }

  async getPatient(id: string) {
    return this.fetch(`/patients/${id}`);
  }

  // Consultations
  async createConsultation(data: any) {
    return this.fetch('/consultations', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async listConsultations(patientId?: string) {
    const params = patientId ? `?patient_id=${patientId}` : '';
    return this.fetch(`/consultations${params}`);
  }

  async startConsultation(id: string) {
    return this.fetch(`/consultations/${id}/start`, { method: 'POST' });
  }

  async stopConsultation(id: string) {
    return this.fetch(`/consultations/${id}/stop`, { method: 'POST' });
  }

  // Transcription
  async transcribe(consultationId: string) {
    return this.fetch('/audio/transcribe', {
      method: 'POST',
      body: JSON.stringify({ consultation_id: consultationId }),
    });
  }

  async getTranscript(consultationId: string) {
    return this.fetch(`/consultations/${consultationId}/transcript`);
  }

  // Clinical
  async extractClinical(consultationId: string) {
    return this.fetch('/clinical/extract', {
      method: 'POST',
      body: JSON.stringify({ consultation_id: consultationId }),
    });
  }

  async generateNote(consultationId: string) {
    return this.fetch('/clinical/generate-note', {
      method: 'POST',
      body: JSON.stringify({ consultation_id: consultationId }),
    });
  }

  async getClinicalNote(noteId: string) {
    return this.fetch(`/clinical/${noteId}`);
  }

  async updateClinicalNote(noteId: string, content: any, changeReason?: string) {
    return this.fetch(`/clinical/${noteId}`, {
      method: 'PUT',
      body: JSON.stringify({ content, change_reason: changeReason }),
    });
  }

  async approveClinicalNote(noteId: string, action: 'approve' | 'reject', reason?: string) {
    return this.fetch(`/clinical/${noteId}/approve`, {
      method: 'POST',
      body: JSON.stringify({ action, reason }),
    });
  }

  async validateClinical(consultationId: string) {
    return this.fetch('/clinical/validate', {
      method: 'POST',
      body: JSON.stringify({ consultation_id: consultationId }),
    });
  }

  // Evidence
  async getEvidence(noteId: string, fieldPath?: string) {
    const params = fieldPath ? `?field_path=${encodeURIComponent(fieldPath)}` : '';
    return this.fetch(`/clinical/${noteId}/evidence${params}`);
  }

  // Patient Summary
  async getPatientSummary(consultationId: string) {
    return this.fetch(`/consultations/${consultationId}/patient-summary`);
  }

  // Timeline
  async getTimeline(patientId: string) {
    return this.fetch(`/patients/${patientId}/timeline`);
  }

  // FHIR
  async getFHIRExport(consultationId: string) {
    return this.fetch(`/encounters/${consultationId}/fhir`);
  }

  // Evaluation
  async getEvaluationMetrics() {
    return this.fetch('/evaluation/metrics');
  }

  // Privacy
  async getPrivacy() {
    return this.fetch('/privacy');
  }

  // Settings
  async getSettings() {
    return this.fetch('/settings');
  }

  // Templates
  async getTemplates() {
    return this.fetch('/templates');
  }

  // Demo
  async getDemoConsultations() {
    return this.fetch('/demo/consultations');
  }

  async runDemoPipeline(consultationId: string = 'consult-demo-001') {
    return this.fetch('/demo/run-pipeline', {
      method: 'POST',
      body: JSON.stringify({ consultation_id: consultationId }),
    });
  }

  // Health
  async healthCheck() {
    return this.fetch('/health');
  }
}

export const api = new ApiClient();
export default api;
