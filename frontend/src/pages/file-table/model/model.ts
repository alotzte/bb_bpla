import { filesPaginationModel } from '@/entities/files';
import { reset } from 'patronum';

export const pageUnmounted = reset({
  target: [filesPaginationModel.$list, filesPaginationModel.$totalCount],
});
