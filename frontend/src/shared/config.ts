/**
 * Модуль инициализации env-переменных
 * @remark Если не найдено значение хоть одной переменной,
 * Приложение сразу выбросит ошибку, при инициализации модуля
 * @module
 */

/**
 * Получение env-переменной
 * @throwable
 */
const getEnvVar = (key: string) => {
  if (import.meta.env[key] === undefined) {
    throw new Error(`Env variable ${key} is required`);
  }
  return import.meta.env[key] || '';
};

type Protocol = string;

const getApiHost = (protocol: Protocol) =>
  protocol === 'https:'
    ? getEnvVar('VITE_API_HOST_HTTPS')
    : getEnvVar('VITE_API_HOST_HTTP');

const getApiHost2 = (protocol: Protocol) =>
  protocol === 'https:'
    ? getEnvVar('VITE_API_DEMO_HOST_HTTPS')
    : getEnvVar('VITE_API_DEMO_HOST_HTTP');

export const getApiUrl = (protocol: Protocol) => `${getApiHost(protocol)}`;
export const getApiUrl2 = (protocol: Protocol) => `${getApiHost2(protocol)}`;

export const isDev = () => import.meta.env.DEV;
