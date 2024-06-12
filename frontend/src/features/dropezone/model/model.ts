import { api } from '@/shared/services/api';
import { message } from 'antd';
import type { AxiosError } from 'axios';
import { createEffect, createEvent, createStore, sample } from 'effector';

export const dropezoneModalOpened = createEvent();
export const dropezoneModalClosed = createEvent();
export const loadFiles = createEvent<File[]>();

const loadFilesFx = createEffect<File[], AxiosError>();
export const loadInfoFx = createEffect<string[], AxiosError>();

const notificationFx = createEffect<string, void>();

export const $isOpen = createStore<boolean>(false);

sample({
  clock: dropezoneModalOpened,
  fn: () => true,
  target: $isOpen,
});

sample({
  clock: dropezoneModalClosed,
  fn: () => false,
  target: $isOpen,
});

sample({
  clock: loadFiles,
  target: loadFilesFx,
});

sample({
  clock: loadFilesFx.doneData,
  fn: () => 'success',
  target: notificationFx,
});

sample({
  clock: loadFilesFx.failData,
  fn: () => 'error',
  target: notificationFx,
});

loadFilesFx.use(api.files.sendFile);

notificationFx.use((status) => {
  if (status === 'success') {
    message.success('Файлы успешно загружены');
  }
  if (status === 'error') {
    message.error('При загрузке файлов произшла ошибка');
  }
});
