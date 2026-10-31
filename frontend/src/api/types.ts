export interface BoundingBox {
  x1: number;
  y1: number;
  x2: number;
  y2: number;
}

export type WarningLevel = 'low' | 'medium' | 'high' | 'info';

export interface SignSummary {
  id?: number;
  sign_code: string;
  name: string;
  group: string;
  meaning: string;
  recommended_action: string;
  warning_level: WarningLevel;
  source: string;
  source_checked_at?: string;
  image_url?: string | null;
}

export interface DetectionItem {
  class_id: number;
  class_name: string;
  confidence: number;
  bbox: BoundingBox;
  sign?: SignSummary | null;
  verification_required: boolean;
}

export interface DetectionResponse {
  request_id: string;
  status: string;
  image: {
    width: number;
    height: number;
    annotated_image: string;
  };
  summary: {
    detection_count: number;
    processing_ms: number;
  };
  detections: DetectionItem[];
  warnings: string[];
}

export interface SignItem {
  id: number;
  class_id: number;
  sign_code: string;
  name: string;
  group_name: string;
  meaning: string;
  recommended_action: string;
  warning_level: WarningLevel;
  image_url?: string | null;
  legal_source: string;
  source_checked_at: string;
  updated_at: string;
}

export type SignDetail = SignItem;

export interface SignListResponse {
  items: SignItem[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
}

export interface SignGroupSummary {
  group_name: string;
  count: number;
}

export interface HistoryItem {
  id: number;
  request_id: string;
  original_filename: string;
  created_at: string;
  detection_count: number;
  processing_ms: number;
  result?: {
    detection_count?: number;
    classes?: string[];
    processing_ms?: number;
  } | null;
}

export interface HistoryListResponse {
  items: HistoryItem[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
}

export interface HealthResponse {
  status: string;
  model_loaded: boolean;
  model_version: string;
  dataset_version: string;
  device: string;
  history_enabled: boolean;
  max_upload_mb: number;
  confidence_range: {
    min: number;
    max: number;
    default: number;
    verification_threshold: number;
  };
  supported_formats: string[];
}

export interface MetricsResponse {
  has_data: boolean;
  message?: string;
  metrics?: {
    experiment?: {
      dataset?: string;
      version?: string;
      model?: string;
      test_images?: number;
      test_instances?: number;
      conf_threshold?: number;
      iou_threshold?: number;
      device?: string;
    };
    metrics?: {
      precision?: number;
      recall?: number;
      f1?: number;
      map50?: number;
      map50_95?: number;
    };
    latency?: {
      preprocess_ms?: number;
      inference_ms?: number;
      postprocess_ms?: number;
      total_ms?: number;
      runs_count?: number;
    };
    classes?: Array<{
      class_id: number;
      class_name: string;
      sign_code?: string;
      precision: number;
      recall: number;
      f1: number;
      map50: number;
      map50_95: number;
      instances: number;
    }>;
  } | null;
  available_plots: string[];
}

export interface ApiError {
  code: string;
  message: string;
  request_id?: string;
  status: number;
}
