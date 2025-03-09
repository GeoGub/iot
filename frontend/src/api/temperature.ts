import { getApiData } from "@/api/api";

export const getTemperature = () => {
  return getApiData("/temperatures", {});
}
