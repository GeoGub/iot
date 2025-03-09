import axios from "axios";


const API = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_BASE_URL || "http://192.168.0.111:1234",
});

export const getApiData = (endpoint: string, params: object) => {
  return API.get(endpoint, { params });
}
