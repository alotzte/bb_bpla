import { type FilesTable, filesPaginationModel } from '@/entities/files';
import type { ColumnsType } from 'antd/es/table';
import { useUnit } from 'effector-react';
import { pageUnmounted } from '../model';
import { useEffect, useState } from 'react';
import { Button, Flex, Pagination, Table } from 'antd';
import { DropezoneModal, dropezoneModalOpened } from '@/features/dropezone';
import { api } from '@/shared/services/api';
import { FileModal, fileModalOpened, setSelectedId } from '@/features/player';
import { Typography } from 'antd';

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
    dataIndex: 'title',
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
  },
  {
    title: 'Тип',
    render: (_, record) => (
      <Flex justify="center">
        <Text>{getType[record.type]}</Text>
      </Flex>
    ),
  },
];

export const FileTablePage = () => {
  const [files, isLoading, totalCount] = useUnit([
    filesPaginationModel.$list,
    filesPaginationModel.$isLoading,
    filesPaginationModel.$totalCount,
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
          <Button href={record.txt} type="link" target="_blank" download>
            Загрузить TXT файл
          </Button>
        </Flex>
      ),
  };

  return (
    <div>
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
          onChange={(page, limit) => {
            const offset = (page - 1) * limit;
            filesPaginationModel.getItems({ offset, limit });
          }}
        />
      </Flex>
      <DropezoneModal type={type} />
      <FileModal />
    </div>
  );
};
