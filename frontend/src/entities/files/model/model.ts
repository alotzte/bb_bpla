import { createItemModel, createPaginationModel } from '@/shared/lib';
import { api } from '@/shared/services/api';
import { createEvent, createStore, sample } from 'effector';

interface Pagination {
  current: number;
  pageSize: number;
}

export interface FilesTable extends api.FilesGetResponse {
  key: React.Key;
}

export const filesPaginationModel = createPaginationModel({
  apiFn: api.files.get,
});

export const fileInfoModel = createItemModel({
  apiFn: api.files.getFileInfo,
});

export const changePagination = createEvent<Pagination>();

export const pagination$ = createStore<Pagination>({
  current: 1,
  pageSize: 10,
});

sample({
  clock: changePagination,
  target: pagination$,
});
