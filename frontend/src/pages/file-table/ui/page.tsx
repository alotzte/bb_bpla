import {
  type FilesTable,
  filesPaginationModel,
  pagination$,
  changePagination,
} from '@/entities/files';
import { useUnit } from 'effector-react';
import { getStatus, getType, pageUnmounted } from '../model';
import { useEffect, useState } from 'react';
import {
  Button,
  Dropdown,
  Flex,
  type MenuProps,
  Pagination,
  Table,
  Typography,
  Tooltip,
} from 'antd';
import { DropezoneModal, dropezoneModalOpened } from '@/features/dropezone';
import { api } from '@/shared/services/api';
import { FileModal, fileModalOpened, setSelectedId } from '@/features/player';
import { DownOutlined, ReloadOutlined, UpOutlined } from '@ant-design/icons';
import styled from 'styled-components';
import { ColumnsType } from 'antd/es/table';
import { formatTime } from '@/shared/lib/format';

const { Text } = Typography;

const Title = styled.div`
  width: 160px;
  text-overflow: ellipsis;
  overflow: hidden;
  white-space: nowrap;
`;

const columns: ColumnsType<FilesTable> = [
  { title: 'ID', dataIndex: 'id' },
  {
    title: 'Имя',
    render: (_, record) => (
      <Tooltip title={record.title} placement="topLeft">
        <Title>{record.title}</Title>
      </Tooltip>
    ),
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
        <Text type={record.status === 'inprogress' ? 'danger' : 'success'}>
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
  const [dropdownState, setDropdownState] = useState<boolean>(false);

  const openFile = ({ correlationId }: Pick<FilesTable, 'correlationId'>) => {
    setSelectedId(correlationId);
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

  const uploadClick = (type: api.FileType) => {
    setType(type);
    dropezoneModalOpened();
  };

  const items: MenuProps['items'] = [
    {
      key: 'archive',
      label: <div onClick={() => uploadClick('archive')}>Архив</div>,
    },
    {
      key: 'image',
      label: <div onClick={() => uploadClick('image')}>Изображение</div>,
    },
    {
      key: 'video',
      label: <div onClick={() => uploadClick('video')}>Видео</div>,
    },
  ];

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
          <Dropdown
            trigger={['click']}
            menu={{ items }}
            onOpenChange={setDropdownState}
          >
            <Button
              type={'primary'}
              icon={dropdownState ? <UpOutlined /> : <DownOutlined />}
              iconPosition="end"
            >
              Загрузить
            </Button>
          </Dropdown>
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
