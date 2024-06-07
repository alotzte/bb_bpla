import { combine, createEffect, createEvent, restore, sample } from 'effector';
import { status } from 'patronum';

interface ListModelParams<GetParams, GetResponse> {
  /** Функция api для загрузки списка записей */
  apiFn: (params: GetParams) => Promise<GetResponse>;
}

/**
 * Создает модель для загрузки списка (без пагинации).
 * @see {@linkcode createPaginatedSource} для модели с пагинацией;
 * @see {@linkcode createSequentiallyLoadedSource} для модели с последовательно загружааемым источником данных.
 */
export function createListModel<GetParams = void, ItemType = unknown>(
  params: ListModelParams<GetParams, ItemType[]>
) {
  const getListFx = createEffect<GetParams, ItemType[]>();
  const getListOnce = createEvent<GetParams>();

  const $list = restore<ItemType[]>(getListFx.doneData, []);

  const $status = status({ effect: getListFx });
  const $isLoading = getListFx.pending;
  const $notFound = combine(
    $status,
    $list,
    (status, list) => list.length === 0 && ['done', 'fail'].includes(status)
  );
  const $isFail = $status.map((status) => status === 'fail');

  sample({
    clock: getListOnce,
    source: combine({ isLoading: $isLoading, list: $list }),
    filter: ({ isLoading, list }) => !isLoading && list.length === 0,
    fn: (_, payload) => payload,
    target: getListFx,
  });

  getListFx.use(params.apiFn);

  const unitShape = {
    list: $list,
    isLoading: $isLoading,
    notFound: $notFound,
    isFail: $isFail,
    getList: getListFx,
    getListOnce: getListOnce,
  };

  return {
    $list,
    $isLoading,
    $notFound,
    $isFail,
    getListFx,
    /** Запрос НЕ стартует, если данные уже есть или идет загрузка */
    getListOnce,
    /** https://effector.dev/docs/ecosystem-development/unit-shape-protocol */
    '@@unitShape': () => unitShape,
  };
}
