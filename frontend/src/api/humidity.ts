import { ClimateQueryParams, getApiData } from "@/api/api";
import { type Humidity } from "@/types/humidity";
import { ApiResponse } from "@/types/types";

export const URL = "/humidity";

export const getTemperature = async (params: ClimateQueryParams): Promise<ApiResponse<Humidity[]>> => {
  return await getApiData(URL, params);
}

export const getCurrentTemperature = async (): Promise<ApiResponse<Humidity>> => {
  return await getApiData(`${URL}/current`, {});
}
