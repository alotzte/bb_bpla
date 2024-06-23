import { filesPaginationModel } from '@/entities/files';
import { api } from '@/shared/services/api';
import { reset } from 'patronum';

export const pageUnmounted = reset({
  target: [filesPaginationModel.$list, filesPaginationModel.$totalCount],
});

export const getStatus: Record<api.FileStatus, string> = {
  inprogress: 'Обрабатывается',
  ready: 'Обработано',
};

export const getType: Record<api.FileType, string> = {
  image: 'Изображение',
  video: 'Видео',
  archive: 'Архив',
};
