import type {
  ApiError,
  DetectionResponse,
  HealthResponse,
  HistoryItem,
  HistoryListResponse,
  MetricsResponse,
  SignGroupSummary,
  SignItem,
  SignListResponse,
} from './types';

const API_BASE = '/api/v1';

async function handleResponse<T>(res: Response): Promise<T> {
  if (!res.ok) {
    let errorData: any = null;
    try {
      errorData = await res.json();
    } catch {
      // Non-JSON error
    }

    const error: ApiError = {
      status: res.status,
      code: errorData?.error?.code || 'UNKNOWN_ERROR',
      message: errorData?.error?.message || `Lỗi máy chủ (${res.status})`,
      request_id: errorData?.request_id || res.headers.get('X-Request-ID') || undefined,
    };
    throw error;
  }
  return res.json() as Promise<T>;
}

export const api = {
  async getHealth(): Promise<HealthResponse> {
    const res = await fetch(`${API_BASE}/health`);
    return handleResponse<HealthResponse>(res);
  },

  async detectSigns(
    file: File,
    confidence?: number,
    saveHistory: boolean = false
  ): Promise<DetectionResponse> {
    const formData = new FormData();
    formData.append('file', file);
    if (confidence !== undefined) {
      formData.append('confidence', confidence.toString());
    }
    formData.append('save_history', saveHistory ? 'true' : 'false');

    const res = await fetch(`${API_BASE}/detections`, {
      method: 'POST',
      body: formData,
    });
    return handleResponse<DetectionResponse>(res);
  },

  getAnnotatedImageUrl(requestId: string): string {
    return `${API_BASE}/detections/${requestId}/image`;
  },

  async listSigns(params?: {
    q?: string;
    group?: string;
    page?: number;
    page_size?: number;
  }): Promise<SignListResponse> {
    const query = new URLSearchParams();
    if (params?.q) query.append('q', params.q);
    if (params?.group) query.append('group', params.group);
    if (params?.page) query.append('page', params.page.toString());
    if (params?.page_size) query.append('page_size', params.page_size.toString());

    const queryString = query.toString() ? `?${query.toString()}` : '';
    const res = await fetch(`${API_BASE}/signs${queryString}`);
    return handleResponse<SignListResponse>(res);
  },

  async getSignGroups(): Promise<SignGroupSummary[]> {
    const res = await fetch(`${API_BASE}/signs/groups`);
    return handleResponse<SignGroupSummary[]>(res);
  },

  async getSignById(id: number): Promise<SignItem> {
    const res = await fetch(`${API_BASE}/signs/${id}`);
    return handleResponse<SignItem>(res);
  },

  async getSignByCode(code: string): Promise<SignItem> {
    const res = await fetch(`${API_BASE}/signs/code/${encodeURIComponent(code)}`);
    return handleResponse<SignItem>(res);
  },

  async getHistory(params?: {
    page?: number;
    page_size?: number;
    q?: string;
  }): Promise<HistoryListResponse> {
    const query = new URLSearchParams();
    if (params?.page) query.append('page', params.page.toString());
    if (params?.page_size) query.append('page_size', params.page_size.toString());
    if (params?.q) query.append('q', params.q);

    const queryString = query.toString() ? `?${query.toString()}` : '';
    const res = await fetch(`${API_BASE}/history${queryString}`);
    return handleResponse<HistoryListResponse>(res);
  },

  async getHistoryById(id: number): Promise<HistoryItem> {
    const res = await fetch(`${API_BASE}/history/${id}`);
    return handleResponse<HistoryItem>(res);
  },

  async deleteHistoryById(id: number): Promise<{ message: string; id: number }> {
    const res = await fetch(`${API_BASE}/history/${id}`, {
      method: 'DELETE',
    });
    return handleResponse<{ message: string; id: number }>(res);
  },

  async clearHistory(): Promise<{ message: string; deleted_count: number }> {
    const res = await fetch(`${API_BASE}/history`, {
      method: 'DELETE',
    });
    return handleResponse<{ message: string; deleted_count: number }>(res);
  },

  async getMetrics(): Promise<MetricsResponse> {
    const res = await fetch(`${API_BASE}/metrics`);
    return handleResponse<MetricsResponse>(res);
  },

  getPlotUrl(plotName: string): string {
    return `${API_BASE}/metrics/plots/${encodeURIComponent(plotName)}`;
  },
};
