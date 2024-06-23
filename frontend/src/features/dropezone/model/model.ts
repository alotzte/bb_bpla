import { filesPaginationModel, pagination$ } from '@/entities/files';
import { api } from '@/shared/services/api';
import { message } from 'antd';
import type { AxiosError } from 'axios';
import { createEffect, createEvent, createStore, sample } from 'effector';
import { or } from 'patronum';

export const dropezoneModalOpened = createEvent();
export const dropezoneModalClosed = createEvent();
export const loadFiles = createEvent<File[]>();
export const loadSingleFile = createEvent<File>();

const loadFilesFx = createEffect<File[], AxiosError>();
const loadSingleFileFx = createEffect<File, AxiosError>();
export const loadInfoFx = createEffect<string[], AxiosError>();

const notificationFx = createEffect<string, void>();

export const $isUploading = or(loadFilesFx.pending, loadSingleFileFx.pending);

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
  clock: loadSingleFile,
  target: loadSingleFileFx,
});

sample({
  clock: [loadFilesFx.doneData, loadSingleFileFx.doneData],
  fn: () => 'success',
  target: notificationFx,
});

sample({
  clock: [loadFilesFx.doneData, loadSingleFileFx.doneData],
  source: pagination$,
  fn: (pagination) => {
    const { current, pageSize } = pagination;
    const offset = (current - 1) * pageSize;
    return {
      offset,
      limit: pageSize,
    };
  },
  target: filesPaginationModel.getItems,
});

sample({
  clock: [loadFilesFx.failData, loadSingleFileFx.failData],
  fn: () => 'error',
  target: notificationFx,
});

sample({
  clock: [loadFilesFx.finally, loadSingleFileFx.finally],
  target: dropezoneModalClosed,
});

loadFilesFx.use(api.files.sendFiles);
loadSingleFileFx.use(api.files.sendSingleFile);

notificationFx.use((status) => {
  if (status === 'success') {
    message.success('Файлы успешно загружены');
  }
  if (status === 'error') {
    message.error('При загрузке файлов произшла ошибка');
  }
});
