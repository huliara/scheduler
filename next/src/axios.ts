import axiosBase, { AxiosResponse } from "axios";

const axios = axiosBase.create({
  baseURL: "http://localhost:8888",
  headers: {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": "http://localhost:8888",
  },
  withCredentials: true,
  responseType: "json",
});

axios.interceptors.request.use(async (config) => {
  if (config.headers) {
    config.headers.Authorization = `Bearer ${localStorage.getItem(
      "accessToken"
    )}`;
  }

  return config;
});

export const fetcher = <T>(url: string): Promise<T> =>
  axios.get(url).then((res: AxiosResponse<T>) => res.data);

export default axios;
