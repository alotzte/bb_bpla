import { createItemModel, createPaginationModel } from '@/shared/lib';
import { api } from '@/shared/services/api';

export interface FilesTable extends api.FilesGetResponse {
  key: React.Key;
}

export const filesPaginationModel = createPaginationModel({
  apiFn: api.files.get,
});

export const fileInfoModel = createItemModel({
  apiFn: api.files.getFileInfo,
});
