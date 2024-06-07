import type { PaginationParams, PaginationResponse } from '@/shared/lib';
import { httpClient } from '../http-client';

export type FileStatus = 'processed' | 'ready';
export type FileType = 'video' | 'image';

export interface FilesGetResponse {
  id: number;
  title: string;
  status: FileStatus;
  type: FileType;
  txt?: string;
}

export interface FileInfoGetResponse {
  marks: number[];
  link: string;
  type: FileType;
}

export const files = {
  get: async (params: PaginationParams) => {
    return await httpClient
      .get<PaginationResponse<FilesGetResponse>>('api/v1/results', {
        params,
      })
      .then((response) => response.data);
  },
  sendFile: async (files: File[]) => {
    const formData = new FormData();
    files.forEach((file) => formData.append(file.name, file));

    const config = {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    };

    return await httpClient
      .post('api/v1/files', formData, config)
      .then((response) => response.data);
  },
  getFileInfo: async (id: number) => {
    return await httpClient
      .get<FileInfoGetResponse>(`api/v1/files/${id}`)
      .then((response) => response.data);
  },
};
