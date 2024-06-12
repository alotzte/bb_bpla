import { combine, createEffect, createEvent, restore, sample } from 'effector';
import { status } from 'patronum';

export interface PaginationParams {
  limit: number;
  offset: number;
}

interface PaginationModelParams<GetParams, GetResponse> {
  /** Функция api для загрузки списка записей */
  apiFn: (params: GetParams) => Promise<GetResponse>;
}

const defaultPagination: PaginationParams = {
  limit: 10,
  offset: 0,
};

export interface PaginationResponse<T> extends PaginationParams {
  totalCount: number;
  items: T[];
}

export function createPaginationModel<GetParams = void, ItemType = unknown>(
  params: PaginationModelParams<GetParams, PaginationResponse<ItemType>>
) {
  const getItems = createEvent<GetParams>();
  const getItemsFx = createEffect<GetParams, PaginationResponse<ItemType>>();

  const $list = restore<ItemType[]>(
    getItemsFx.doneData.map((data) => data.items),
    []
  );
  const $totalCount = restore<number>(
    getItemsFx.doneData.map((data) => data.totalCount),
    0
  );

  const $status = status({ effect: getItemsFx });
  const $isLoading = getItemsFx.pending;
  const $notFound = combine(
    $status,
    $list,
    (status, list) => list.length === 0 && ['done', 'fail'].includes(status)
  );
  const $isFail = $status.map((status) => status === 'fail');

  sample({
    clock: getItems,
    target: getItemsFx,
  });

  getItemsFx.use(params.apiFn);

  const unitShape = {
    list: $list,
    isLoading: $isLoading,
    notFound: $notFound,
    isFail: $isFail,
    getItems: getItems,
    totalCount: $totalCount,
    defaultPagination,
  };

  return {
    $list,
    $isLoading,
    $notFound,
    $isFail,
    getItems,
    $totalCount,
    defaultPagination,
    '@@unitShape': () => unitShape,
  };
}
