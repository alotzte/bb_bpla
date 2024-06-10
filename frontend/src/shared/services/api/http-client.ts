import axios, { AxiosError } from 'axios';
import { paramsSerializer } from './params-serializer';
import { getApiUrl } from '@/shared/config';

// eslint-disable-next-line @typescript-eslint/no-explicit-any
export type ApiError<T = unknown, D = any> = AxiosError<T, D>;

export const httpClient = axios.create({
  baseURL: getApiUrl(window.location.protocol),
  paramsSerializer,
});
