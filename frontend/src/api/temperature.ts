import { ClimateQueryParams, getApiData } from "@/api/api";
import { type Temperature } from "@/types/temperature";
import { ApiResponse } from "@/types/types";

export const URL = "/temperature";

export const getTemperature = async (params: ClimateQueryParams): Promise<ApiResponse<Temperature[]>> => {
  return await getApiData(URL, params);
}

export const getCurrentTemperature = async (): Promise<ApiResponse<Temperature>> => {
  return await getApiData(`${URL}/current`, {});
}
