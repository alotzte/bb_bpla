import { createApi, createStore } from 'effector';

/** Модель работы с модальной формой */
export function createModalFormModel() {
  const $isOpen = createStore<boolean>(false);

  const modalApi = createApi($isOpen, {
    closeModal: () => false,
    openModal: () => true,
  });

  const unitShape = {
    isOpen: $isOpen,
    ...modalApi,
  };

  return {
    $isOpen,
    ...modalApi,
    '@@unitShape': () => unitShape,
  };
}
