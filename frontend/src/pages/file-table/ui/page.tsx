import {
  type FilesTable,
  filesPaginationModel,
  pagination$,
  changePagination,
} from '@/entities/files';
import type { ColumnsType } from 'antd/es/table';
import { useUnit } from 'effector-react';
import { pageUnmounted } from '../model';
import { useEffect, useState } from 'react';
import { Button, Flex, Pagination, Table } from 'antd';
import { DropezoneModal, dropezoneModalOpened } from '@/features/dropezone';
import { api } from '@/shared/services/api';
import { FileModal, fileModalOpened, setSelectedId } from '@/features/player';
import { Typography } from 'antd';
import { ReloadOutlined } from '@ant-design/icons';
import styled from 'styled-components';
import { formatTime } from '@/shared/lib/format';

const { Text } = Typography;

const getStatus: Record<api.FileStatus, string> = {
  processed: 'Обрабатывается',
  ready: 'Обработано',
};

const getType: Record<api.FileType, string> = {
  image: 'Изображение',
  video: 'Видео',
};

const columns: ColumnsType<FilesTable> = [
  { title: 'ID', dataIndex: 'id' },
  {
    title: 'Имя',
    render: (_, record) => <Title>{record.title}</Title>,
    width: 180,
  },
  {
    title: 'Время загрузки',
    render: (_, record) => (
      <Flex justify="center">
        {record.uploadDateTime &&
          new Date(record.uploadDateTime).toLocaleString()}
      </Flex>
    ),
    align: 'center',
  },
  {
    title: 'Время обработки',
    render: (_, record) => (
      <Flex justify="center">
        {record.processedTime && formatTime.msecToString(record.processedTime)}
      </Flex>
    ),
    align: 'center',
  },
  {
    title: 'Статус',
    render: (_, record) => (
      <Flex justify="center">
        <Text type={record.status === 'processed' ? 'danger' : 'success'}>
          {getStatus[record.status]}
        </Text>
      </Flex>
    ),
    align: 'center',
  },
  {
    title: 'Тип',
    render: (_, record) => (
      <Flex justify="center">
        <Text>{getType[record.type]}</Text>
      </Flex>
    ),
    align: 'center',
  },
];

export const FileTablePage = () => {
  const [files, isLoading, totalCount, pagination] = useUnit([
    filesPaginationModel.$list,
    filesPaginationModel.$isLoading,
    filesPaginationModel.$totalCount,
    pagination$,
  ]);

  const [type, setType] = useState<api.FileType>('image');

  const openFile = ({ id }: Pick<FilesTable, 'id'>) => {
    setSelectedId(id);
    fileModalOpened();
  };

  useEffect(() => {
    return () => {
      pageUnmounted();
    };
  }, []);

  useEffect(() => {
    filesPaginationModel.getItems(filesPaginationModel.defaultPagination);
  }, []);

  const actionColumn = {
    title: '',
    key: 'action',
    width: 180,
    render: (record: FilesTable) =>
      record.status === 'ready' && (
        <Flex vertical justify="center">
          <Button type="link" onClick={() => openFile(record)}>
            Подробнее
          </Button>
          {record.txt && (
            <Button href={record.txt} type="link" target="_blank" download>
              Загрузить TXT файл
            </Button>
          )}
        </Flex>
      ),
  };

  return (
    <div>
      <Flex justify="space-between">
        <Flex gap="small">
          <Button
            type="primary"
            onClick={() => {
              setType('video');
              dropezoneModalOpened();
            }}
          >
            Загрузить видео
          </Button>
          <Button
            onClick={() => {
              setType('image');
              dropezoneModalOpened();
            }}
          >
            Загрузить фото
          </Button>
        </Flex>
        <Button
          type="primary"
          loading={isLoading}
          icon={<ReloadOutlined />}
          onClick={() => {
            const { current, pageSize } = pagination;
            const offset = (current - 1) * pageSize;
            filesPaginationModel.getItems({ offset, limit: pageSize });
          }}
        >
          Обновить
        </Button>
      </Flex>
      <Table
        loading={isLoading}
        columns={[...columns, actionColumn]}
        dataSource={files.map((file, index) => ({ ...file, key: index }))}
        pagination={false}
        style={{ marginTop: '16px', marginBottom: '16px' }}
      />
      <Flex justify="end">
        <Pagination
          total={totalCount}
          showSizeChanger
          current={pagination.current}
          pageSize={pagination.pageSize}
          onChange={(current, pageSize) => {
            changePagination({ current, pageSize });
            const offset = (current - 1) * pageSize;
            filesPaginationModel.getItems({ offset, limit: pageSize });
          }}
        />
      </Flex>
      <DropezoneModal type={type} />
      <FileModal />
    </div>
  );
};

const Title = styled.div`
  width: 160px;
  text-overflow: ellipsis;
  overflow: hidden;
  white-space: nowrap;
`;
