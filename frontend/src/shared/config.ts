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

export const getApiUrl = (protocol: Protocol) => `${getApiHost(protocol)}`;

export const isDev = () => import.meta.env.DEV;
