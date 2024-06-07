import { createEvent, createStore, sample } from 'effector';

export const fileModalOpened = createEvent();
export const fileModalClosed = createEvent();

export const setSelectedId = createEvent<number>();
export const resetSelectedId = createEvent();

export const $isOpen = createStore<boolean>(false);
export const $selectedId = createStore<number | null>(null);

$selectedId.reset(resetSelectedId);

sample({
  clock: fileModalOpened,
  fn: () => true,
  target: $isOpen,
});

sample({
  clock: fileModalClosed,
  fn: () => false,
  target: $isOpen,
});

sample({
  clock: setSelectedId,
  target: $selectedId,
});
