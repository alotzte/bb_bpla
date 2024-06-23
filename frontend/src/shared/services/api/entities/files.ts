import type { PaginationParams, PaginationResponse } from '@/shared/lib';
import { httpClient } from '../http-client';

export type FileStatus = 'inprogress' | 'ready';
export type FileType = 'video' | 'image' | 'archive';

export interface FilesGetResponse {
  id: number;
  title: string;
  status: FileStatus;
  type: FileType;
  txt?: string;
  uploadDateTime?: string;
  processedTime?: number;
  correlationId: string;
}

export interface FileInfoGetResponse {
  marks: number[];
  link?: string;
  type: FileType;
  archiveLink?: string;
}

export const files = {
  get: async (params: PaginationParams) => {
    return await httpClient
      .get<PaginationResponse<FilesGetResponse>>('api/v1/results', {
        params,
      })
      .then((response) => response.data);
  },
  sendFiles: async (uploadedFiles: File[]) => {
    const formData = new FormData();

    for (let i = 0; i < uploadedFiles.length; i++) {
      formData.append('files', uploadedFiles[i]);
    }

    const config = {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    };

    return await httpClient
      .post('api/v1/upload', formData, config)
      .then((response) => response.data);
  },
  sendSingleFile: async (uploadedFile: File) => {
    const formData = new FormData();

    formData.append('file', uploadedFile);

    const config = {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    };

    return await httpClient
      .post('api/v1/upload/single', formData, config)
      .then((response) => response.data);
  },
  getFileInfo: async (id: string) => {
    return await httpClient
      .get<FileInfoGetResponse>(`api/v1/files/${id}`)
      .then((response) => response.data);
  },
};
