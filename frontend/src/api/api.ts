import axios from "axios";
import { type ClimateQueryParams, type ApiResponse } from "@/types/types";


const API = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_BASE_URL || "http://192.168.0.105:8000",
});

export const getApiData = async <T>(endpoint: string, params: object): Promise<ApiResponse<T>> => {
  return API.get(endpoint, { params });
}

export { ClimateQueryParams }
