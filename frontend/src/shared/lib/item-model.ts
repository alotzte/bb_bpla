import { combine, createEffect, restore } from 'effector';
import { status } from 'patronum';

interface ItemModelParams<GetParams, GetResponse> {
  /** Функция api для загрузки одной записи */
  apiFn: (params: GetParams) => Promise<GetResponse>;
}

/** Создает модель для загрузки одной записи */
export function createItemModel<GetParams, GetResponse>(
  params: ItemModelParams<GetParams, GetResponse>
) {
  const getItemFx = createEffect<GetParams, GetResponse>();

  const $item = restore<GetResponse>(getItemFx.doneData, null);

  const $status = status({ effect: getItemFx });
  const $isLoading = getItemFx.pending;
  const $notFound = combine(
    $status,
    $item,
    (status, item) => !item && ['done', 'fail'].includes(status)
  );

  getItemFx.use(params.apiFn);

  return {
    $item,
    $isLoading,
    $notFound,
    getItemFx,
  };
}
