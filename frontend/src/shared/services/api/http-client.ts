import axios, { AxiosError } from 'axios';
import { paramsSerializer } from './params-serializer';
import { getApiUrl, getApiUrl2 } from '@/shared/config';

// eslint-disable-next-line @typescript-eslint/no-explicit-any
export type ApiError<T = unknown, D = any> = AxiosError<T, D>;

export const httpClient = axios.create({
  baseURL: getApiUrl(window.location.protocol),
  paramsSerializer,
});

export const httpClient2 = axios.create({
  baseURL: getApiUrl2(window.location.protocol),
  paramsSerializer,
});

httpClient2.interceptors.request.use((config) => {
  return config;
});
