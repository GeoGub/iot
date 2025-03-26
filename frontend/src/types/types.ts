export interface BaseClimate {
  created_at_timestamp: number;
}

export interface ClimateQueryParams {
  start_timestamp?: number;
  end_timestamp?: number;
}

export interface ApiResponse<T> {
  data: T;
  status: number;
  message?: string;
}
