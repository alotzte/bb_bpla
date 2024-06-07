import { api } from '@/shared/services/api';
import type { AxiosError } from 'axios';
import { createEffect, createEvent, createStore, sample } from 'effector';

export const dropezoneModalOpened = createEvent();
export const dropezoneModalClosed = createEvent();

export const loadFilesFx = createEffect<File[], AxiosError>();
export const loadInfoFx = createEffect<string[], AxiosError>();

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

loadFilesFx.use(api.files.sendFile);
